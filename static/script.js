// =========================================
// DATE & TIME
// =========================================

function updateDateTime() {

    const now = new Date();

    const element = document.getElementById("dateTime");

    if (element) {
        element.textContent = now.toLocaleString();
    }
}

updateDateTime();
setInterval(updateDateTime, 1000);



// =========================================
// DARK / LIGHT MODE
// =========================================

function applyTheme() {

    const theme = localStorage.getItem("theme");

    const html = document.documentElement;

    const body = document.body;

    const buttons = document.querySelectorAll(".theme-btn");


    // Remove loading class
    html.classList.remove("dark-loading");


    if (theme === "dark") {

        html.classList.add("dark");

        body.classList.add("dark");


        buttons.forEach(function(button) {

            const icon =
                button.querySelector(".theme-icon");

            const text =
                button.querySelector(".theme-text");


            if (icon) {
                icon.textContent = "☀️";
            }

            if (text) {
                text.textContent = "Light Mode";
            }

        });


    } else {

        html.classList.remove("dark");

        body.classList.remove("dark");


        buttons.forEach(function(button) {

            const icon =
                button.querySelector(".theme-icon");

            const text =
                button.querySelector(".theme-text");


            if (icon) {
                icon.textContent = "🌙";
            }

            if (text) {
                text.textContent = "Dark Mode";
            }

        });

    }
}



// =========================================
// TOGGLE THEME
// =========================================

function toggleTheme() {

    const currentTheme =
        localStorage.getItem("theme");


    if (currentTheme === "dark") {

        // DARK → LIGHT
        localStorage.setItem(
            "theme",
            "light"
        );

    } else {

        // LIGHT → DARK
        localStorage.setItem(
            "theme",
            "dark"
        );

    }


    applyTheme();

}



// =========================================
// APPLY SAVED THEME
// =========================================

applyTheme();



// =========================================
// PROFILE SIDEBAR
// =========================================

function openProfile() {

    const sidebar =
        document.getElementById("profileSidebar");

    const overlay =
        document.getElementById("profileOverlay");


    if (sidebar) {
        sidebar.classList.add("active");
    }


    if (overlay) {
        overlay.classList.add("active");
    }

}



// =========================================
// CLOSE PROFILE
// =========================================

function closeProfile() {

    const sidebar =
        document.getElementById("profileSidebar");

    const overlay =
        document.getElementById("profileOverlay");


    if (sidebar) {
        sidebar.classList.remove("active");
    }


    if (overlay) {
        overlay.classList.remove("active");
    }

}



// =========================================
// ESCAPE KEY
// =========================================

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Escape") {

            closeProfile();

        }

    }
);