/* site.js - shared behavior for all pages */
(function () {
  'use strict';

  function getActive() {
    var p = location.pathname.replace(/\\/g, '/');
    if (p === '/' || p === '/index.html') return 'home';
    if (p.indexOf('/guides') !== -1) return 'guides';
    if (p.indexOf('/centers') !== -1) return 'centers';
    if (p.indexOf('/events') !== -1) return 'events';
    if (p.indexOf('/howto') !== -1) return 'howto';
    return '';
  }

  function loadHeader() {
    var el = document.getElementById('site-header');
    if (!el) return;
    fetch('./_header.html', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.text() : ''; })
      .then(function (html) {
        el.innerHTML = html;
        var active = getActive();
        var map = { home: 'home', guides: 'guides', centers: 'centers', events: 'events', howto: 'howto' };
        var key = map[active];
        if (key) {
          var link = el.querySelector('[data-nav="' + key + '"]');
          if (link) link.classList.add('active');
        }
        initMobileNav(el);
        initLangToggle(el);
      });
  }

  function loadFooter() {
    var el = document.getElementById('site-footer');
    if (!el) return;
    fetch('./_footer.html', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.text() : ''; })
      .then(function (html) { el.innerHTML = html; });
  }

  function initMobileNav(root) {
    root = root || document;
    var toggle = root.getElementById('navToggle');
    var links = root.querySelector('.nav-links');
    if (!toggle || !links) return;
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      links.classList.toggle('open');
      toggle.textContent = links.classList.contains('open') ? '✕' : '☰';
    });
    root.addEventListener('click', function (e) {
      if (!links.contains(e.target) && e.target !== toggle) {
        links.classList.remove('open');
        toggle.textContent = '☰';
      }
    });
  }

  function initLangToggle(root) {
    var btn = root.querySelector('[data-i18n-toggle]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      if (window.__recyclebinI18n && typeof window.__recyclebinI18n.toggle === 'function') {
        window.__recyclebinI18n.toggle();
      }
    });
  }

  window.RecycleBin = {
    loadHeader: loadHeader,
    loadFooter: loadFooter,
    initMobileNav: initMobileNav,
    initLangToggle: initLangToggle
  };
})();
