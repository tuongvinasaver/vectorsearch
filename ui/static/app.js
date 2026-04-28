/* ─── app.js — DataVector Camera Dashboard ─── */
'use strict';

const API = '';          // same origin; change to 'http://localhost:5000' if serving separately
let allCameras  = [];
let currentFilter = 'all';
let currentView   = 'grid';
let deleteTargetId   = null;
let deleteTargetName = '';

/* ══════════════════════════════════════════════
   INIT
══════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  loadCameras();
  checkConnection();
});

/* ══════════════════════════════════════════════
   NAVIGATION
══════════════════════════════════════════════ */
function showSection(name) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById(`section-${name}`).classList.add('active');
  document.getElementById('page-title').textContent =
    name === 'search' ? 'Vector Search' :
    'Camera Management';

  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const navEl = document.getElementById(`nav-${name}`);
  if (navEl) navEl.classList.add('active');

  // Lazy-load index count when Vector Search section is opened
  if (name === 'search') loadVsStatus();

  // Close sidebar on mobile
  if (window.innerWidth <= 768) document.getElementById('sidebar').classList.remove('open');
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

/* ══════════════════════════════════════════════
   CONNECTION CHECK
══════════════════════════════════════════════ */
async function checkConnection() {
  try {
    const r = await fetch(`${API}/api/stats`);
    const badge = document.getElementById('connection-badge');
    if (r.ok) {
      document.getElementById('conn-text').textContent = 'API Connected';
      badge.querySelector('.pulse-dot').style.background = 'var(--green)';
    } else {
      throw new Error();
    }
  } catch {
    document.getElementById('conn-text').textContent = 'API Offline';
    document.querySelector('.pulse-dot').style.background = 'var(--red)';
  }
}


/* ══════════════════════════════════════════════
   LOAD CAMERAS
══════════════════════════════════════════════ */
async function loadCameras() {
  try {
    const res  = await fetch(`${API}/api/cameras`);
    const data = await res.json();
    allCameras = data.cameras || [];
    renderAll();
  } catch {
    showToast('error', 'Could not load cameras. Is the API running?');
    document.getElementById('cameras-grid').innerHTML =
      '<p class="no-data" style="grid-column:1/-1">Failed to load cameras.</p>';
  }
}

function renderAll() {
  const filtered = filterCameras(allCameras, currentFilter);
  renderGrid(filtered);
  renderListTable(filtered, 'cameras-tbody', true);
}

function filterCameras(list, filter) {
  if (filter === 'all') return list;
  return list.filter(c => c.status === filter);
}

