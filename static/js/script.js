/*
==========================================================
AI Real-Time IDS Dashboard
JavaScript
==========================================================
*/

// ==========================================================
// AUTO HIDE ALERTS
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition = "0.5s";

            alert.style.opacity = "0";

            setTimeout(function () {

                alert.remove();

            }, 500);

        }, 4000);

    });

});


// ==========================================================
// FILE INPUT NAME
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    const input = document.querySelector('input[type="file"]');

    if (!input) return;

    input.addEventListener("change", function () {

        if (this.files.length > 0) {

            console.log("Selected :", this.files[0].name);

        }

    });

});


// ==========================================================
// LOADING BUTTON
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", function () {

        const btn = form.querySelector("button");

        btn.disabled = true;

        btn.innerHTML =

            '<span class="spinner-border spinner-border-sm"></span> Predicting...';

    });

});


// ==========================================================
// CARD ANIMATION
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(

        ".stat-card,.feature-card,.upload-card,.info-card"

    );

    cards.forEach(function (card, index) {

        card.style.opacity = "0";

        card.style.transform = "translateY(30px)";

        setTimeout(function () {

            card.style.transition = "0.6s";

            card.style.opacity = "1";

            card.style.transform = "translateY(0px)";

        }, index * 120);

    });

});


// ==========================================================
// SMOOTH SCROLL
// ==========================================================

document.querySelectorAll("a[href^='#']").forEach(function (anchor) {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(

            this.getAttribute("href")

        );

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});


// ==========================================================
// PAGE LOADED
// ==========================================================

console.log(

    "AI Real-Time IDS Dashboard Loaded"

);