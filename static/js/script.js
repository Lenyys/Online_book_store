searchForm = document.querySelector('.search-form');
document.querySelector('#search-btn').onclick = () => {
    searchForm.classList.toggle('active');
};

let loginForm = document.querySelector('.login-form-container');

document.querySelector('#login-btn').onclick = (event) => {
    const isAuthenticated = loginBtn.dataset.auth === "true";

    if (isAuthenticated) {
        // Přihlášený → zobrazit dropdown
        dropdown.classList.toggle('show');
        event.stopPropagation(); // aby nezmizel hned
    } else {
        // Nepřihlášený → zobrazit přihlašovací formulář
        loginForm.classList.toggle('active');
    }
};

document.querySelector('#close-login-btn').onclick = () => {
    loginForm.classList.remove('active');
};

// První onscroll (ponechána duplicita)
window.onscroll = () => {
    searchForm.classList.remove('active');
    if (window.scrollY > 80) {
        document.querySelector('.header .header-2').classList.add('active');
    } else {
        document.querySelector('.header .header-2').classList.remove('active');
    }
};

// Druhá onscroll (taky nechána jak jsi chtěl)
window.onscroll = () => {
    if (window.scrollY > 80) {
        document.querySelector('.header .header-2').classList.add('active');
    } else {
        document.querySelector('.header .header-2').classList.remove('active');
    }
};

// 🔥 Přihlášený uživatel – změna ikony + dropdown menu
window.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.getElementById('login-btn');
    const dropdown = document.getElementById('user-dropdown-menu');
    const isAuthenticated = loginBtn.dataset.auth === "true";

    if (isAuthenticated) {
        loginBtn.classList.add('authenticated');
        loginBtn.title = loginBtn.dataset.username;
    } else {
        loginBtn.title = "Nikdo není přihlášen";
    }

    loginBtn.addEventListener('click', function (event) {
        event.stopPropagation();
        if (isAuthenticated) {
            dropdown.classList.toggle('show');
        } else {
            loginForm.classList.add('active');
        }
    });

    window.addEventListener('click', function () {
        dropdown.classList.remove('show');
    });
});


window.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.login-message p');

    messages.forEach(msg => {
        if (msg.textContent.includes('Přihlášení bylo úspěšné')) {
            setTimeout(() => {
                window.location.href = '/';  // nebo tvá konkrétní url
            }, 2000);
        }
    });
});

var swiper = new Swiper(".books-slider", {
    loop: true,
    centeredSlides: true,
    autoplay: {
        delay: 9500,
        disableOnInteraction: false,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});


var swiper1 = new Swiper(".featured-slider", {
    spaceBetween: 10,
    loop: true,
    centeredSlides: true,
    autoplay: {
        delay: 9500,
        disableOnInteraction: false,
    },
        navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        450: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 3,
        },
        1024: {
            slidesPerView: 4,
        },
    },
});



var swiper2 = new Swiper(".arrivals-slider", {
    spaceBetween: 10,
    loop: true,
    centeredSlides: true,
    autoplay: {
        delay: 9500,
        disableOnInteraction: false,
    },

    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});

var swiper2 = new Swiper(".reviews-slider", {
    spaceBetween: 10,
    grabCursor:true,
    loop: true,
    centeredSlides: true,
    autoplay: {
        delay: 9500,
        disableOnInteraction: false,
    },

    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
})

var swiper2 = new Swiper(".blogs-slider", {
    spaceBetween: 10,
    grabCursor:true,
    loop: true,
    centeredSlides: true,
    autoplay: {
        delay: 9500,
        disableOnInteraction: false,
    },

    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});;


document.addEventListener('DOMContentLoaded', function () {
    const bookListLink = document.getElementById('book-list-link');
    let loginForm = document.querySelector('.login-form-container');

    bookListLink.addEventListener('click', function (event) {
        const isAuthenticated = bookListLink.getAttribute('data-auth') === 'true';
        const redirectUrl = bookListLink.getAttribute('data-url');

        if (isAuthenticated) {
            window.location.href = redirectUrl;
        } else {
            event.preventDefault();
            loginForm.classList.add('active');
        }
    });
});