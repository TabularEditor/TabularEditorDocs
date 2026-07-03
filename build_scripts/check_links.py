#!/usr/bin/env python
"""
Standalone dead-link checker for the generated `_site`.

Walks the built HTML, resolves every href/src to a local file or an external
URL, visits each unique target once, and reports references to broken targets
(missing files, missing fragments). Local failures are errors (nonzero exit);
external failures are warnings (network issues are often transient or the
target blocks bots), emitted as a copy-paste list of URLs to verify by hand.

The functional core (extract, resolve, validate) is pure; the imperative shell
does filesystem, HTTP, and reporting.
"""

import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
from time import monotonic
from typing import NamedTuple
from urllib.parse import unquote, urldefrag, urlsplit


def _normalize_text(text: str) -> str:
    """Collapse whitespace and case-fold, so text-fragment queries match the page regardless of layout or case."""
    return " ".join(text.split()).casefold()


class _LinkAnchorParser(HTMLParser):
    """Collects href/src references and fragment targets (`id`, and `name` on `a`), and optionally the page text."""

    def __init__(self, collect_text: bool = False) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, int]] = []  # (href, 1-based line in the source HTML)
        self.anchors: set[str] = set()
        self._collect_text = collect_text
        self._chunks: list[str] = []
        self._skip_depth = 0  # inside <script>/<style>, whose text is not visible content

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        line = self.getpos()[0]
        # <link> is head chrome (canonical/hreflang SEO tags, stylesheets), never authored content.
        if tag != "link":
            for key in ("href", "src"):
                if value := attr.get(key):
                    self.links.append((value, line))
        if element_id := attr.get("id"):
            self.anchors.add(element_id)
        if tag == "a" and (name := attr.get("name")):
            self.anchors.add(name)
        if tag in ("script", "style"):
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._collect_text and not self._skip_depth:
            self._chunks.append(data)

    @property
    def text(self) -> str:
        return "".join(self._chunks)


def extract(html: str) -> tuple[list[tuple[str, int]], set[str]]:
    """Parse one page into (referenced (URL, line) pairs, fragment targets defined on the page)."""
    parser = _LinkAnchorParser()
    parser.feed(html)
    return parser.links, parser.anchors


def cmd_extract(args: list[str]) -> int:
    """Print the links (with line numbers) and fragment targets extracted from an HTML file."""
    links, anchors = extract(Path(args[0]).read_text(encoding="utf-8"))
    for href, line in links:
        print(f"link\t{line}\t{href}")
    for anchor in sorted(anchors):
        print(f"anchor\t{anchor}")
    return 0


class Target(NamedTuple):
    """A resolved link destination: a local file, an external URL, or a root-absolute site link."""

    kind: str  # "local" (filesystem), "external" (HTTP), or "site" (root-absolute, resolved by resolve_site_targets)
    resource: str  # local: normalized filesystem path; external: URL; site: root-absolute URL path
    fragment: str  # decoded element-id anchor, or "" for none / page-top
    text_targets: tuple[str, ...]  # decoded text segments of a `:~:text=` directive that must all be on the page
    internal: bool = False  # a link to our own site; a failure is an error even when checked over HTTP


_SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")

# API endpoints and the like that are documented in the docs but are not pages meant to be fetched. The `api.`
# heuristic covers most (api.openai.com, *.api.daxoptimizer.com, ...); add other non-gettable hosts explicitly.
_UNCHECKED_HOSTS: set[str] = set()

# Any hosts where we observe 429s when we use `stats` get a lower max for
# in-flight requests. Try to be a good citizen of the web.
_HOST_MAX_IN_FLIGHT_OVERRIDES = {"github.com": 6}

# Where root-absolute ("site") links resolve on the deployed site. Ones missing from the local build are checked
# here, because the deployed site's redirects (Azure SWA) make many of them valid even without a matching file.
_LIVE_SITE_BASE = "https://docs.tabulareditor.com"

# Some encoders (DocFX/Markdig) percent-encode the ~ in the :~: text-fragment delimiter, so it must be normalized
# before the split -- partitioning the still-encoded fragment would miss the delimiter entirely.
_FRAGMENT_DELIMITER = ":~:"
_ENCODED_DELIMITER_CHARS = {"%7e": "~", "%7E": "~"}


