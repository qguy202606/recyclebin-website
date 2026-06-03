/**
 * Shared layout, navigation, and i18n for RecycleBin pages.
 * Classic script; attaches window.RecycleBin.
 */
(function(){
  'use strict';

  var prefix = '[recyclebin]';

  function getActivePage(){
    var path = location.pathname.replace(/\\/g,'/');
    if(path.indexOf('/events') !== -1) return 'events';
    if(path.indexOf('/guides') !== -1) return 'guides';
    if(path.indexOf('/centers') !== -1) return 'centers';
    if(path.indexOf('/howto') !== -1) return 'howto';
    if(path === '/' || path === '/index.html') return 'home';
    return '';
  }

  function loadHeader(){
    var headerTarget = document.getElementById('site-header');
    if(!headerTarget) return;
    fetch('./_header.html', {cache:'no-store'})
      .then(function(r){ if(!r.ok) throw new Error('header fetch failed'); return r.text(); })
      .then(function(html){
        headerTarget.innerHTML = html;
        setActiveNav(headerTarget);
        if(typeof initMobileNav === 'function') initMobileNav();
      })
      .catch(function(){ headerTarget.innerHTML = ''; });
  }

  function setActiveNav(root){
    var active = getActivePage();
    var map = {home:'home', guides:'guides', centers:'centers', events:'events', howto:'howto'};
    var key = map[active];
    if(!key) return;
    var link = (root || document).querySelector('[data-nav="'+key+'"]');
    if(link) link.classList.add('active');
    if(active === 'events'){
      var homeLink = (root || document).querySelector('[data-nav="home"]');
      if(homeLink && homeLink.parentElement) homeLink.parentElement.style.display = 'none';
    }
  }

  function loadFooter(){
    var footerTarget = document.getElementById('site-footer');
    if(!footerTarget) return;
    fetch('./_footer.html', {cache:'no-store'})
      .then(function(r){ if(!r.ok) throw new Error('footer fetch failed'); return r.text(); })
      .then(function(html){ footerTarget.innerHTML = html; })
      .catch(function(){ footerTarget.innerHTML = ''; });
  }

  function initMobileNav(){
    var root = document;
    var toggle = root.getElementById('navToggle');
    var linksEl = root.querySelector('.nav-links');
    if(!toggle || !linksEl) return;
    toggle.addEventListener('click', function(e){
      e.preventDefault();
      e.stopPropagation();
      linksEl.classList.toggle('open');
      toggle.textContent = linksEl.classList.contains('open') ? '✕' : '☰';
    });
    root.addEventListener('click', function(e){
      if(!linksEl.contains(e.target) && e.target !== toggle){
        linksEl.classList.remove('open');
        toggle.textContent = '☰';
      }
    });
  }

  function initLayout(opts){
    opts = opts || {};
    var footer = document.getElementById('site-footer');
    if(footer){
      footer.innerHTML = '<div class="container"><p>&copy; 2025 RecycleBin.com. All rights reserved.</p></div>';
    }
    var h1 = document.querySelector('.page-header h1');
    if(h1 && !h1.textContent.trim()){
      h1.textContent = document.title.replace('RecycleBin.com - ','');
    }
  }

  var I18N = {
    en: {
      nav_home:'Home', nav_guides:'Guides', nav_centers:'Centers', nav_events:'Events', nav_howto:'How-To',
      read_more:'Read More', start:'Start Learning', guides_back:'Back to Guides',
      event_back:'Back to Events', event_join:'Join Now',
      filter_state:'Filter by state:', filter_all:'All United States',
      status_loaded:'Events are loaded from an external provider.', status_none:'No events available.',
      centers_title:'Find a Recycling Center', centers_sub:'Find the nearest recycling drop-off locations.',
      geo_error:'Unable to detect location. Showing all centers.',
      detecting:'Detecting location...', loc_unknown:'Location unknown', loc_hint:'— enter a city to find centers',
      search_btn:'Search', reset_btn:'Show All',
      empty:'Content is being updated.', date:'Date',
      detail_title:'About this event', detail_body:'',
      back:'Back to Events', join:'Join Now'
    }
  };

  var currentLang = 'en';

  function getLang(){ return currentLang; }

  function t(key){
    var dict = I18N[currentLang] || I18N['en'];
    return dict[key] || I18N['en'][key] || key;
  }

  window.t = t;

  function setLanguage(lang){
    currentLang = lang;
    document.documentElement.lang = lang;
    try{ localStorage.setItem('recyclebin-lang', lang); }catch(e){}
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      var k = el.getAttribute('data-i18n');
      if(!k) return;
      var text = t(k);
      if(!text || text === k) return;
      if(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') el.value = text;
      else el.innerHTML = text;
    });
    var btn = document.getElementById('langToggle');
    if(btn) btn.textContent = lang === 'zh' ? '中' : 'EN';
  }

  function toggleLanguage(){
    var next = currentLang === 'en' ? 'zh' : 'en';
    setLanguage(next);
  }

  function initI18n(){
    var saved;
    try{ saved = localStorage.getItem('recyclebin-lang'); }catch(e){ saved = null; }
    if(saved === 'zh' || saved === 'en') setLanguage(saved);
    document.addEventListener('click', function(e){
      if(e.target && e.target.id === 'langToggle'){
        e.preventDefault();
        toggleLanguage();
      }
    });
  }

  function renderStateOptions(states){
    var sel = document.getElementById('stateSelect');
    if(!sel) return;
    sel.innerHTML = '';
    var allOpt = document.createElement('option');
    allOpt.value = 'ALL';
    allOpt.textContent = t('filter_all');
    sel.appendChild(allOpt);
    (states || []).forEach(function(s){
      var opt = document.createElement('option');
      opt.value = s; opt.textContent = s;
      sel.appendChild(opt);
    });
  }

  function setEventStatus(key){
    var el = document.getElementById('feed-status');
    if(!el) return;
    el.textContent = key ? (t(key) || key) : '';
  }

  function initSharedEvents(){
    var sel = document.getElementById('stateSelect');
    if(!sel) return;
    sel.addEventListener('change', function(){
      var ev = new CustomEvent('statefilter:change', {detail:{state: sel.value}});
      document.dispatchEvent(ev);
    });
  }

  function initSearch(inputId, panelId, indexUrl){
    if(!inputId || !panelId) return;
    var input = document.getElementById(inputId);
    var panel = document.getElementById(panelId);
    if(!input || !panel) return;
    function hide(){ panel.style.display='none'; panel.innerHTML=''; }
    function show(){ panel.style.display='block'; }
    function esc(s){ return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
    fetch(indexUrl, {cache:'no-store'})
      .then(function(r){ if(!r.ok) throw new Error('fail'); return r.json(); })
      .then(function(index){ window.__searchIndex = index || []; })
      .catch(function(){ window.__searchIndex = []; });
    input.addEventListener('input', function(){
      var q = (input.value||'').trim().toLowerCase();
      if(!q){ hide(); return; }
      var rows = (window.__searchIndex || []).filter(function(x){
        return (x.title||'').toLowerCase().indexOf(q)!==-1 || (x.desc||'').toLowerCase().indexOf(q)!==-1;
      });
      if(!rows.length){ panel.innerHTML='<div style=\"padding:14px 16px;color:#b0b0b0;font-size:14px;\">No results</div>'; show(); return; }
      panel.innerHTML = rows.slice(0,7).map(function(r){
        return '<a href=\"'+esc(r.url)+'\" style=\"display:flex;flex-direction:column;gap:2px;padding:12px 14px;text-decoration:none;color:#f3f3f3;border-bottom:1px solid #1c1c1c;\">' +
          '<div style=\"font-weight:600;font-size:14px;\">'+esc(r.title)+'</div>' +
          '<div style=\"font-size:13px;color:#a0a0a0;\">'+esc(r.desc||'')+'</div>' +
        '</a>';
      }).join('');
      show();
    });
    document.addEventListener('click', function(e){
      if(!panel.contains(e.target) && e.target !== input) hide();
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape') hide();
    });
  }

  function navigateTo(url){ window.location.href = url; }

  window.RecycleBin = {
    initLayout: initLayout,
    initI18n: initI18n,
    setLanguage: setLanguage,
    toggleLanguage: toggleLanguage,
    getLang: getLang,
    t: t,
    renderStateOptions: renderStateOptions,
    setEventStatus: setEventStatus,
    initSharedEvents: initSharedEvents,
    initSearch: initSearch,
    navigateTo: navigateTo,
    initMobileNav: initMobileNav,
    loadHeader: loadHeader,
    loadFooter: loadFooter
  };
})();