/* ─── GRID ─── */
function renderGrid(cameras) {
  const grid = document.getElementById('cameras-grid');
  if (!cameras.length) {
    grid.innerHTML = '<p class="no-data" style="grid-column:1/-1">No cameras found.</p>';
    return;
  }
  grid.innerHTML = cameras.map(cam => `
    <div class="cam-card" id="cam-card-${cam.id}">
      <div class="cam-card-header">
        <div style="display:flex;gap:12px;align-items:flex-start">
          <div class="cam-thumb">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/>
            </svg>
          </div>
          <div>
            <div class="cam-name">${esc(cam.name)}</div>
            <div class="cam-location">${esc(cam.location || '—')}</div>
          </div>
        </div>
        ${statusBadge(cam.status)}
      </div>
      <div class="cam-meta">
        <div class="cam-meta-row">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2"/><path d="M7 2v20M17 2v20M2 12h20M2 7h5M2 17h5M17 7h5M17 17h5"/></svg>
          <span>IP:</span><span class="mono">${esc(cam.ip_address || '—')}</span>
        </div>
        <div class="cam-meta-row">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
          <span>${esc(cam.resolution || '—')}</span>
        </div>
      </div>
      <div class="cam-footer">
        <span style="font-size:.72rem;color:var(--text-3)">#${cam.id}</span>
        <div class="cam-actions">
          <button class="btn-icon" onclick="openModal('edit', ${cam.id})" title="Edit" aria-label="Edit camera">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </button>
          <button class="btn-icon danger" onclick="openDeleteModal(${cam.id}, '${esc(cam.name)}')" title="Delete" aria-label="Delete camera">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

/* ─── TABLE ─── */
function renderListTable(cameras, tbodyId, showDate) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  if (!cameras.length) {
    const cols = showDate ? 8 : 7;
    tbody.innerHTML = `<tr><td colspan="${cols}" class="no-data">No cameras found.</td></tr>`;
    return;
  }
  tbody.innerHTML = cameras.map(cam => `
    <tr>
      <td class="td-mono">${cam.id}</td>
      <td><strong>${esc(cam.name)}</strong></td>
      <td>${esc(cam.location || '—')}</td>
      <td class="td-mono">${esc(cam.ip_address || '—')}</td>
      <td>${esc(cam.resolution || '—')}</td>
      <td>${statusBadge(cam.status)}</td>
      ${showDate ? `<td class="td-mono" style="font-size:.75rem">${fmtDate(cam.created_at)}</td>` : ''}
      <td>
        <div class="td-actions">
          <button class="btn-icon" onclick="openModal('edit', ${cam.id})" title="Edit" aria-label="Edit">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </button>
          <button class="btn-icon danger" onclick="openDeleteModal(${cam.id}, '${esc(cam.name)}')" title="Delete" aria-label="Delete">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

/* ══════════════════════════════════════════════
   FILTER & VIEW
══════════════════════════════════════════════ */
function applyFilter(filter, btn) {
  currentFilter = filter;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderAll();
}

function setView(view, btn) {
  currentView = view;
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const grid = document.getElementById('cameras-grid');
  const list = document.getElementById('cameras-list');
  if (view === 'grid') {
    grid.classList.remove('hidden');
    list.classList.add('hidden');
  } else {
    grid.classList.add('hidden');
    list.classList.remove('hidden');
  }
}

/* ══════════════════════════════════════════════
   SEARCH
══════════════════════════════════════════════ */
let searchDebounce = null;
function handleSearch(term) {
  clearTimeout(searchDebounce);
  searchDebounce = setTimeout(async () => {
    if (!term.trim()) {
      renderAll();
      return;
    }
    try {
      const res  = await fetch(`${API}/api/cameras/search/${encodeURIComponent(term.trim())}`);
      const data = await res.json();
      const cams = data.cameras || [];
      renderGrid(cams);
      renderListTable(cams, 'cameras-tbody', true);
    } catch {
      showToast('error', 'Search failed.');
    }
  }, 300);
}

/* ══════════════════════════════════════════════
   ADD / EDIT MODAL
══════════════════════════════════════════════ */
function openModal(mode, cameraId = null) {
  const overlay = document.getElementById('modal-overlay');
  const form    = document.getElementById('camera-form');
  const errEl   = document.getElementById('form-error');
  form.reset();
  errEl.classList.add('hidden');
  document.getElementById('form-camera-id').value = '';

  if (mode === 'add') {
    document.getElementById('modal-title').textContent = 'Add Camera';
    document.getElementById('form-submit-text').textContent = 'Add Camera';
  } else {
    document.getElementById('modal-title').textContent = 'Edit Camera';
    document.getElementById('form-submit-text').textContent = 'Save Changes';
    const cam = allCameras.find(c => c.id === cameraId);
    if (cam) {
      document.getElementById('form-camera-id').value  = cam.id;
      document.getElementById('form-name').value       = cam.name || '';
      document.getElementById('form-ip').value         = cam.ip_address || '';
      document.getElementById('form-location').value   = cam.location || '';
      document.getElementById('form-resolution').value = cam.resolution || '';
      document.getElementById('form-status').value     = cam.status || 'active';
      
      const imgPath = cam.image || '';
      document.getElementById('form-image-path').value = imgPath;
      if (imgPath) {
        document.getElementById('form-image-display').src = imgPath;
        document.getElementById('form-image-display').classList.remove('hidden');
        document.getElementById('form-image-placeholder').classList.add('hidden');
      } else {
        document.getElementById('form-image-display').classList.add('hidden');
        document.getElementById('form-image-placeholder').classList.remove('hidden');
      }
    }
  }
  overlay.classList.add('open');
}

function previewFormImage(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    document.getElementById('form-image-display').src = ev.target.result;
    document.getElementById('form-image-display').classList.remove('hidden');
    document.getElementById('form-image-placeholder').classList.add('hidden');
  };
  reader.readAsDataURL(file);
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('open');
}
function closeModalOnOverlay(e) {
  if (e.target === document.getElementById('modal-overlay')) closeModal();
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const id     = document.getElementById('form-camera-id').value;
  const isEdit = !!id;
  const errEl  = document.getElementById('form-error');
  const btn    = document.getElementById('form-submit-btn');
  const text   = document.getElementById('form-submit-text');
  const spinner = document.getElementById('form-spinner');

  const formData = new FormData();
  formData.append('name', document.getElementById('form-name').value.trim());
  formData.append('ip_address', document.getElementById('form-ip').value.trim());
  formData.append('location', document.getElementById('form-location').value.trim());
  formData.append('resolution', document.getElementById('form-resolution').value.trim());
  formData.append('status', document.getElementById('form-status').value);
  
  const imgFile = document.getElementById('form-image').files[0];
  if (imgFile) {
    formData.append('image', imgFile);
  }

  // Client-side validation
  if (!formData.get('name') || !formData.get('ip_address') || !formData.get('location')) {
    showFormError(errEl, 'Name, IP Address, and Location are required.');
    return;
  }

  errEl.classList.add('hidden');
  btn.disabled = true;
  text.classList.add('hidden');
  spinner.classList.remove('hidden');

  try {
    const url    = isEdit ? `${API}/api/cameras/${id}` : `${API}/api/cameras`;
    const method = isEdit ? 'PUT' : 'POST';
    const res    = await fetch(url, {
      method,
      body: formData, // Browser sets Content-Type automatically for FormData
    });
    const data = await res.json();

    if (!data.success) throw new Error(data.message || 'Request failed');

    closeModal();
    showToast('success', isEdit ? 'Camera updated successfully.' : 'Camera added successfully.');
    await loadCameras();
  } catch (err) {
    showFormError(errEl, err.message || 'Something went wrong. Please try again.');
  } finally {
    btn.disabled = false;
    text.classList.remove('hidden');
    spinner.classList.add('hidden');
  }
}

function showFormError(el, msg) {
  el.textContent = msg;
  el.classList.remove('hidden');
}

/* ══════════════════════════════════════════════
   DELETE MODAL
══════════════════════════════════════════════ */
function openDeleteModal(id, name) {
  deleteTargetId   = id;
  deleteTargetName = name;
  document.getElementById('delete-camera-name').textContent = name;
  document.getElementById('delete-error').classList.add('hidden');
  document.getElementById('delete-overlay').classList.add('open');
}

function closeDeleteModal() {
  document.getElementById('delete-overlay').classList.remove('open');
  deleteTargetId = null;
}
function closeDeleteOnOverlay(e) {
  if (e.target === document.getElementById('delete-overlay')) closeDeleteModal();
}

async function confirmDelete() {
  if (!deleteTargetId) return;
  const btn     = document.getElementById('delete-confirm-btn');
  const text    = document.getElementById('delete-btn-text');
  const spinner = document.getElementById('delete-spinner');
  const errEl   = document.getElementById('delete-error');

  btn.disabled = true;
  text.classList.add('hidden');
  spinner.classList.remove('hidden');
  errEl.classList.add('hidden');

  try {
    const res  = await fetch(`${API}/api/cameras/${deleteTargetId}`, { method: 'DELETE' });
    const data = await res.json();
    if (!data.success) throw new Error(data.message || 'Delete failed');

    closeDeleteModal();
    showToast('success', `Camera "${deleteTargetName}" deleted.`);
    await loadCameras();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    text.classList.remove('hidden');
    spinner.classList.add('hidden');
  }
}

/* ══════════════════════════════════════════════
   TOAST
══════════════════════════════════════════════ */
function showToast(type, message) {
  const icons = {
    success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    error:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    info:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
  };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `${icons[type] || icons.info}<span>${esc(message)}</span>`;
  document.getElementById('toast-container').appendChild(toast);
  setTimeout(() => toast.remove(), 4200);
}

/* ══════════════════════════════════════════════
   HELPERS
══════════════════════════════════════════════ */
function statusBadge(status) {
  const cls = status === 'active' ? 'badge-active' : 'badge-inactive';
  return `<span class="badge ${cls}"><span class="badge-dot"></span>${status || 'unknown'}</span>`;
}

function fmtDate(ts) {
  if (!ts) return '—';
  try { return new Date(ts).toLocaleDateString('en-GB', { day:'2-digit', month:'short', year:'numeric' }); }
  catch { return ts; }
}

function esc(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;')
    .replace(/'/g,'&#39;');
}

/* ══════════════════════════════════════════════
   VECTOR SEARCH — STATE
══════════════════════════════════════════════ */
let vsImageFile = null;   // File object from file picker
let vsImageUrl  = '';     // URL pasted by user

/* ── Tab switching ─────────────────────────── */
function switchVsTab(tab) {
  document.querySelectorAll('.vs-tab').forEach(t => t.classList.remove('active'));
  document.getElementById(`vstab-${tab}`).classList.add('active');
  document.getElementById('vs-panel-text').classList.toggle('hidden',   tab !== 'text');
  document.getElementById('vs-panel-image').classList.toggle('hidden',  tab !== 'image');
  document.getElementById('vs-panel-hybrid').classList.toggle('hidden', tab !== 'hybrid');
  const elasticPanel = document.getElementById('vs-panel-elastic');
  if (elasticPanel) elasticPanel.classList.toggle('hidden', tab !== 'elastic');
}

/* ── Index status (load on section show) ───── */
async function loadVsStatus() {
  try {
    const res  = await fetch(`${API}/api/vector/status`);
    const data = await res.json();
    if (data.success) {
      document.getElementById('vs-index-count').textContent = data.indexed;
    }
  } catch { /* silently ignore */ }
}

/* ── Re-index all ──────────────────────────── */
async function reindexAll() {
  const btn     = document.getElementById('reindex-btn');
  const spinner = document.getElementById('reindex-spinner');
  btn.disabled  = true;
  spinner.classList.remove('hidden');
  try {
    const res  = await fetch(`${API}/api/vector/index/all`, { method: 'POST' });
    const data = await res.json();
    if (!data.success) throw new Error(data.message);
    showToast('success', `Re-indexed ${data.indexed} / ${data.total} cameras.`);
    document.getElementById('vs-index-count').textContent = data.indexed;
  } catch (err) {
    showToast('error', err.message || 'Re-index failed.');
  } finally {
    btn.disabled = false;
    spinner.classList.add('hidden');
  }
}
/* ══════════════════════════════════════════════
   ELASTICSEARCH (KEYWORD SEARCH)
══════════════════════════════════════════════ */
async function runElasticSearch() {
  const query = document.getElementById('vs-elastic-input').value.trim();
  if (!query) { showToast('info', 'Enter a search query.'); return; }

  const limit  = parseInt(document.getElementById('vs-elastic-limit').value, 10);
  const status = document.getElementById('vs-elastic-status').value;

  const btn     = document.getElementById('vs-elastic-btn');
  const spinner = document.getElementById('vs-elastic-spinner');
  const results = document.getElementById('vs-elastic-results');

  btn.disabled = true;
  spinner.classList.remove('hidden');
  results.innerHTML = '<div class="vs-empty"><div class="spinner"></div></div>';

  try {
    const res  = await fetch(`${API}/api/vector/search/elastic`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ query, limit, status }),
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.message);
    
    // Render using the same vs results renderer
    renderVsResults(data.cameras, results);
  } catch (err) {
    results.innerHTML = `<div class="vs-empty"><p>${esc(err.message || 'Elasticsearch failed.')}</p></div>`;
  } finally {
    btn.disabled = false;
    spinner.classList.add('hidden');
  }
}