def _is_skippable(href: str) -> bool:
    """True for hrefs with nothing to check: empty, a bare '#', or a non-navigable scheme."""
    return not href or href == "#" or href.lower().startswith(_SKIP_SCHEMES)


def _is_external(url: str) -> bool:
    """True for absolute or protocol-relative URLs, which are checked over HTTP rather than on disk."""
    return url.lower().startswith(("http://", "https://", "//"))


def _is_root_absolute(url: str) -> bool:
    """True for site-root-relative links, resolved against the site root rather than the source page."""
    return url.startswith("/")


def _is_unchecked_host(host: str) -> bool:
    """True for hosts we deliberately skip -- API endpoints and other documented-but-not-navigable URLs."""
    return host in _UNCHECKED_HOSTS or host.startswith("api.") or ".api." in host


def _split_fragment(raw_fragment: str) -> tuple[str, str]:
    """Split a raw URL fragment into (element-id anchor, text directive), decoding an encoded delimiter first so
    the :~: split is found even when the ~ arrives percent-encoded. Delimiters are decoded before the split; the
    directive's own values stay encoded for `_parse_text_directive` to split and decode."""
    normalized = raw_fragment
    for encoded, decoded in _ENCODED_DELIMITER_CHARS.items():
        normalized = normalized.replace(encoded, decoded)
    anchor, _, directive = normalized.partition(_FRAGMENT_DELIMITER)
    return anchor, directive


def _parse_text_directive(directive: str) -> tuple[str, ...]:
    """The decoded text segments of a `:~:text=` fragment directive (textStart and textEnd), all of which must be
    present on the page. Empty if it is not a text directive. The optional prefix-/-suffix context is dropped."""
    if not directive.startswith("text="):
        return ()
    # value is [prefix-,]textStart[,textEnd][,-suffix]; keep the non-context segments.
    segments = [seg for seg in directive[len("text=") :].split(",") if seg]
    return tuple(unquote(seg) for seg in segments if not seg.endswith("-") and not seg.startswith("-"))


def resolve(href: str, source_page: Path, site_root: Path) -> Target | None:
    """Classify and normalize a raw href into a checkable Target, or None when there is nothing to check."""
    href = href.strip()
    if _is_skippable(href):
        return None
    url, raw_fragment = urldefrag(href)
    anchor, directive = _split_fragment(raw_fragment)
    fragment = unquote(anchor)
    if fragment == "top":  # browsers scroll to the page top for #top even with no matching element
        fragment = ""
    text_targets = _parse_text_directive(directive)
    if _is_external(url):
        return None if _is_unchecked_host(_host_of(url)) else Target("external", url, fragment, text_targets)
    if not url:  # a same-page "#fragment" reference (nothing to check for a pure text directive)
        return Target("local", str(source_page), fragment, text_targets) if fragment else None
    if _is_root_absolute(url):  # a site link; resolve_site_targets decides on-disk vs live once the tree is known
        return Target("site", url, fragment, text_targets)
    base = source_page.parent / url
    return Target("local", os.path.normpath(base), fragment, text_targets)


def cmd_resolve(args: list[str]) -> int:
    """Print the resolved Target (or 'skip') for a raw href found in a source page."""
    href, source_page = args[0], Path(args[1])
    site_root = Path(args[2]) if len(args) > 2 else Path("_site")
    target = resolve(href, source_page, site_root)
    if target is None:
        print("skip")
    else:
        print(f"{target.kind}\t{target.resource}\t{target.fragment}\t{target.text_targets}")
    return 0


def enumerate_site(
    root: Path, source_prefix: str | None = None
) -> tuple[dict[Target, dict[str, list[int]]], dict[str, set[str]]]:
    """Walk the built site under `root`: return (target -> {referring page -> line numbers}) and (page -> anchors).

    Anchors are indexed for every page so fragment targets anywhere resolve, but links are collected only from pages
    whose path starts with `source_prefix` (when given) -- a way to check just a subset of the docs."""
    refs: dict[Target, dict[str, list[int]]] = {}
    anchors_by_file: dict[str, set[str]] = {}
    for page in root.rglob("*.html"):
        source = os.path.normpath(page)
        links, anchors = extract(page.read_text(encoding="utf-8"))
        anchors_by_file[source] = anchors
        if source_prefix and not source.startswith(source_prefix):
            continue  # index this page's anchors, but do not check its outgoing links
        for href, line in links:
            target = resolve(href, page, root)
            if target is not None:
                refs.setdefault(target, {}).setdefault(source, []).append(line)
    return refs, anchors_by_file


