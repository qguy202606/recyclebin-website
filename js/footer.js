/* footer.js - shared footer year fallback when _footer.html is used */
(function () {
  'use strict';
  try {
    var el = document.getElementById('footerYear');
    if (el) el.textContent = new Date().getFullYear();
  } catch (e) {}
})();
