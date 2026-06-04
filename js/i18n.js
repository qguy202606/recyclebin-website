(() => {
  const KEY = 'recyclebin.lang';
  const DEFAULT_LANG = 'en';
  const SUPPORTED_LANGUAGES = ['en', 'zh'];

  const parseQueryLang = () => {
    const params = new URLSearchParams(window.location.search);
    const raw = (params.get('lang') || '').trim().toLowerCase();
    return SUPPORTED_LANGUAGES.includes(raw) ? raw : null;
  };

  const getStoredLang = () => {
    try {
      const stored = localStorage.getItem(KEY);
      return SUPPORTED_LANGUAGES.includes(stored) ? stored : DEFAULT_LANG;
    } catch {
      return DEFAULT_LANG;
    }
  };

  const resolveLang = () => parseQueryLang() || getStoredLang();

  const setLang = (lang) => {
    try {
      localStorage.setItem(KEY, lang);
    } catch {
      // ignore storage errors
    }
  };

  const setQueryLang = (lang) => {
    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    window.history.replaceState({}, '', url);
  };

  const updateHtmlLang = (lang) => {
    document.documentElement.setAttribute('lang', lang);
  };

  const apply = (lang) => {
    updateHtmlLang(lang);
    setLang(lang);
    setQueryLang(lang);
    updateTranslatables(lang);
    updateToggleButton(lang);
  };

  const toggle = () => {
    const current = resolveLang();
    const next = current === 'en' ? 'zh' : 'en';
    apply(next);
  };

  const dictionary = {
    en: {
      'nav.guides': 'Guides',
      'nav.centers': 'Centers',
      'nav.events': 'Events',
      'nav.howto': 'How-To',
      'nav.games': 'Games',
      'home.backToHome': 'Back to Home',
      'events.comingSoon': 'Community events coming soon.'
    },
    zh: {
      'nav.guides': '回收指南',
      'nav.centers': '回收中心',
      'nav.events': '活動',
      'nav.howto': '教學環節',
      'nav.games': '遊戲',
      'home.backToHome': '返回首頁',
      'events.comingSoon': '社區活動即將推出。'
    }
  };

  const translate = (lang, text) => (dictionary[lang] && dictionary[lang][text]) || text;

  const updateTranslatables = (lang) => {
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      el.textContent = translate(lang, key);
    });
  };

  const updateToggleButton = (lang) => {
    document.querySelectorAll('[data-i18n-toggle]').forEach((btn) => {
      btn.textContent = lang === 'en' ? '中文' : 'EN';
      btn.setAttribute('aria-pressed', lang === 'zh' ? 'true' : 'false');
    });
  };

  document.addEventListener('DOMContentLoaded', () => {
    const lang = resolveLang();
    apply(lang);

    document.querySelectorAll('[data-i18n-toggle]').forEach((btn) => {
      btn.addEventListener('click', () => toggle());
    });
  });

  window.__recyclebinI18n = {
    resolveLang,
    toggle,
    apply,
    updateTranslatables,
    updateToggleButton
  };
})();