/* ══════════════════════════════════════════════
   VECTOR SEARCH — TEXT
══════════════════════════════════════════════ */
async function runTextSearch() {
  const query = document.getElementById('vs-text-input').value.trim();
  if (!query) { showToast('info', 'Enter a search query.'); return; }

  const limit     = parseInt(document.getElementById('vs-text-limit').value, 10);
  const status    = document.getElementById('vs-text-status').value;
  const threshold = parseFloat(document.getElementById('vs-text-threshold').value) / 100;

  const btn     = document.getElementById('vs-text-btn');
  const spinner = document.getElementById('vs-text-spinner');
  const results = document.getElementById('vs-text-results');

  btn.disabled = true;
  spinner.classList.remove('hidden');
  results.innerHTML = '<div class="vs-empty"><div class="spinner"></div></div>';

  try {
    const res  = await fetch(`${API}/api/vector/search/text`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ query, limit, status, threshold }),
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.message);
    renderVsResults(data.cameras, results);
  } catch (err) {
    results.innerHTML = `<div class="vs-empty"><p>${esc(err.message || 'Search failed.')}</p></div>`;
  } finally {
    btn.disabled = false;
    spinner.classList.add('hidden');
  }
}

/* ══════════════════════════════════════════════
   VECTOR SEARCH — HYBRID
   Combine Keyword + Semantic
══════════════════════════════════════════════ */
async function runHybridSearch() {
  const query = document.getElementById('vs-hybrid-input').value.trim();
  if (!query) { showToast('info', 'Enter a search query.'); return; }

  const limit     = parseInt(document.getElementById('vs-hybrid-limit').value, 10);
  const status    = document.getElementById('vs-hybrid-status').value;
  const threshold = parseFloat(document.getElementById('vs-hybrid-threshold').value) / 100;

  const btn     = document.getElementById('vs-hybrid-btn');
  const spinner = document.getElementById('vs-hybrid-spinner');
  const results = document.getElementById('vs-hybrid-results');

  btn.disabled = true;
  spinner.classList.remove('hidden');
  results.innerHTML = '<div class="vs-empty"><div class="spinner"></div></div>';

  try {
    const res  = await fetch(`${API}/api/vector/search/hybrid`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ query, limit, status, threshold }),
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.message);
    renderVsResults(data.cameras, results);
  } catch (err) {
    results.innerHTML = `<div class="vs-empty"><p>${esc(err.message || 'Hybrid search failed.')}</p></div>`;
  } finally {
    btn.disabled = false;
    spinner.classList.add('hidden');
  }
}

