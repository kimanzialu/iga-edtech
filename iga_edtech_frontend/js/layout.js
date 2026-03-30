/**
 * Shared dashboard layout helpers
 * Used by student-dashboard.html and teacher-dashboard.html
 */

function buildSidebar(navItems, activeKey) {
  const user = Auth.getUser();
  const initials = user ? user.full_name.split(' ').map(w=>w[0]).join('').toUpperCase().slice(0,2) : 'KI';

  const navHTML = navItems.map(n => `
    <button class="nav-item ${n.key===activeKey?'active':''}"
            data-key="${n.key}"
            onclick="switchSection('${n.key}',this)">
      ${n.label}
    </button>`).join('');

  return `
    <aside class="sidebar">
      <div class="sidebar-logo">Iga EdTech</div>
      <nav class="sidebar-nav">${navHTML}</nav>
      <div class="sidebar-footer">
        <div class="sidebar-user">
          <div class="sidebar-avatar" id="sidebarAvatar">${initials}</div>
          <div>
            <div class="sidebar-user-name" id="sidebarName">${user ? user.full_name : 'User'}</div>
            <div class="sidebar-user-role">${user ? (user.role.charAt(0).toUpperCase()+user.role.slice(1)) : ''}</div>
          </div>
          <span class="sidebar-logout" onclick="handleLogout()">↩</span>
        </div>
      </div>
    </aside>`;
}

function buildTopbar(breadcrumb, heading, userInitials) {
  return `
    <div class="main-topbar">
      <div>
        <div class="topbar-breadcrumb" id="topbarBreadcrumb">${breadcrumb}</div>
        <div class="topbar-heading" id="topbarHeading">${heading}</div>
      </div>
      <div class="topbar-right">
        <span class="topbar-bell">🔔</span>
        <div class="topbar-avatar" id="topbarAvatar">${userInitials}</div>
      </div>
    </div>`;
}

function updateTopbar(breadcrumb, heading) {
  const bc = document.getElementById('topbarBreadcrumb');
  const h  = document.getElementById('topbarHeading');
  if (bc) bc.textContent = breadcrumb;
  if (h)  h.textContent  = heading;
}
