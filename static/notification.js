// ==========================
// NOTIFICATION PANEL
// ==========================

function toggleNotifications() {
    const panel = document.getElementById("notificationPanel");

    if (panel) {
        panel.classList.toggle("active");
    }
}


// ==========================
// CLOSE WHEN CLICKING OUTSIDE
// ==========================

document.addEventListener("click", function (event) {

    const wrapper = document.querySelector(".notification-wrapper");
    const panel = document.getElementById("notificationPanel");

    if (!wrapper || !panel) {
        return;
    }

    if (!wrapper.contains(event.target)) {
        panel.classList.remove("active");
    }

});


// ==========================
// ESCAPE KEY
// ==========================

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        const panel = document.getElementById("notificationPanel");

        if (panel) {
            panel.classList.remove("active");
        }

    }

});