/* ══════════════════════════════════════════════
   VECTOR SEARCH — IMAGE
══════════════════════════════════════════════ */
async function runImageSearch() {
  const hasFile = !!vsImageFile;
  const hasUrl  = !!vsImageUrl.trim();
  if (!hasFile && !hasUrl) { showToast('info', 'Upload an image or paste a URL first.'); return; }

  const limit     = parseInt(document.getElementById('vs-img-limit').value, 10);
  const status    = document.getElementById('vs-img-status').value;
  const threshold = parseFloat(document.getElementById('vs-img-threshold').value) / 100;

  const btn     = document.getElementById('vs-img-btn');
  const spinner = document.getElementById('vs-img-spinner');
  const results = document.getElementById('vs-image-results');

  btn.disabled = true;
  spinner.classList.remove('hidden');
  results.innerHTML = '<div class="vs-empty"><div class="spinner"></div></div>';

  try {
    let res;
    if (hasFile) {
      const form = new FormData();
      form.append('image', vsImageFile);
      form.append('limit', limit);
      form.append('status', status);
      form.append('threshold', threshold);
      res = await fetch(`${API}/api/vector/search/image`, { method: 'POST', body: form });
    } else {
      res = await fetch(`${API}/api/vector/search/image`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ url: vsImageUrl.trim(), limit, status, threshold }),
      });
    }
    const data = await res.json();
    if (!data.success) throw new Error(data.message);
    renderVsResults(data.cameras, results);
  } catch (err) {
    results.innerHTML = `<div class="vs-empty"><p>${esc(err.message || 'Image search failed.')}</p></div>`;
  } finally {
    btn.disabled = false;
    spinner.classList.add('hidden');
  }
}

