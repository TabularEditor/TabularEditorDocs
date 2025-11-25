---
_disableToc: true
_disableContribution: true
---

<script>
    // Redirect old release notes to new location
    (function() {
        var path = window.location.pathname;
        var hash = window.location.hash;
        var search = window.location.search;
        
        // Replace old path with new path
        var newPath = path.replace('/te3/other/release-notes/', '/references/release-notes/');
        
        // If it's just the base path, redirect to main release notes
        if (newPath === '/te3/other/release-notes' || newPath === '/te3/other/release-notes.html') {
            newPath = '/references/release-notes/';
        }
        
        // Perform the redirect
        window.location.replace(newPath + search + hash);
    })();
</script>

# Redirecting...

This page has moved. If you are not redirected automatically, [click here](/references/release-notes/).
