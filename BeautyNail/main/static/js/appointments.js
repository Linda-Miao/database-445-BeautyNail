// static/js/appointments.js
(function () {
  // ---- Service rows ----
  window.addServiceRow = function () {
    const box = document.getElementById('services-list');
    if (!box) return;
    const first = box.querySelector('.service-row');
    if (!first) return;
    const clone = first.cloneNode(true);
    const sel = clone.querySelector('select[name="service_ids[]"]');
    if (sel) sel.value = '';
    const color = clone.querySelector('input[name="polish_colors[]"]');
    if (color) color.value = '';
    box.appendChild(clone);
  };

  window.removeServiceRow = function (btn) {
    const box = document.getElementById('services-list');
    if (!box) return;
    const rows = box.querySelectorAll('.service-row');
    if (rows.length <= 1) return; // keep at least one
    btn.closest('.service-row')?.remove();
  };

  // ---- Date picker (inline) ----
  function initDate() {
    const host = document.getElementById('inline_date');
    const hidden = document.getElementById('appointment_date');
    if (!host || !hidden || !window.flatpickr) return;

    if (!hidden.value) {
      const t = new Date();
      const yyyy = t.getFullYear();
      const mm = String(t.getMonth() + 1).padStart(2, '0');
      const dd = String(t.getDate()).padStart(2, '0');
      hidden.value = `${yyyy}-${mm}-${dd}`;
    }

    const defaultDate = host.getAttribute('data-selected-date') || hidden.value;

    flatpickr(host, {
      inline: true,
      dateFormat: 'Y-m-d',
      defaultDate: defaultDate,
      onChange: (_, dateStr) => { hidden.value = dateStr; },
      // minDate: 'today',
    });
  }

  // ---- Time slots (shared for add/edit) ----
function initTime() {
  const grid = document.getElementById('time_grid');
  const hidden = document.getElementById('start_time');
  if (!grid || !hidden) return;

  const allBtns = Array.from(grid.querySelectorAll('.time-slot-btn'));
  let dataVal = (grid.getAttribute('data-selected-time') || hidden.value || '').trim();

  if (dataVal) {
    const norm = dataVal.length === 5 ? `${dataVal}:00` : dataVal;
    allBtns.forEach(b => b.classList.remove('selected-slot'));
    const match = grid.querySelector(`.time-slot-btn[data-time="${norm}"]`);
    if (match) {
      match.classList.add('selected-slot');
      hidden.value = norm;
    }
  } else {
    // ADD page: pick the first available slot by default
    const first = allBtns[0];
    if (first) {
      allBtns.forEach(b => b.classList.remove('selected-slot'));
      first.classList.add('selected-slot');
      hidden.value = (first.dataset.time || '').trim();
    }
  }

  // Click to select (always clear ALL, then set ONE)
  grid.addEventListener('click', (e) => {
    const btn = e.target.closest('.time-slot-btn');
    if (!btn) return;
    allBtns.forEach(b => b.classList.remove('selected-slot'));
    btn.classList.add('selected-slot');
    hidden.value = (btn.dataset.time || '').trim();
  });
}

// book now in services page
  function prefillServiceFromQuery() {
    const params = new URLSearchParams(window.location.search);
    const idRaw = params.get('prefill_service');
    if (!idRaw) return;
    const wanted = idRaw.trim();

    // Find selects inside the services list (guest + member forms)
    const selects = document.querySelectorAll('#services-list select[name="service_ids[]"]');
    if (!selects.length) return;

    // Prefer an empty select; fallback to the first one
    const target = Array.from(selects).find(s => !s.value || s.value.trim() === '') || selects[0];

    // Match by option value
    const opt = Array.from(target.options).find(o => (o.value || '').trim() === wanted);
    if (opt) {
      target.value = opt.value;
      target.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  // Run initializers
  document.addEventListener('DOMContentLoaded', function () {
    initDate();
    initTime();
    prefillServiceFromQuery();
  });


})();