/* ══════════════════════════════════════════════
   VECTOR SEARCH — RESULTS RENDER
══════════════════════════════════════════════ */
function renderVsResults(results, container) {
  if (!results || !results.length) {
    container.innerHTML = `
      <div class="vs-empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <p>No matching cameras found in the index.</p>
        <p style="font-size:.75rem;margin-top:6px">Try Re-index All if you just added cameras.</p>
      </div>`;
    return;
  }
  container.innerHTML = results.map((cam, i) => {
    const scorePct = Math.round((cam.score || 0) * 100);
    const color    = scorePct >= 70 ? 'var(--green)' : scorePct >= 40 ? 'var(--yellow)' : 'var(--red)';
    
    const imgHtml = cam.image 
      ? `<div class="vs-result-thumb"><img src="${cam.image}" alt="${cam.name}"></div>`
      : `<div class="vs-cam-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg></div>`;

    return `
      <div class="vs-result-card">
        <span class="vs-rank">${i + 1}</span>
        ${imgHtml}
        <div class="vs-result-body">
          <div class="vs-result-name">${esc(cam.name)}</div>
          <div class="vs-result-meta">
            <span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              ${esc(cam.location || '—')}
            </span>
            <span style="font-family:'JetBrains Mono',monospace">${esc(cam.ip_address || '—')}</span>
            ${statusBadge(cam.status)}
          </div>
        </div>
        <div class="vs-score-wrap">
          <div class="vs-score-label">Similarity</div>
          <div class="vs-score-value" style="color:${color}">${scorePct}%</div>
          <div class="vs-score-bar-bg">
            <div class="vs-score-bar" style="width: ${scorePct}%; background:${color}"></div>
          </div>
          <button class="btn-inspect" onclick='showAiDetails(${JSON.stringify(cam).replace(/'/g, "&apos;")})'>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            Inspect
          </button>
        </div>
      </div>`;
  }).join('');
}

