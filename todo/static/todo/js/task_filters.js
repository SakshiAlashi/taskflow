const filterState = {
    tab: "all",
    search: "",
    priority: "all",
    category: "all",
    sort: "due_date",
};

document.addEventListener("DOMContentLoaded", function () {
    const isTaskPage = document.querySelector(".task-tab");

    if (!isTaskPage) {
        return;
    }
    const globalSearch = document.getElementById("globalSearch");

    const tabs = document.querySelectorAll(".task-tab");
    const cards = document.querySelectorAll(".task-card");
    const priorityFilter = document.getElementById("priorityFilter");
    const categoryFilter = document.getElementById("categoryFilter");
    const sortFilter = document.getElementById("sortFilter");
    const pendingSection = document.getElementById("pendingSection");
    const completedSection = document.getElementById("completedSection");
    const pendingColumn = document.getElementById("pendingColumn");
    const completedColumn = document.getElementById("completedColumn");

    function sortColumn(column) {
        const cards = Array.from(
        column.querySelectorAll(".task-card")
        );
        const priorityOrder = {
            high: 1,
            medium: 2,
            low: 3
        };

        if (filterState.sort === "priority") {

            cards.sort((a, b) => {
            
                return (
                    priorityOrder[a.dataset.priority] -
                    priorityOrder[b.dataset.priority]
                );

            });

        }

        if (filterState.sort === "due_date") {

            cards.sort((a, b) => {

                const dateA = a.dataset.due || "9999-12-31";
                const dateB = b.dataset.due || "9999-12-31";

                return dateA.localeCompare(dateB);

            });

        }
        if (filterState.sort === "newest") {

            cards.sort((a, b) => {

                return b.dataset.created.localeCompare(a.dataset.created);

            });

        }

        if (filterState.sort === "oldest") {

            cards.sort((a, b) => {

                return a.dataset.created.localeCompare(b.dataset.created);

            });

        }
        cards.forEach(card => {

            column.appendChild(card);

        });
    }

    function applyFilters() {
        let visiblePending = 0;
        let visibleCompleted = 0;
        cards.forEach(card => {

            const status = card.dataset.status;
            const overdue = card.dataset.overdue;
            const priority = card.dataset.priority;
            const category = card.dataset.category;
            const text = card.textContent.toLowerCase();

            let show = true;

            // Tab
            if (filterState.tab === "pending" && status !== "pending") {
                show = false;
            }

            if (filterState.tab === "completed" && status !== "completed") {
                show = false;
            }

            if (filterState.tab === "overdue" &&
                !(status === "pending" && overdue === "overdue")) {
                show = false;
            }

            if (
                filterState.priority !== "all" &&
                priority !== filterState.priority
            ) {
                show = false;
            }

            if (
                filterState.category !== "all" &&
                category !== filterState.category
            ) {
                show = false;
            }
            
            if (
                filterState.search &&
                !text.includes(filterState.search)
            ) {
                show = false;
            }

            if (show) {

                if (status === "pending") {
                    visiblePending++;
                } else {
                    visibleCompleted++;
                }

            }
            card.style.display = show ? "" : "none";

        });
        
        const pendingCount = document.getElementById("pendingCount");
        const completedCount = document.getElementById("completedCount");

        pendingCount.textContent = visiblePending;
        completedCount.textContent = visibleCompleted;
        
        pendingSection.style.display =
            visiblePending ? "" : "none";

        completedSection.style.display =
            visibleCompleted ? "" : "none";

        sortColumn(pendingColumn);
        sortColumn(completedColumn);
    }

    tabs.forEach(tab => {

        tab.addEventListener("click", function () {
            

            // Remove active class
            tabs.forEach(t => t.classList.remove("active"));
            this.classList.add("active");

            filterState.tab = this.textContent.trim().toLowerCase();

            applyFilters();

        });

    });
    if (priorityFilter) {

        priorityFilter.addEventListener("change", function () {

            filterState.priority = this.value;

            applyFilters();

        });

    }
    
    if (categoryFilter) {

        categoryFilter.addEventListener("change", function () {

            filterState.category = this.value;

            applyFilters();

        });
    }
    if (sortFilter) {

        sortFilter.addEventListener("change", function () {
           filterState.sort = this.value;
            applyFilters();
            });
        }

    if (globalSearch) {

        globalSearch.addEventListener("input", function () {

            filterState.search = this.value.toLowerCase().trim();

            applyFilters();

        });
    }
    applyFilters();
});