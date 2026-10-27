"""
Block segmentation and block-level diff of Markdown bodies for translate-content.py.

A body (Markdown without frontmatter, LF line endings) is split into blocks: a blank line ends
a block; a heading, thematic break or table row is a block of its own; a list item, a `> [!` alert, a fenced
code block and an HTML comment start a new block. Blank lines after a block are kept verbatim
in its `gap`, so `join(segment(body))` returns the body unchanged.

Two segmentations align when their block kinds are identical in order. A translation that was
written from English version O aligns with O, so the blocks of a newer English version N are
produced from three sources: the translated block of O (unchanged or moved text), a new
translation (changed or inserted text) or the English block itself (untranslatable text).
"""

from __future__ import annotations

import difflib
import hashlib
import re
from collections.abc import Callable
from dataclasses import dataclass

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^#{1,6}\s+\S")
RULE_RE = re.compile(r"^ {0,3}([-*_])(?:[ \t]*\1){2,}[ \t]*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TABLE_ROW_RE = re.compile(r"^\s*\|")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*$")
ALERT_START_RE = re.compile(r"^\s*>\s*\[!")
COMMENT_START_RE = re.compile(r"^\s*<!--")
INCLUDE_LINE_RE = re.compile(r"^\s*\[!(?:include|code-[\w-]+)\[[^\]\n]*\]\([^)\n]*\)\]\s*$")
ALT_TEXT_RE = re.compile(r"""\b(?:alt|title)\s*=\s*["']([^"']*)["']""")
# Removed before deciding whether a block has text to translate: inline code, link targets,
# HTML tags, bare URLs, alert/include markers and @uid cross-references.
UNTRANSLATABLE_SPAN_RE = re.compile(
    r"`+[^`\n]*?`+|\]\([^)\s]*\)|<[^>\n]*>|https?://\S+|\[![A-Za-z][A-Za-z0-9-]*|(?<![\w@])@[A-Za-z0-9_.\-/#]+"
)

KIND_HEADING = "h"
KIND_RULE = "hr"
KIND_LIST_ITEM = "li"
KIND_TABLE_ROW = "tr"
KIND_ALERT = "alert"
KIND_COMMENT = "comment"
KIND_FENCE = "fence"
KIND_PARAGRAPH = "p"

ACTION_REUSE = "reuse"
ACTION_REPAIR = "repair"  # reuse, with code/markers/link targets restored from the new English
ACTION_TRANSLATE = "translate"
ACTION_ENGLISH = "english"
REUSED = (ACTION_REUSE, ACTION_REPAIR)


