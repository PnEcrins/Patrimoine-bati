function toggleTableRows(btn) {
    var table = btn.closest('table');
    var tbody = table.querySelector('tbody');
    var arrow = btn.querySelector('.arrow');
    var collapsed = btn.classList.toggle('collapsed');
    if (collapsed) {
        tbody.style.display = 'none';
        arrow.textContent = '+';
    } else {
        tbody.style.display = '';
        arrow.textContent = '−';
    }
}