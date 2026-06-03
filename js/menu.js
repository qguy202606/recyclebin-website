(function() {
  var page = location.pathname.split('/').pop() || 'index.html';
  var links = document.querySelectorAll('.menu-link');
  links.forEach(function(a) {
    var href = a.getAttribute('href') || '';
    a.classList.toggle('active', href && href.indexOf(page) > -1);
  });
})();
