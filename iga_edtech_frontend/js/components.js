/**
 * Iga EdTech — Shared Components
 * Navbar and footer inject into every page.
 * Globe button toggles EN ↔ RW via i18n.js.
 */

// ── Path detection ────────────────────────────────────────────────────────────
const _path     = window.location.pathname;
const isSubPage = _path.includes('/pages/');
const isIndex   = _path === '/' || _path.endsWith('index.html');
const rootPath  = isSubPage ? '../' : './';
const pagesPath = isSubPage ? './'  : './pages/';
const isTeacher = _path.includes('teacher');

// ── Theme colors ──────────────────────────────────────────────────────────────
const BRAND       = isTeacher ? '#10B981' : '#2563EB';
const BRAND_DARK  = isTeacher ? '#3d6b4d' : '#1d4ed8';
const BRAND_LIGHT = isTeacher ? 'rgba(82,134,97,0.08)' : 'rgba(37,99,235,0.05)';

function injectTheme() {
  const existing = document.getElementById('iga-theme');
  if (existing) existing.remove();
  const style = document.createElement('style');
  style.id = 'iga-theme';
  style.textContent = `
    :root {
      --brand:       ${BRAND};
      --brand-dark:  ${BRAND_DARK};
      --brand-light: ${BRAND_LIGHT};
    }
    .btn-submit           { background: ${BRAND} !important; }
    .btn-submit:hover     { background: ${BRAND_DARK} !important; }
    .btn-nav.active       { background: ${BRAND} !important; border-color: ${BRAND} !important; color: #fff !important; }
    .switch-box a         { color: ${BRAND} !important; }
    .input-field:focus    { border-color: ${BRAND} !important; box-shadow: 0 0 0 3px ${BRAND_LIGHT} !important; }
    .logo .ed             { color: ${BRAND} !important; }
    .footer-logo .ed      { color: ${BRAND} !important; }
  `;
  document.head.appendChild(style);
}

// ── Navbar ────────────────────────────────────────────────────────────────────
function getNavbar() {
  const onTeacherLogin    = _path.includes('teacher-login');
  const onTeacherRegister = _path.includes('teacher-register');
  const onStudentLogin    = _path.includes('login')    && !isTeacher;
  const onStudentRegister = _path.includes('register') && !isTeacher;
  const loginHref         = isTeacher ? `${pagesPath}teacher-login.html`    : `${pagesPath}login.html`;
  const signupHref        = isTeacher ? `${pagesPath}teacher-register.html` : `${pagesPath}register.html`;
  const onLogin           = isTeacher ? onTeacherLogin    : onStudentLogin;
  const onRegister        = isTeacher ? onTeacherRegister : onStudentRegister;
  const showJourneyText   = !isIndex;

  return `
    <nav class="navbar">
      <div class="navbar-left">
        <a href="${rootPath}index.html" class="logo">Iga <span class="ed">Ed</span>Tech</a>
      </div>
      <div class="navbar-right">
        ${showJourneyText ? `<span class="nav-journey" data-i18n="nav.journey">Start the journey</span>` : ''}
        <button class="btn-nav ${onLogin ? 'active' : ''}"
                onclick="window.location.href='${loginHref}'"
                data-i18n="nav.login">Login</button>
        <button class="btn-nav ${onRegister ? 'active' : ''}"
                onclick="window.location.href='${signupHref}'"
                data-i18n="nav.signup">Sign Up</button>
        <div id="langToggleBtn"
             onclick="toggleLang()"
             title="Switch language"
             style="cursor:pointer;display:inline-flex;align-items:center;gap:5px;
                    padding:5px 12px;border-radius:20px;
                    border:1.5px solid #e2e8f0;background:#fff;
                    font-size:12px;font-weight:700;color:#475569;
                    line-height:1;white-space:nowrap;flex-shrink:0;
                    font-family:'DM Sans',sans-serif;
                    transition:border-color .15s,color .15s;">
          <i class="fa-solid fa-globe" style="font-size:13px;"></i>
          <span id="langLabel">EN</span>
        </div>
      </div>
    </nav>`;
}

