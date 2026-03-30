
const API_BASE = 'http://127.0.0.1:5000';

const Auth = {
  getToken()       { return localStorage.getItem('iga_access_token'); },
  getRefresh()     { return localStorage.getItem('iga_refresh_token'); },
  getUser()        { try { return JSON.parse(localStorage.getItem('iga_user')); } catch { return null; } },
  setSession(data) {
    localStorage.setItem('iga_access_token',  data.access_token);
    localStorage.setItem('iga_refresh_token', data.refresh_token);
    localStorage.setItem('iga_user',          JSON.stringify(data.user));
  },
  clearSession() {
    ['iga_access_token','iga_refresh_token','iga_user'].forEach(k => localStorage.removeItem(k));
  },
  isLoggedIn() { return !!this.getToken() && !!this.getUser(); },
  getRole()    { return this.getUser()?.role || null; },
};

async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  const token   = Auth.getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  try {
    const res  = await fetch(`${API_BASE}${path}`, { ...options, headers });
    const json = await res.json().catch(() => ({}));

    if (res.status === 401 && Auth.getRefresh()) {
      const refreshed = await _tryRefresh();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${Auth.getToken()}`;
        const retry = await fetch(`${API_BASE}${path}`, { ...options, headers });
        return { ok: retry.ok, status: retry.status, data: await retry.json().catch(() => ({})) };
      } else {
        Auth.clearSession();
        window.location.href = window.location.pathname.includes('teacher') ? 'teacher-login.html' : 'login.html';
        return;
      }
    }
    return { ok: res.ok, status: res.status, data: json };
  } catch {
    return { ok: false, status: 0, data: { message: 'Cannot reach the server. Is the backend running?' } };
  }
}

async function _tryRefresh() {
  try {
    const res = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${Auth.getRefresh()}` },
    });
    if (!res.ok) return false;
    const json = await res.json();
    localStorage.setItem('iga_access_token', json.data.access_token);
    return true;
  } catch { return false; }
}

const AuthAPI = {
  registerStudent: (d) => apiFetch('/auth/register/student', { method: 'POST', body: JSON.stringify(d) }),
  registerTeacher: (d) => apiFetch('/auth/register/teacher', { method: 'POST', body: JSON.stringify(d) }),
  login:           (d) => apiFetch('/auth/login',            { method: 'POST', body: JSON.stringify(d) }),
  verifyEmail:     (d) => apiFetch('/auth/verify-email',     { method: 'POST', body: JSON.stringify(d) }),
  resendOTP:       (d) => apiFetch('/auth/resend-otp',       { method: 'POST', body: JSON.stringify(d) }),
  forgotPassword:  (d) => apiFetch('/auth/forgot-password',  { method: 'POST', body: JSON.stringify(d) }),
  resetPassword:   (d) => apiFetch('/auth/reset-password',   { method: 'POST', body: JSON.stringify(d) }),
  logout:          ()  => apiFetch('/auth/logout',           { method: 'POST' }),
  getMe:           ()  => apiFetch('/auth/me'),
  updateMe:        (d) => apiFetch('/auth/me', { method: 'PUT', body: JSON.stringify(d) }),
};

