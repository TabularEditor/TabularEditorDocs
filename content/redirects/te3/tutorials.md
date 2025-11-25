---
_disableToc: true
_disableContribution: true
---

<script>
    // Redirect old tutorials to new location
    (function() {
        var path = window.location.pathname;
        var hash = window.location.hash;
        var search = window.location.search;
        
        // Replace old path with new path
        var newPath = path.replace('/te3/tutorials/', '/tutorials/');
        
        // If it's just the base path, redirect to main tutorials
        if (newPath === '/te3/tutorials' || newPath === '/te3/tutorials.html') {
            newPath = '/tutorials/';
        }
        
        // Perform the redirect
        window.location.replace(newPath + search + hash);
    })();
</script>

# Redirecting

This page has moved to the tutorials section.
