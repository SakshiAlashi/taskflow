const toggle = document.getElementById("progressToggle");
const data = document.getElementById("progressData");

const circle = document.getElementById("progressCircle");
const percent = document.getElementById("progressPercent");
const caption = document.getElementById("progressCaption");

const completed = document.getElementById("completedValue");
const pending = document.getElementById("pendingValue");
const total = document.getElementById("totalValue");

const title = document.getElementById("progressTitle");
const message = document.getElementById("progressMessage");

const heading = document.getElementById("progressHeading");
const headingIcon = document.getElementById("progressHeadingIcon");
const subtitle = document.getElementById("progressSubtitle");

function getOverallMessage(progress){

    progress = Number(progress);

    if(progress === 100){
        return {
            title: "🎉 Fantastic!",
            message: "You've completed every task."
        };
    }

    if(progress >= 75){
        return {
            title: "🔥 Excellent Progress",
            message: "Most of your tasks are completed."
        };
    }

    if(progress >= 50){
        return {
            title: "😊 Halfway There",
            message: "You're making steady progress."
        };
    }

    if(progress > 0){
        return {
            title: "💪 Keep Going",
            message: "You're building momentum."
        };
    }

    return {
        title: "🚀 Let's Get Started!",
        message: "Complete your first task."
    };
}

function showToday(){

    circle.style.setProperty(
        "--progress",
        data.dataset.todayProgress + "%"
    );

    percent.textContent = data.dataset.todayProgress + "%";

    caption.textContent = "Completed today";

    completed.textContent = data.dataset.todayCompleted;
    pending.textContent = data.dataset.todayPending;
    total.textContent = data.dataset.todayTotal;

    title.textContent = data.dataset.todayTitle;
    message.textContent = data.dataset.todayMessage;

    heading.textContent = "OVERALL PROGRESS";

    headingIcon.className =
        "bi bi-bar-chart-fill text-success me-2";

    subtitle.textContent =
        "Your complete task library";

    circle.style.setProperty("--progress-color", "#4f46e5");

    toggle.classList.remove("overall-mode");
    toggle.classList.add("today-mode");

    toggle.dataset.mode = "today";
    toggle.querySelector("span").textContent = "Today";
    toggle.querySelector("i").className = "bi bi-calendar3";
}

function showOverall(){

    circle.style.setProperty(
        "--progress",
        data.dataset.overallProgress + "%"
    );

    percent.textContent = data.dataset.overallProgress + "%";

    caption.textContent = "Overall completion";

    completed.textContent = data.dataset.overallCompleted;
    pending.textContent = data.dataset.overallPending;
    total.textContent = data.dataset.overallTotal;

    const msg = getOverallMessage(
        data.dataset.overallProgress
    );

    title.textContent = msg.title;
    message.textContent = msg.message;

    heading.textContent = "TODAY'S PROGRESS";

    headingIcon.className =
        "bi bi-calendar-check-fill text-primary me-2";

    subtitle.textContent =
        "Track today's productivity";

    circle.style.setProperty("--progress-color", "#16a34a");

    toggle.classList.remove("today-mode");
    toggle.classList.add("overall-mode");

    toggle.dataset.mode = "overall";
    toggle.querySelector("span").textContent = "Overall";
    toggle.querySelector("i").className = "bi bi-bar-chart";
}

toggle.addEventListener("click", function(){

    if(toggle.dataset.mode === "today"){
        showOverall();
    }
    else{
        showToday();
    }

});
toggle.classList.add("today-mode");