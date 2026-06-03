(() => {
  const mount = (id, src) => {
    const root = document.getElementById(id);
    if (!root) return;
    fetch(src, { cache: 'no-store' })
      .then((r) => (r.ok ? r.text() : Promise.reject(r.status)))
      .then((html) => {
        root.innerHTML = html;
        if (id === 'site-header') initHeader(root);
      })
      .catch(() => {});
  };

  const initHeader = (root) => {
    const current = location.pathname.split('/').pop() || 'index.html';
    const links = root.querySelectorAll('[data-nav]');
    links.forEach((a) => {
      const nav = a.getAttribute('data-nav');
      a.classList.toggle('active', nav && `${nav}.html` === current);
    });

    const toggle = root.querySelector('.nav-toggle, [aria-label="Menu"]');
    const menu = root.querySelector('.nav-links');
    if (!toggle || !menu) return;
    toggle.addEventListener('click', () => menu.classList.toggle('open'));
    menu.addEventListener('click', (e) => {
      if (e.target.tagName === 'A') menu.classList.remove('open');
    });
  };

  const initFooter = (root) => {
    const year = root.querySelector('.footer-year');
    if (year) year.textContent = new Date().getFullYear().toString();
  };

  document.addEventListener('DOMContentLoaded', () => {
    mount('site-header', './_header.html');
    mount('site-footer', './_footer.html');
  });
})();