// ── Footer ────────────────────────────────────────────────────────────────────
function getFooter() {
  return `
    <footer class="site-footer">
      <div class="footer-grid">
        <div class="footer-col">
          <h4 data-i18n="footer.learn">Learn</h4>
          <a href="${pagesPath}student-dashboard.html" data-i18n="footer.courses">Courses</a>
          <a href="${pagesPath}student-dashboard.html" data-i18n="footer.assessment">Assessment</a>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.contact">Contact Us On</h4>
          <p>Tel: +0 123 456 789</p>
          <p>iga_learn@gmail.com</p>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.terms">Terms</h4>
          <a href="#" data-i18n="footer.privacy">Privacy Policy</a>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.socials">Socials</h4>
          <div class="footer-socials">
            <div class="social-btn"><i class="fa-brands fa-linkedin-in"></i></div>
            <div class="social-btn"><i class="fa-brands fa-instagram"></i></div>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span class="footer-logo">
          <span class="rest">Iga </span><span class="ed">Ed</span><span class="rest">Tech</span>
        </span>
        <span class="footer-copy" data-i18n="footer.rights">© 2026 Iga EdTech || All rights reserved.</span>
        <div class="footer-lang-btn" onclick="toggleLang()"
             style="cursor:pointer;display:flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--brand,#2563EB);">
          <i class="fa-solid fa-globe"></i>
          <span id="footerLangLabel">EN</span>
        </div>
      </div>
    </footer>`;
}

// ── Font Awesome ──────────────────────────────────────────────────────────────
function injectFontAwesome() {
  if (!document.getElementById('fa-cdn')) {
    const link = document.createElement('link');
    link.id  = 'fa-cdn'; link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css';
    document.head.appendChild(link);
  }
}

// ── Update language label in navbar + footer ──────────────────────────────────
function _updateLangLabel() {
  const lang  = (typeof getLang === 'function') ? getLang() : (localStorage.getItem('iga_lang') || 'en');
  const label = lang === 'en' ? 'EN' : 'RW';
  const nav   = document.getElementById('langLabel');
  const foot  = document.getElementById('footerLangLabel');
  if (nav)  nav.textContent  = label;
  if (foot) foot.textContent = label;
}

// ── Inject everything ─────────────────────────────────────────────────────────
function injectComponents() {
  injectFontAwesome();
  injectTheme();
  const navEl    = document.getElementById('navbar-placeholder');
  const footerEl = document.getElementById('footer-placeholder');
  if (navEl)    navEl.innerHTML    = getNavbar();
  if (footerEl) footerEl.innerHTML = getFooter();

  // Hover effect for lang toggle (can't use :hover on inline style)
  const langBtn = document.getElementById('langToggleBtn');
  if (langBtn) {
    langBtn.addEventListener('mouseenter', () => {
      langBtn.style.borderColor = 'var(--brand, #2563EB)';
      langBtn.style.color       = 'var(--brand, #2563EB)';
    });
    langBtn.addEventListener('mouseleave', () => {
      langBtn.style.borderColor = '#e2e8f0';
      langBtn.style.color       = '#475569';
    });
  }

  // Apply translations if i18n.js is loaded
  if (typeof applyLang === 'function') applyLang();
  _updateLangLabel();
}

// ── Redirect helper ───────────────────────────────────────────────────────────
function redirectToDashboard(role) {
  const dashMap = {
    student: `${rootPath}pages/student-dashboard.html`,
    teacher: `${rootPath}pages/teacher-dashboard.html`,
    admin:   `${rootPath}pages/admin-dashboard.html`,
  };
  window.location.href = dashMap[role] || `${rootPath}pages/student-dashboard.html`;
}

// Patch setLang to also update the label whenever language changes
const _origSetLang = typeof setLang !== 'undefined' ? setLang : null;
function _patchedLangUpdate() { _updateLangLabel(); }
// Hook in after i18n.js runs (i18n.js defines setLang, components.js calls injectComponents)
document.addEventListener('iga-lang-changed', _patchedLangUpdate);

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectComponents);
} else {
  injectComponents();
}