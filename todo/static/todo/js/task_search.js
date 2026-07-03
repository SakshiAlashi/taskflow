console.log("Search JS Loaded");
document.addEventListener("DOMContentLoaded", function () {

    const topSearch = document.getElementById("globalSearch");
    const pageSearch = document.getElementById("searchInput");

        function filterTasks(value) {

            value = value.toLowerCase();

            document.querySelectorAll(".task-card").forEach(card => {

                const text = card.textContent.toLowerCase();

                card.style.display =
                    text.includes(value) ? "" : "none";

            });
        }
    if (topSearch) {
        topSearch.addEventListener("input", function () {
            filterTasks(this.value);

            if (pageSearch)
                pageSearch.value = this.value;
        });
    }

    if (pageSearch) {
        pageSearch.addEventListener("input", function () {
            filterTasks(this.value);

            if (topSearch)
                topSearch.value = this.value;
        });
    }

});