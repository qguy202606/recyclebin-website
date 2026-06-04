/* site.js - shared layout, i18n toggle, mobile nav, dark mode */
(() => {
  'use strict';

  const applyI18nLang = (lang, root = document) => {
    root.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (!key) return;
      const text = (window.__recyclebinI18n &&
        window.__recyclebinI18n.translate &&
        window.__recyclebinI18n.translate(lang, key)) || key;
      el.textContent = text;
    });
    root.querySelectorAll('[data-i18n-toggle]').forEach((btn) => {
      btn.textContent = lang === 'en' ? '中文' : 'EN';
      btn.setAttribute('aria-pressed', lang === 'zh' ? 'true' : 'false');
    });
  };

  const toggleLang = () => {
    let next = 'zh';
    if (window.__recyclebinI18n) {
      const current = window.__recyclebinI18n.resolveLang ? window.__recyclebinI18n.resolveLang() : null;
      next = (current === 'en') ? 'zh' : 'en';
    }
    if (window.__recyclebinI18n && typeof window.__recyclebinI18n.apply === 'function') {
      window.__recyclebinI18n.apply(next);
    }
    applyI18nLang(next);
  };

  const getActive = () => {
    const p = location.pathname.replace(/\\/g, '/');
    if (p === '/' || p === '/index.html') return 'home';
    if (p.indexOf('/guides') !== -1) return 'guides';
    if (p.indexOf('/centers') !== -1) return 'centers';
    if (p.indexOf('/events') !== -1) return 'events';
    if (p.indexOf('/howto') !== -1) return 'howto';
    if (p.indexOf('/games') !== -1) return 'games';
    return '';
  };

  const loadHeader = (root = document) => {
    const el = root.getElementById('site-header');
    if (!el) return;
    fetch('./_header.html', { cache: 'no-store' })
      .then((r) => r.ok ? r.text() : '')
      .then((html) => {
        el.innerHTML = html;
        const active = getActive();
        const map = { home: 'home', guides: 'guides', centers: 'centers', events: 'events', howto: 'howto', games: 'games' };
        const key = map[active];
        if (key) {
          const link = el.querySelector('[data-nav="' + key + '"]');
          if (link) link.classList.add('active');
        }
        initMobileNav(el);
        initLangToggle(el);
        const lang = (window.__recyclebinI18n && window.__recyclebinI18n.resolveLang && window.__recyclebinI18n.resolveLang()) || 'en';
        applyI18nLang(lang, el);
      });
  };

  const loadFooter = (root = document) => {
    const el = root.getElementById('site-footer');
    if (!el) return;
    fetch('./_footer.html', { cache: 'no-store' })
      .then((r) => r.ok ? r.text() : '')
      .then((html) => el.innerHTML = html);
  };

  const initMobileNav = (root = document) => {
    const toggle = root.getElementById('navToggle');
    const links = root.querySelector('.nav-links');
    if (!toggle || !links) return;
    const open = () => {
      links.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.textContent = '✕';
    };
    const close = () => {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = '☰';
    };
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      links.classList.contains('open') ? close() : open();
    });
    const doc = root === document ? root : document;
    doc.addEventListener('click', (e) => {
      if (!links.contains(e.target) && e.target !== toggle) close();
    });
  };

  const initLangToggle = (root = document) => {
    const btn = root.querySelector('[data-i18n-toggle]');
    if (!btn) return;
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      toggleLang();
    });
  };

  const applyDark = (enabled) => {
    document.documentElement.setAttribute('data-theme', enabled ? 'dark' : 'light');
    try { localStorage.setItem('recyclebin.theme', enabled ? 'dark' : 'light'); } catch {}
  };

  const toggleDark = () => {
    const enabled = document.documentElement.getAttribute('data-theme') !== 'dark';
    applyDark(enabled);
  };

  const initDark = () => {
    const btn = document.querySelector('[data-theme-toggle]');
    if (btn) btn.addEventListener('click', () => toggleDark());
  };

  document.addEventListener('DOMContentLoaded', () => {
    loadHeader();
    loadFooter();
    initDark();
    const lang = (window.__recyclebinI18n && window.__recyclebinI18n.resolveLang && window.__recyclebinI18n.resolveLang()) || 'en';
    applyI18nLang(lang);
  });

  window.RecycleBin = {
    loadHeader,
    loadFooter,
    initMobileNav,
    initLangToggle,
    applyI18nLang,
    toggleDark,
    applyDark
  };
})();
