document.addEventListener("DOMContentLoaded", function () {

    if (!window.showFocusReview) {
        return;
    }

    const modalElement = document.getElementById("focusReviewModal");

    if (!modalElement) {
        return;
    }

    const modal = new bootstrap.Modal(modalElement);

    modal.show();

});
document.addEventListener("DOMContentLoaded", function () {

    const selectAll = document.getElementById("selectAllFocusTasks");
    const clearAll = document.getElementById("clearAllFocusTasks");

    if (selectAll) {
        selectAll.addEventListener("click", function (e) {
            e.preventDefault();

            document.querySelectorAll(
                '#focusReviewModal input[type="checkbox"]'
            ).forEach(cb => cb.checked = true);
        });
    }

    if (clearAll) {
        clearAll.addEventListener("click", function (e) {
            e.preventDefault();

            document.querySelectorAll(
                '#focusReviewModal input[type="checkbox"]'
            ).forEach(cb => cb.checked = false);
        });
    }

});