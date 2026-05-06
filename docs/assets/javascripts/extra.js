/**
 * OBiBa Custom JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log('OBiBa MkDocs site loaded');
  
  // Add any custom JavaScript functionality here
  
  // Example: External link handling
  const links = document.querySelectorAll('a[href^="http"]');
  links.forEach(link => {
    if (!link.href.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });
});