function showAiDetails(res) {
  const overlay = document.getElementById('ai-modal-overlay');
  document.getElementById('ai-inspect-score').innerText = Math.round(res.score * 100) + '%';
  document.getElementById('ai-inspect-distance').innerText = (res.distance || 0).toFixed(4) + ' (Cosine)';
  
  // Use real embedding data from backend
  const emb = res.embedding || [];
  const snippet = emb.slice(0, 12).map(v => v.toFixed(3)).join(', ');
  document.getElementById('ai-inspect-vector').innerText = emb.length > 0 
    ? `[${snippet}${emb.length > 12 ? ', ...' : ''}]`
    : '[No vector data available]';
  
  document.getElementById('ai-inspect-meta').innerText = JSON.stringify(res.metadata || {}, null, 2);
  overlay.classList.add('open');
}

function closeAiModal() {
  document.getElementById('ai-modal-overlay').classList.remove('open');
}

/* ══════════════════════════════════════════════
   DROP ZONE HANDLERS
══════════════════════════════════════════════ */
function dzDragOver(e) {
  e.preventDefault();
  document.getElementById('dropzone').classList.add('drag-over');
}
function dzDragLeave(e) {
  document.getElementById('dropzone').classList.remove('drag-over');
}
function dzDrop(e) {
  e.preventDefault();
  document.getElementById('dropzone').classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) _setDzFile(file);
}
function dzFileSelected(e) {
  const file = e.target.files[0];
  if (file) _setDzFile(file);
}
function dzUrlChanged(val) {
  vsImageUrl = val;
  // If user types a URL, clear any uploaded file preview
  if (val.trim()) {
    vsImageFile = null;
    document.getElementById('dz-preview').classList.add('hidden');
    document.getElementById('dz-inner').classList.remove('hidden');
  }
}


function _setDzFile(file) {
  vsImageFile = file;
  vsImageUrl  = '';
  document.getElementById('vs-img-url').value = '';
  const reader = new FileReader();
  reader.onload = ev => {
    const img = document.getElementById('dz-preview-img');
    img.src   = ev.target.result;
    document.getElementById('dz-inner').classList.add('hidden');
    document.getElementById('dz-preview').classList.remove('hidden');
  };
  reader.readAsDataURL(file);
}
function clearDz(e) {
  e.stopPropagation();
  vsImageFile = null;
  vsImageUrl  = '';
  document.getElementById('img-file-input').value = '';
  document.getElementById('vs-img-url').value     = '';
  document.getElementById('dz-preview').classList.add('hidden');
  document.getElementById('dz-inner').classList.remove('hidden');
}
