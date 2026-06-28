function filterTasks() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.task-card');

    cards.forEach(function(card) {
        const titleEl = card.querySelector('.task-title');
        if (!titleEl) return;
        const titleText = titleEl.textContent.toLowerCase();
        card.style.display = titleText.includes(input) ? '' : 'none';
    });
}