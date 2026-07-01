console.log("task_modal.js loaded");
function showToast(message) {

    const toastElement = document.getElementById("successToast");

    toastElement.querySelector(".toast-body").textContent = message;

    const toast = new bootstrap.Toast(toastElement, {
        delay: 3000
    });

    toast.show();

}

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".edit-task-form").forEach(form => {

        form.addEventListener("submit", async function (e) {

            e.preventDefault();

            // Clear previous errors
            form.querySelectorAll(".is-invalid").forEach(el => {
                el.classList.remove("is-invalid");
            });

            form.querySelectorAll(".invalid-feedback").forEach(el => {
                el.textContent = "";
            });

            const formData = new FormData(form);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (response.ok) {

                const data = await response.json();

                // Close modal
                const modalElement = form.closest(".modal");

                const modal = bootstrap.Modal.getInstance(modalElement);

                modal.hide();

                // Show toast
                showToast(data.message);

                // Reload after a short delay
                setTimeout(() => {
                    location.reload();
                }, 1200);

                return;
            }

            const data = await response.json();

            if (data.errors.title) {

                const input = form.querySelector(".title-input");
                input.classList.add("is-invalid");

                form.querySelector(".title-error").textContent =
                    data.errors.title[0];
            }

            if (data.errors.due_date) {

                const input = form.querySelector(".due-date-input");
                input.classList.add("is-invalid");

                form.querySelector(".due-date-error").textContent =
                    data.errors.due_date[0];
            }

        });

    });

    document.getElementById("taskForm").addEventListener("submit", async function (e) {

        e.preventDefault();

        const form = this;

        // Clear previous errors
        form.querySelectorAll(".is-invalid").forEach(el => {
            el.classList.remove("is-invalid");
        });

        form.querySelectorAll(".invalid-feedback").forEach(el => {
            el.textContent = "";
        });

        const formData = new FormData(form);

        const response = await fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (response.ok) {

            const data = await response.json();

            const modal = bootstrap.Modal.getInstance(
                document.getElementById("addTaskModal")
            );

            modal.hide();

            showToast(data.message);

            setTimeout(() => {
                location.reload();
            }, 1200);

            return;
        }

        const data = await response.json();

        if (data.errors.title) {

            const input = form.querySelector(".title-input");

            input.classList.add("is-invalid");

            form.querySelector(".title-error").textContent =
                data.errors.title[0];
        }

        if (data.errors.due_date) {

            const input = form.querySelector(".due-date-input");

            input.classList.add("is-invalid");

            form.querySelector(".due-date-error").textContent =
                data.errors.due_date[0];
        }

    });

    document.querySelectorAll(".delete-task-form").forEach(form => {

        form.addEventListener("submit", async function (e) {

            e.preventDefault();

            const formData = new FormData(form);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
                }
            });

            if (response.ok) {

                const data = await response.json();

                // Close delete modal
                const modalElement = form.closest(".modal");
                const modal = bootstrap.Modal.getInstance(modalElement);

                modal.hide();

                // Show toast
                showToast(data.message);

                // Reload page after a short delay
                setTimeout(() => {
                    location.reload();
                }, 1200);
            }

        });

    });

});