def cmd_enumerate(args: list[str]) -> int:
    """Print summary counts for the site's links and fragment targets."""
    root = Path(args[0]) if args else Path("_site")
    refs, anchors_by_file = enumerate_site(root)
    local = sum(1 for target in refs if target.kind == "local")
    external = sum(1 for target in refs if target.kind == "external")
    site = sum(1 for target in refs if target.kind == "site")
    total = sum(len(lines) for sources in refs.values() for lines in sources.values())
    print(f"html files indexed: {len(anchors_by_file)}")
    print(f"unique targets:     {len(refs)}  (local {local}, external {external}, site {site})")
    print(f"total references:   {total}")
    return 0


# A real browser User-Agent: stdlib's default python-urllib string is 403'd by GitHub and Microsoft Learn.
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class FetchResult(NamedTuple):
    """The outcome of visiting one external URL: reachability, status, any error detail, and page anchors (GET only)."""

    ok: bool  # True when the server answered with a 2xx/3xx status
    status: int  # HTTP status code, or 0 when the request never completed
    detail: str  # human-readable error for the report, or "" on success
    anchors: set[str]  # fragment targets found in the body (populated only on a body-parsing GET)
    retry_after: int  # seconds requested by a 429 Retry-After header; 0 otherwise
    method: str  # the request method that produced this result ("HEAD"/"GET"), or "" if none completed
    text: str  # normalized visible page text for text-fragment checks (populated only on a body-parsing GET)


# Hosts confirmed to 404 a HEAD they serve on GET; skip the doomed HEAD probe for them. Diagnostics
# (`head_fallbacks`) surface further candidates to add here.
_GET_ONLY_HOSTS = {"cdn.tabulareditor.com", "www.nuget.org"}


def _host_of(url: str) -> str:
    """The lowercased host of an external URL (with a scheme prepended for protocol-relative //host)."""
    return urlsplit("https:" + url if url.startswith("//") else url).netloc.lower()


def _parse_retry_after(value: str | None) -> int:
    """Seconds from a 429 Retry-After header; 0 when absent or given as an HTTP-date we do not parse."""
    return int(value) if value and value.isdigit() else 0