const CourseAPI = {
  list:               ()        => apiFetch('/courses'),
  get:                (id)      => apiFetch(`/courses/${id}`),
  create:             (d)       => apiFetch('/courses',                  { method: 'POST',   body: JSON.stringify(d) }),
  update:             (id, d)   => apiFetch(`/courses/${id}`,            { method: 'PUT',    body: JSON.stringify(d) }),
  delete:             (id)      => apiFetch(`/courses/${id}`,            { method: 'DELETE' }),
  addModule:          (cid, d)  => apiFetch(`/courses/${cid}/modules`,   { method: 'POST',   body: JSON.stringify(d) }),
  deleteModule:       (mid)     => apiFetch(`/courses/modules/${mid}`,   { method: 'DELETE' }),
  addLesson: (mid, d, file) => {
    if (file) {
      const form = new FormData();
      form.append('title',     d.title);
      form.append('file_type', d.file_type || 'video');
      if (d.file_url) form.append('file_url', d.file_url);
      form.append('file', file);
      return fetch(`${API_BASE}/courses/modules/${mid}/lessons`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${Auth.getToken()}` },
        body: form,
      }).then(r => r.json().then(data => ({ ok: r.ok, status: r.status, data }))).catch(() => ({ ok:false, status:0, data:{message:'Upload failed.'} }));
    }
    return apiFetch(`/courses/modules/${mid}/lessons`, { method: 'POST', body: JSON.stringify(d) });
  },
  updateLesson: (lid, d, file) => {
    if (file) {
      const form = new FormData();
      if (d.title)     form.append('title',     d.title);
      if (d.file_type) form.append('file_type', d.file_type);
      if (d.file_url)  form.append('file_url',  d.file_url);
      form.append('file', file);
      return fetch(`${API_BASE}/courses/lessons/${lid}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${Auth.getToken()}` },
        body: form,
      }).then(r => r.json().then(data => ({ ok: r.ok, status: r.status, data }))).catch(() => ({ ok:false, status:0, data:{message:'Upload failed.'} }));
    }
    return apiFetch(`/courses/lessons/${lid}`, { method: 'PUT', body: JSON.stringify(d) });
  },
  deleteLesson:       (lid)     => apiFetch(`/courses/lessons/${lid}`,   { method: 'DELETE' }),
  enroll:             (cid)     => apiFetch(`/courses/${cid}/enroll`,    { method: 'POST' }),
  myEnrollments:      ()        => apiFetch('/courses/my-enrollments'),
  completeLesson:     (lid)     => apiFetch(`/courses/lessons/${lid}/complete`, { method: 'POST' }),
  uncompleteLesson:   (lid)     => apiFetch(`/courses/lessons/${lid}/complete`, { method: 'DELETE' }),
  myCompletions:      ()        => apiFetch('/courses/my-completions'),
};

const AssessmentAPI = {
  listAll:        ()         => apiFetch('/courses/assessments/all'),
  listForCourse:  (cid)      => apiFetch(`/courses/${cid}/assessments`),
  get:            (id)       => apiFetch(`/courses/assessments/${id}`),
  create:         (cid, d)   => apiFetch(`/courses/${cid}/assessments`,           { method: 'POST',   body: JSON.stringify(d) }),
  update:         (id, d)    => apiFetch(`/courses/assessments/${id}`,             { method: 'PUT',    body: JSON.stringify(d) }),
  addQuestion:    (aid, d)   => apiFetch(`/courses/assessments/${aid}/questions`,  { method: 'POST',   body: JSON.stringify(d) }),
  updateQuestion: (qid, d)   => apiFetch(`/courses/questions/${qid}`,              { method: 'PUT',    body: JSON.stringify(d) }),
  deleteQuestion: (qid)      => apiFetch(`/courses/questions/${qid}`,              { method: 'DELETE' }),
  submit:         (aid, d)   => apiFetch(`/courses/assessments/${aid}/submit`,     { method: 'POST',   body: JSON.stringify(d) }),
};

const GradeAPI = {
  myGrades:              () => apiFetch('/courses/my-submissions'),
  studentPerformance:    () => apiFetch('/courses/teacher/students'),
  pendingGrades:         () => apiFetch('/courses/teacher/pending-grades'),
  gradeSubmission:       (sid, d) => apiFetch(`/courses/submissions/${sid}/grade`, { method: 'POST', body: JSON.stringify(d) }),
  teacherViewSubmission: (sid)    => apiFetch(`/courses/teacher/submission/${sid}`),
  exportPDF: async () => {
    const token = Auth.getToken();
    if (!token) { showToast('Not authenticated.', 'error'); return; }
    try {
      const res = await fetch(`${API_BASE}/courses/teacher/export-report`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.status === 401) {
        // Try refresh then retry once
        const refreshed = await _tryRefresh();
        if (!refreshed) { showToast('Session expired. Please log in again.', 'error'); return; }
        const retry = await fetch(`${API_BASE}/courses/teacher/export-report`, {
          headers: { 'Authorization': `Bearer ${Auth.getToken()}` }
        });
        if (!retry.ok) { showToast('Failed to generate report.', 'error'); return; }
        const blob2 = await retry.blob();
        const a2 = document.createElement('a');
        a2.href = URL.createObjectURL(blob2);
        a2.download = `iga_report_${new Date().toISOString().slice(0,10)}.pdf`;
        a2.click();
        URL.revokeObjectURL(a2.href);
        return;
      }
      if (!res.ok) { showToast('Failed to generate report.', 'error'); return; }
      const blob = await res.blob();
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `iga_report_${new Date().toISOString().slice(0,10)}.pdf`;
      a.click();
      URL.revokeObjectURL(a.href);
    } catch { showToast('Failed to generate report.', 'error'); }
  },
};

function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${{success:'✓',error:'✕',info:'ℹ'}[type]||'ℹ'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0'; toast.style.transform = 'translateY(8px)';
    toast.style.transition = 'all .3s';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function setLoading(btn, loading) {
  if (loading) { btn.dataset.origText = btn.innerHTML; btn.innerHTML = '<div class="spinner"></div>'; btn.disabled = true; }
  else { btn.innerHTML = btn.dataset.origText || btn.innerHTML; btn.disabled = false; }
}

function redirectToDashboard(role) {
  const isSubPage = window.location.pathname.includes('/pages/');
  const prefix    = isSubPage ? '' : 'pages/';
  window.location.href = role === 'teacher' ? `${prefix}teacher-dashboard.html` : `${prefix}student-dashboard.html`;
}

function requireAuth(expectedRole = null) {
  if (!Auth.isLoggedIn()) { window.location.href = 'login.html'; return false; }
  if (expectedRole && Auth.getRole() !== expectedRole && Auth.getRole() !== 'admin') {
    window.location.href = 'login.html'; return false;
  }
  return true;
}

async function handleLogout() {
  await AuthAPI.logout().catch(() => {});
  Auth.clearSession();
  window.location.href = 'login.html';
}