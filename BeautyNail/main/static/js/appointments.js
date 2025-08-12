// static/js/appointments.js
(function () {
  // Add a new .service-row inside #services-list
  window.addServiceRow = function () {
    const container = document.getElementById('services-list');
    if (!container) return;
    const first = container.querySelector('.service-row');
    if (!first) return;

    const clone = first.cloneNode(true);

    // Reset only the fields you use in the row
    const sel = clone.querySelector('select[name="service_ids[]"]');
    if (sel) sel.value = '';
    const colorInput = clone.querySelector('input[name="polish_colors[]"]');
    if (colorInput) colorInput.value = '';

    container.appendChild(clone);
  };

  // Remove the clicked .service-row, but keep at least one
  window.removeServiceRow = function (btn) {
    const container = document.getElementById('services-list');
    if (!container) return;
    const rows = container.querySelectorAll('.service-row');
    if (rows.length > 1 && btn && btn.closest) {
      btn.closest('.service-row').remove();
    }
  };

  // --- date picker + time grid ---
  document.addEventListener('DOMContentLoaded', function () {
    const dateEl = document.getElementById('inline_date');
    const dateHidden = document.getElementById('appointment_date');
    const timeHidden = document.getElementById('start_time');
    const timeGrid = document.getElementById('time_grid');

    if (typeof flatpickr !== 'undefined' && dateEl) {
      // Destroy any prior instance (if navigating back)
      if (dateEl._flatpickr && typeof dateEl._flatpickr.destroy === 'function') {
        dateEl._flatpickr.destroy();
      }
      flatpickr(dateEl, {
        inline: true,
        enableTime: false,      // DATE ONLY
        minDate: 'today',
        dateFormat: 'Y-m-d',
        defaultDate: 'today',
        onChange(selectedDates, dateStr) {
          dateHidden.value = dateStr;   // e.g., "2025-08-11"
        },
        onReady(selectedDates, dateStr, instance) {
          // initialize with default date
          dateHidden.value = dateStr || instance.formatDate(new Date(), 'Y-m-d');
        }
      });
    }

// Time selection
if (timeGrid && timeHidden) {
  timeGrid.addEventListener('click', function (e) {
    const btn = e.target.closest('.time-slot-btn');   // <- was .time-slot
    if (!btn) return;
    timeGrid.querySelectorAll('.time-slot-btn').forEach(b => b.classList.remove('active')); // <- was .time-slot
    btn.classList.add('active');                       // <- use .active for buttons
    timeHidden.value = btn.getAttribute('data-time');  // HH:MM:SS
  });

  // Default to first slot
  const first = timeGrid.querySelector('.time-slot-btn');
  if (first) {
    first.classList.add('active');
    timeHidden.value = first.getAttribute('data-time');
  }
}
  });
})();
