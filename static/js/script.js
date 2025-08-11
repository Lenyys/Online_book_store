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
  // vybereme všechny odkazy s třídou .staff-link
  const staffLinks = document.querySelectorAll('.staff-link');
  const loginForm = document.querySelector('.login-form-container');

  staffLinks.forEach(link => {
    link.addEventListener('click', function (event) {
      const isAuthenticated = link.dataset.auth === 'true';
      const redirectUrl     = link.dataset.url;

      if (isAuthenticated) {
        // uživatel je přihlášený → klidně přejdeme
        window.location.href = redirectUrl;
      } else {
        // není přihlášený → zamezíme navigaci a zobrazíme přihlašovací formulář
        event.preventDefault();
        loginForm.classList.add('active');
      }
    });
  });
});


document.addEventListener('DOMContentLoaded', () => {
  const wrapper   = document.getElementById('search-wrapper');
  const input     = document.getElementById('search-input');
  const button    = document.getElementById('search-button');
  const suggList  = document.getElementById('suggestions');

  const searchUrl = wrapper.dataset.searchUrl;            // např. "/eshop/search/"
  const autoUrl   = wrapper.dataset.autocompleteUrl;      // např. "/eshop/autocomplete-search/"
  const detailTpl = wrapper.dataset.detailUrlTemplate;    // "/eshop/book_detail/0/"

  // 1) full‑textové vyhledávání
  button.addEventListener('click', () => {
    const q = input.value.trim();
    if (!q) return;
    window.location.href = `${searchUrl}?q=${encodeURIComponent(q)}`;
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      button.click();
    }
  });

  // 2) autocomplete
  input.addEventListener('input', () => {
    const q = input.value.trim();
    if (!q) {
      suggList.innerHTML = '';
      return;
    }

    fetch(`${autoUrl}?q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(json => {
        suggList.innerHTML = '';
        if (!json.results.length) {
          suggList.innerHTML = `<li class="list-group-item disabled">Žádné výsledky</li>`;
          return;
        }
        json.results.forEach(item => {
          const li = document.createElement('li');
          li.className = 'list-group-item list-group-item-action';
          li.textContent = item.name;
          li.addEventListener('click', () => {
            // nahradíme "0/" v šabloně za "<id>/"
            const url = detailTpl.replace(/0\/$/, `${item.id}/`);
            window.location.href = url;
          });
          suggList.appendChild(li);
        });
      });
  });
});


  window.addEventListener('load', function() {
    // Po 1 s skryjeme preloader, zobrazíme poděkování
    setTimeout(function() {
      document.getElementById('preloader').style.display = 'none';
      document.getElementById('order-thanks').style.display = 'block';
    }, 1000);
  });
