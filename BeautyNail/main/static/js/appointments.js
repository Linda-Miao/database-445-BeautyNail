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
})();