@dataclass
class Block:
    kind: str
    text: str
    gap: str = ""

    @property
    def key(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()

    @property
    def translatable(self) -> bool:
        if self.kind in (KIND_FENCE, KIND_COMMENT):
            return False
        lines = [line for line in self.text.splitlines() if line.strip()]
        if self.kind == KIND_TABLE_ROW and all(TABLE_SEPARATOR_RE.match(line) for line in lines):
            return False
        if all(INCLUDE_LINE_RE.match(line) for line in lines):
            return False
        visible = UNTRANSLATABLE_SPAN_RE.sub(" ", self.text) + " ".join(ALT_TEXT_RE.findall(self.text))
        return any(c.isalpha() for c in visible)


@dataclass
class Segmented:
    lead: str
    blocks: list[Block]

    @property
    def kinds(self) -> list[str]:
        return [b.kind for b in self.blocks]

    def join(self, texts: list[str] | None = None, gaps: list[str] | None = None, lead: str | None = None) -> str:
        """The body; `texts`, `gaps` and `lead` replace the blocks' texts, gaps and the lead."""
        texts = [b.text for b in self.blocks] if texts is None else texts
        gaps = [b.gap for b in self.blocks] if gaps is None else gaps
        lead = self.lead if lead is None else lead
        return lead + "".join(text + gap for text, gap in zip(texts, gaps, strict=True))


def segment(body: str) -> Segmented:
    lead = ""
    blocks: list[Block] = []
    cur: list[str] = []
    cur_kind = ""
    in_fence = False
    in_comment = False

    def flush() -> None:
        nonlocal cur, cur_kind
        if cur:
            blocks.append(Block(cur_kind, "".join(cur)))
        cur = []
        cur_kind = ""

    def start(kind: str, line: str) -> None:
        nonlocal cur, cur_kind
        flush()
        cur = [line]
        cur_kind = kind

    for line in body.splitlines(keepends=True):
        if in_fence:
            cur.append(line)
            if FENCE_RE.match(line):
                in_fence = False
                flush()
            continue
        if in_comment:
            cur.append(line)
            if "-->" in line:
                in_comment = False
                flush()
            continue
        if not line.strip():
            flush()
            if blocks:
                blocks[-1].gap += line
            else:
                lead += line
            continue
        if FENCE_RE.match(line):
            start(KIND_FENCE, line)
            in_fence = True
        elif COMMENT_START_RE.match(line):
            start(KIND_COMMENT, line)
            if "-->" in line:
                flush()
            else:
                in_comment = True
        elif HEADING_RE.match(line):
            start(KIND_HEADING, line)
            flush()
        elif RULE_RE.match(line):
            start(KIND_RULE, line)
            flush()
        elif TABLE_ROW_RE.match(line):
            start(KIND_TABLE_ROW, line)
            flush()
        elif LIST_ITEM_RE.match(line):
            start(KIND_LIST_ITEM, line)
        elif ALERT_START_RE.match(line):
            start(KIND_ALERT, line)
        elif cur:
            cur.append(line)
        else:
            start(KIND_PARAGRAPH, line)
    flush()
    return Segmented(lead, blocks)


@dataclass(frozen=True)
class Action:
    kind: str
    old_index: int = -1


def diff_blocks(old: list[Block], new: list[Block], prose_key: Callable[[str], str] | None = None) -> list[Action]:
    """One action per new block. Equal runs reuse the aligned old block; a changed or inserted
    block whose exact text exists elsewhere in the old version (a move) reuses that block; inside
    a replaced run, a block whose `prose_key` matches an old block of the same kind in the run
    (only code, link targets, the list number or the heading level changed) is reused with repair; any other
    untranslatable block (code, comment, table separator) is taken from the English."""
    first_index: dict[str, int] = {}
    for i, b in enumerate(old):
        first_index.setdefault(b.key, i)
    matcher = difflib.SequenceMatcher(None, [b.key for b in old], [b.key for b in new], autojunk=False)
    actions: list[Action] = [Action(ACTION_TRANSLATE)] * len(new)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        for j in range(j1, j2):
            if tag == "equal":
                actions[j] = Action(ACTION_REUSE, i1 + (j - j1))
            elif new[j].key in first_index:
                actions[j] = Action(ACTION_REUSE, first_index[new[j].key])
        if tag != "replace" or prose_key is None:
            continue
        runs = difflib.SequenceMatcher(
            None, [prose_key(b.text) for b in old[i1:i2]], [prose_key(b.text) for b in new[j1:j2]], autojunk=False
        )
        for sub_tag, a1, _a2, b1, b2 in runs.get_opcodes():
            if sub_tag != "equal":
                continue
            for k in range(b2 - b1):
                i, j = i1 + a1 + k, j1 + b1 + k
                if actions[j].kind == ACTION_TRANSLATE and new[j].translatable and old[i].kind == new[j].kind:
                    actions[j] = Action(ACTION_REPAIR, i)
    return [
        Action(ACTION_ENGLISH) if a.kind == ACTION_TRANSLATE and not b.translatable else a
        for a, b in zip(actions, new, strict=True)
    ]


def reused_layout(actions: list[Action], new: Segmented, old_count: int, loc: Segmented) -> tuple[str, list[str]]:
    """(lead, gaps) for the rebuilt body: the translation's blank lines between two blocks that
    are both reused in their old order (and before the first / after the last), else the English."""
    gaps: list[str] = []
    for j, (a, b) in enumerate(zip(actions, new.blocks, strict=True)):
        nxt = actions[j + 1] if j + 1 < len(actions) else None
        follows = (nxt is None and a.old_index == old_count - 1) or (
            nxt is not None and nxt.kind in REUSED and nxt.old_index == a.old_index + 1
        )
        gaps.append(loc.blocks[a.old_index].gap if a.kind in REUSED and follows else b.gap)
    starts_reused = bool(actions) and actions[0].kind in REUSED and actions[0].old_index == 0
    return (loc.lead if starts_reused or not actions else new.lead), gaps


def context_indices(actions: list[Action], blocks: list[Block], width: int) -> list[int]:
    """Indices of up to `width` translatable, unchanged blocks on each side of every changed block;
    a negative width selects every translatable, unchanged block (the whole page as context)."""
    changed = {j for j, a in enumerate(actions) if a.kind == ACTION_TRANSLATE}
    if width == 0 or not changed:
        return []
    if width < 0:
        return [k for k, b in enumerate(blocks) if k not in changed and b.translatable]
    picked: set[int] = set()
    for j in changed:
        for step in (-1, 1):
            k, taken = j + step, 0
            while 0 <= k < len(blocks) and taken < width:
                if k not in changed and blocks[k].translatable:
                    picked.add(k)
                    taken += 1
                k += step
    return sorted(picked)
