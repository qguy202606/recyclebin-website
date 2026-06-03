(function() {
  var page = location.pathname.split('/').pop() || 'index.html';

  function highlight() {
    var links = document.querySelectorAll('.menu-link');
    links.forEach(function(a) {
      var href = a.getAttribute('href') || '';
      a.classList.toggle('active', href && href.indexOf(page) > -1);
    });
  }

  highlight();

  if (window.MutationObserver) {
    new MutationObserver(highlight).observe(document.body, { childList: true, subtree: true });
  }
})();
