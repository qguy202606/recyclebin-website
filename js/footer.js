(() => {
  const mount = (id, src) => {
    const root = document.getElementById(id);
    if (!root) return;
    fetch(src, { cache: 'no-store' })
      .then((r) => (r.ok ? r.text() : Promise.reject(r.status)))
      .then((html) => {
        root.innerHTML = html;
        const year = root.querySelector('.footer-year');
        if (year) year.textContent = new Date().getFullYear().toString();
      })
      .catch(() => {});
  };

  document.addEventListener('DOMContentLoaded', () => {
    mount('site-footer', './_footer.html');
  });
})();
