navbar_user = document.querySelector(".navbar-user")
navbar_user_dropdown = document.querySelector(".user-dropdown")
let toggle_user_dropdown = function () {
    if (navbar_user_dropdown.className.includes("active")) {
        navbar_user_dropdown.classList.remove("active");
        document.querySelector(".navbar-user-top i").className = "bx bx-chevron-down"
    } else {
        navbar_user_dropdown.classList.toggle("active");
        document.querySelector(".navbar-user-top i").className = "bx bx-chevron-up"

    }
}

navbar_user.onclick = function () {
    toggle_user_dropdown()
}