def fetch_external(url: str, need_body: bool) -> FetchResult:
    """Visit one external URL. HEAD is a cheap reachability probe; any HEAD failure is reconfirmed with a GET before
    the URL is declared broken, because many hosts 404/405 a HEAD they would serve (known ones skip HEAD via
    `_GET_ONLY_HOSTS`). GET downloads the body only when a fragment must be verified."""
    target = "https:" + url if url.startswith("//") else url  # protocol-relative //host needs a scheme
    get_only = need_body or _host_of(url) in _GET_ONLY_HOSTS
    for method in (("GET",) if get_only else ("HEAD", "GET")):
        request = urllib.request.Request(target, method=method, headers={"User-Agent": _USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                anchors: set[str] = set()
                text = ""
                # Download the body only to verify a fragment; a reachability GET (the HEAD fallback) needs just the
                # status, and reading it would pull whole binaries (installers, images) off the CDN.
                if method == "GET" and need_body:
                    charset = response.headers.get_content_charset() or "utf-8"
                    parser = _LinkAnchorParser(collect_text=True)
                    parser.feed(response.read().decode(charset, "replace"))
                    anchors, text = parser.anchors, _normalize_text(parser.text)
                return FetchResult(True, response.status, "", anchors, 0, method, text)
        except urllib.error.HTTPError as error:
            if method == "HEAD":
                continue  # HEAD is only a probe; reconfirm the failure with a GET
            retry_after = _parse_retry_after(error.headers.get("Retry-After")) if error.code == 429 else 0
            return FetchResult(False, error.code, f"HTTP {error.code} {error.reason}", set(), retry_after, method, "")
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            if method == "HEAD":
                continue  # reconfirm transport failures with a GET too
            return FetchResult(False, 0, str(getattr(error, "reason", error)), set(), 0, method, "")
    return FetchResult(False, 0, "no request attempted", set(), 0, "", "")


class _Task(NamedTuple):
    """A queued fetch: the URL, whether its body is needed, its host (cached), and the 429 retry count so far."""

    url: str
    need_body: bool
    host: str
    attempt: int


class HostStats(NamedTuple):
    """Per-host fetch diagnostics for understanding timing and rate limiting."""

    requests: int  # fetch attempts completed, including 429 retries
    rate_limited: int  # 429 responses received
    wait_seconds: float  # total cooldown time applied to the host
    head_fallbacks: int  # reachability GETs after a failed HEAD (candidates for _GET_ONLY_HOSTS)
    final_cap: int  # ending per-host in-flight cap (below the start value means it was throttled down)
    retry_after_seen: frozenset[int]  # distinct Retry-After values seen on 429s (0 = header absent/unparsed)


_MAX_RETRIES = 8  # per-URL: after this many 429 retries, give up on a URL and record the last result


def _backoff(attempt: int) -> float:
    """Seconds to wait before retrying a 429 that carried no Retry-After: 1, 2, 4, ..."""
    return float(2**attempt)


def _next_cooldown_wait(pending: dict[str, deque[_Task]], cooldown: dict[str, float], now: float) -> float | None:
    """Seconds until the soonest cooling-down host with pending work becomes eligible, or None if none are cooling."""
    waits = [cooldown[host] - now for host in pending if cooldown.get(host, 0.0) > now]
    return min(waits) if waits else None


def fetch_all_external(
    refs: dict[Target, dict[str, list[int]]], max_per_host: int = 8, max_workers: int = 16
) -> tuple[dict[str, FetchResult], dict[str, HostStats]]:
    """Fetch every unique external URL once. `max_workers` threads drain a shared work queue kept as full as
    eligibility allows; admission holds each host to its current cap (starting at `max_per_host`). A 429 cools the
    host down (honoring Retry-After), drops its cap by one as backpressure, and re-queues its URLs for after the
    wait. GET only when a fragment must be verified. Returns the results plus per-host diagnostics.

    All scheduling state is owned by this thread alone (workers only pull tasks and push results), so it needs no
    locks. On a 429 we also reclaim that host's not-yet-claimed tasks from the queue; any a worker already grabbed
    slip through, which is a bounded, acceptable miss."""
    need_body: dict[str, bool] = {}
    for target in refs:
        if target.kind == "external":
            wants_body = bool(target.fragment) or bool(target.text_targets)
            need_body[target.resource] = need_body.get(target.resource, False) or wants_body

    pending: dict[str, deque[_Task]] = defaultdict(deque)
    for url, body in need_body.items():
        host = _host_of(url)
        pending[host].append(_Task(url, body, host, 0))

    work_q: Queue[_Task | None] = Queue()
    done_q: Queue[tuple[_Task, FetchResult]] = Queue()
    outstanding: dict[str, int] = defaultdict(int)
    host_cap: dict[str, int] = defaultdict(lambda: max_per_host)
    host_cap.update(_HOST_MAX_IN_FLIGHT_OVERRIDES)
    cooldown: dict[str, float] = {}
    results: dict[str, FetchResult] = {}

    requests: dict[str, int] = defaultdict(int)
    rate_limited: dict[str, int] = defaultdict(int)
    wait_seconds: dict[str, float] = defaultdict(float)
    head_fallbacks: dict[str, int] = defaultdict(int)
    retry_after_seen: dict[str, set[int]] = defaultdict(set)

    def worker() -> None:
        while (task := work_q.get()) is not None:
            done_q.put((task, fetch_external(task.url, task.need_body)))

    def admit() -> None:
        now = monotonic()
        for host, queued in pending.items():
            while queued and outstanding[host] < host_cap[host] and cooldown.get(host, 0.0) <= now:
                outstanding[host] += 1
                work_q.put(queued.popleft())

    def reclaim(host: str) -> None:
        """Pull the cooling host's not-yet-claimed tasks back out of the work queue so they wait for the cooldown."""
        kept: list[_Task | None] = []
        try:
            while True:
                task = work_q.get_nowait()
                if task is not None and task.host == host:
                    outstanding[host] -= 1
                    pending[host].appendleft(task)
                else:
                    kept.append(task)
        except Empty:
            pass
        for task in kept:
            work_q.put(task)

    workers = [Thread(target=worker) for _ in range(max_workers)]
    for thread in workers:
        thread.start()

    remaining = len(need_body)
    admit()
    while remaining:
        try:
            task, result = done_q.get(timeout=_next_cooldown_wait(pending, cooldown, monotonic()))
        except Empty:
            admit()  # a cooldown expired; that host is eligible again
            continue
        outstanding[task.host] -= 1
        requests[task.host] += 1
        if result.method == "GET" and not task.need_body and task.host not in _GET_ONLY_HOSTS:
            head_fallbacks[task.host] += 1
        if result.status == 429:
            rate_limited[task.host] += 1
            retry_after_seen[task.host].add(result.retry_after)
        if result.status == 429 and task.attempt < _MAX_RETRIES:
            host_cap[task.host] = max(1, host_cap[task.host] - 1)  # adaptive backpressure
            delay = result.retry_after or _backoff(task.attempt)
            wait_seconds[task.host] += delay
            cooldown[task.host] = monotonic() + delay
            pending[task.host].appendleft(task._replace(attempt=task.attempt + 1))
            reclaim(task.host)
        else:
            results[task.url] = result
            remaining -= 1
        admit()

    for _ in workers:
        work_q.put(None)
    for thread in workers:
        thread.join()

    stats = {
        host: HostStats(
            requests[host],
            rate_limited[host],
            wait_seconds[host],
            head_fallbacks[host],
            host_cap[host],
            frozenset(retry_after_seen[host]),
        )
        for host in pending
    }
    return results, stats


def cmd_fetch(args: list[str]) -> int:
    """Fetch a single external URL (pass a second arg to force a body-parsing GET) and print the result."""
    url = args[0]
    need_body = len(args) > 1
    result = fetch_external(url, need_body)
    print(
        f"ok={result.ok} status={result.status} anchors={len(result.anchors)} "
        f"retry_after={result.retry_after} detail={result.detail}"
    )
    return 0


class Failure(NamedTuple):
    """A broken target: the target, a short reason, and each referring page mapped to the lines it appears on."""

    target: Target
    reason: str
    sources: dict[str, list[int]]


def _find_local_file(resource: str, existing_files: set[str]) -> str | None:
    """Map a resolved local path to an existing file, trying `.html` and `index.html` fallbacks; None if absent."""
    if resource in existing_files:
        return resource
    if not resource.endswith(".html"):
        for fallback in (f"{resource}.html", os.path.normpath(os.path.join(resource, "index.html"))):
            if fallback in existing_files:
                return fallback
    return None


def validate(
    refs: dict[Target, dict[str, list[int]]],
    anchors_by_file: dict[str, set[str]],
    existing_files: set[str],
    external_results: dict[str, FetchResult],
) -> list[Failure]:
    """Cross-reference every target against the filesystem snapshot and fetch results into a list of failures."""
    failures: list[Failure] = []
    for target, sources in refs.items():
        if target.kind == "local":
            resolved = _find_local_file(target.resource, existing_files)
            if resolved is None:
                failures.append(Failure(target, "missing file", sources))
            elif target.fragment and target.fragment not in anchors_by_file.get(resolved, set()):
                failures.append(Failure(target, "missing anchor", sources))
        else:
            result = external_results.get(target.resource)
            if result is None:
                failures.append(Failure(target, "not fetched", sources))
            elif not result.ok:
                failures.append(Failure(target, result.detail or f"unreachable (status {result.status})", sources))
            elif target.text_targets and not all(_normalize_text(t) in result.text for t in target.text_targets):
                failures.append(Failure(target, "missing text", sources))
            elif target.fragment and target.fragment not in result.anchors:
                failures.append(Failure(target, "missing anchor", sources))
    return failures


def _existing_files(root: Path) -> set[str]:
    """Snapshot every file under `root` as a normalized path, for pure existence checks in `validate`."""
    return {os.path.normpath(path) for path in root.rglob("*") if path.is_file()}


def resolve_site_targets(
    refs: dict[Target, dict[str, list[int]]], existing_files: set[str], site_root: Path, live: bool
) -> dict[Target, dict[str, list[int]]]:
    """Resolve root-absolute ("site") links against the built tree: those present on disk become ordinary local
    checks; those absent are checked against the live site (its redirects usually make them valid) and, being our
    own links, a failure there is an error, not a warning. With `live` false (offline mode) absent links stay
    on-disk errors. Non-site targets pass through unchanged."""
    resolved: dict[Target, dict[str, list[int]]] = {}
    for target, sources in refs.items():
        reclassified = target
        if target.kind == "site":
            disk_path = os.path.normpath(site_root / target.resource.lstrip("/"))
            if live and _find_local_file(disk_path, existing_files) is None:
                url = _LIVE_SITE_BASE + target.resource
                reclassified = Target("external", url, target.fragment, target.text_targets, internal=True)
            else:
                reclassified = target._replace(kind="local", resource=disk_path)
        merged = resolved.setdefault(reclassified, {})
        for source, lines in sources.items():
            merged.setdefault(source, []).extend(lines)
    return resolved


def map_to_source(built: str, root: Path) -> str | None:
    """Map a built HTML path back to its authored markdown under content/, or None for generated/localized pages."""
    parts = Path(os.path.relpath(built, root)).parts  # e.g. ("en", "features", "foo.html")
    if len(parts) >= 2 and parts[0] == "en" and parts[1] != "api":
        return os.path.normpath(os.path.join("content", str(Path(*parts[1:]).with_suffix(".md"))))
    return None


def _anchor_member(type_stem: str, fragment: str) -> str:
    """Best-effort member name from a DocFX member anchor; empty when the anchor scheme does not match."""
    prefix = type_stem.replace(".", "_") + "_"
    return fragment[len(prefix):].split("_", 1)[0] if fragment.startswith(prefix) else ""


def _fragment_suffix(target: Target) -> str:
    """The full URL fragment for display: the element-id anchor and/or the complete `:~:text=` directive, or ""."""
    directive = ("text=" + ",".join(target.text_targets)) if target.text_targets else ""
    if target.fragment and directive:
        return f"#{target.fragment}:~:{directive}"
    if target.fragment:
        return f"#{target.fragment}"
    return f"#:~:{directive}" if directive else ""


def humanize(target: Target) -> str:
    """A greppable rendering of the destination for finding it in the markdown source (best-effort for API anchors)."""
    if target.kind == "external":
        return _display_url(target) + _fragment_suffix(target)
    stem = os.path.basename(target.resource).removesuffix(".html")
    if not target.fragment:
        return stem
    member = _anchor_member(stem, target.fragment)
    type_name = stem.rsplit(".", 1)[-1]  # last dotted segment of the type UID
    return f"{type_name}.{member}" if member else f"{type_name} (#{target.fragment})"


def _display_url(target: Target) -> str:
    """The path or URL shown for a target. Internal (live-checked own-site) links show the authored root-absolute
    path rather than the live URL; protocol-relative externals get an https scheme."""
    if target.internal:
        return target.resource.removeprefix(_LIVE_SITE_BASE)
    if target.kind == "external" and target.resource.startswith("//"):
        return "https:" + target.resource
    return target.resource


def report(failures: list[Failure], root: Path, content_only: bool = True) -> int:
    """Print broken references grouped by source file and return an exit code (nonzero if any on-disk error).

    On-disk breaks are errors; external breaks are warnings with a trailing copy-paste URL list. Each break shows
    the greppable destination for the markdown, the exact built-HTML href, and clickable `path:line` locations. By
    default only breaks on authored `content/*.md` pages are shown; `content_only=False` adds generated API and
    localized pages. Groups sort by displayed path, so `content/` files lead:

        ERRORS -- 2 broken on-disk reference(s) across 1 file(s)

        content/features/semantic-bridge-metric-view-object-model.md
          built: _site/en/features/semantic-bridge-metric-view-object-model.html
          missing anchor  (x2)
            md grep: DatabricksMetricViewService.Load
            html:    ../../api/TabularEditor.SemanticBridge...DatabricksMetricViewService.html#..._Load_System_String_
            at:      _site/en/features/semantic-bridge-metric-view-object-model.html:120  ...:145
          missing file  (x3)
            md grep: Advanced-features
            html:    /Advanced-features
            at:      _site/en/features/semantic-bridge-metric-view-object-model.html:12  ...:30  ...:88

        WARNINGS -- 1 broken external reference(s) across 1 file(s)
        ...
        External URLs to verify:
          https://example.com/gone
    """
    errors: dict[str, list[tuple[Failure, list[int]]]] = {}
    warnings: dict[str, list[tuple[Failure, list[int]]]] = {}
    for failure in failures:
        is_error = failure.target.kind == "local" or failure.target.internal  # our own content vs third-party
        bucket = errors if is_error else warnings
        for source, lines in failure.sources.items():
            if content_only and map_to_source(source, root) is None:
                continue
            bucket.setdefault(source, []).append((failure, sorted(lines)))

    if not errors and not warnings:
        print("No broken references found.")
        return 0

    for label, bucket in (("ERRORS", errors), ("WARNINGS", warnings)):
        if not bucket:
            continue
        kind = "internal" if label == "ERRORS" else "external"
        total = sum(len(breaks) for breaks in bucket.values())
        print(f"{label} -- {total} broken {kind} reference(s) across {len(bucket)} file(s)")
        for source in sorted(bucket, key=lambda s: map_to_source(s, root) or s):
            md = map_to_source(source, root)
            print(f"\n{md or source}")
            print(f"  built: {source}" if md else "  (generated or localized page; no direct .md source)")
            for failure, lines in sorted(bucket[source], key=lambda fl: (fl[0].reason, fl[0].target.resource)):
                # A missing file makes any fragment/text directive moot, so drop it from what we display.
                target = failure.target
                if failure.reason == "missing file":
                    target = target._replace(fragment="", text_targets=())
                locations = "  ".join(f"{source}:{line}" for line in lines)
                print(f"  {failure.reason}  (x{len(lines)})")
                print(f"    md grep: {humanize(target)}")
                print(f"    html:    {_display_url(target)}{_fragment_suffix(target)}")
                print(f"    at:      {locations}")
        print()

    if warnings:
        urls = {_display_url(failure.target) for breaks in warnings.values() for failure, _ in breaks}
        print("External URLs to verify:")
        for url in sorted(urls):
            print(url)

    return 1 if errors else 0


def print_diagnostics(stats: dict[str, HostStats], elapsed: float) -> None:
    """Print per-host fetch diagnostics: requests, 429s, cooldown time, HEAD fallbacks, final cap, Retry-After set."""
    active = {host: stat for host, stat in stats.items() if stat.requests}
    print(f"\n--- fetch diagnostics ({elapsed:.1f}s, {len(active)} hosts) ---")
    print(f"{'reqs':>5} {'429s':>5} {'wait(s)':>8} {'fb':>4} {'cap':>4}  host  [retry-after seen]")
    ranked = sorted(active.items(), key=lambda kv: (kv[1].rate_limited, kv[1].wait_seconds), reverse=True)
    for host, stat in ranked:
        seen = sorted(stat.retry_after_seen)
        tail = f"  {seen}" if stat.rate_limited else ""
        print(f"{stat.requests:>5} {stat.rate_limited:>5} {stat.wait_seconds:>8.1f} "
              f"{stat.head_fallbacks:>4} {stat.final_cap:>4}  {host}{tail}")


def cmd_validate(args: list[str]) -> int:
    """Validate a built site and report broken references.

    Usage: validate [root] [local] [all] [stats] [under=<subpath>]
      local           skip external fetching (on-disk checks only)
      all             include generated API and localized pages (default: authored content/*.md only)
      stats           print per-host fetch diagnostics
      under=<subpath> check only links from pages under root/<subpath> (anchors are still indexed site-wide)
    """
    flags = {arg for arg in args if arg in ("local", "all", "stats")}
    under = next((arg[len("under=") :] for arg in args if arg.startswith("under=")), None)
    positional = [arg for arg in args if arg not in flags and not arg.startswith("under=")]
    root = Path(positional[0]) if positional else Path("_site")
    source_prefix = os.path.normpath(root / under) if under else None

    refs, anchors_by_file = enumerate_site(root, source_prefix)
    existing = _existing_files(root)
    refs = resolve_site_targets(refs, existing, root, live="local" not in flags)
    stats: dict[str, HostStats] = {}
    started = monotonic()
    if "local" in flags:
        refs = {target: sources for target, sources in refs.items() if target.kind == "local"}
        external: dict[str, FetchResult] = {}
    else:
        external, stats = fetch_all_external(refs)
    elapsed = monotonic() - started

    exit_code = report(validate(refs, anchors_by_file, existing, external), root, content_only="all" not in flags)
    if "stats" in flags:
        print_diagnostics(stats, elapsed)
    return exit_code


COMMANDS = {
    "extract": cmd_extract,
    "resolve": cmd_resolve,
    "enumerate": cmd_enumerate,
    "fetch": cmd_fetch,
    "validate": cmd_validate,
}


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: {Path(sys.argv[0]).name} <{'|'.join(COMMANDS)}> [args]", file=sys.stderr)
        return 2
    return COMMANDS[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
