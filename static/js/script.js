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


/*



document.addEventListener("DOMContentLoaded", () => {
  const input       = document.getElementById("search-input");
  const btn         = document.getElementById("search-button");
  const suggList    = document.getElementById("suggestions");
  const baseSearch  = "{% url 'book_list' %}";      // Django URL pro vaši list view
  const autoUrl     = "/eshop/autocomplete-search/"; // endpoint pro autocomplete

  // 1) Odeslat vyhledávání
  function doSearch() {
    const q = input.value.trim();
    if (!q) return;
    // přesměrujeme na adresu: /book_list/?q=...
    window.location.href = `${baseSearch}?q=${encodeURIComponent(q)}`;
  }

  // klik na lupičku
  btn.addEventListener("click", doSearch);

  // stisk Enter v poli
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      doSearch();
    }
  });


  // 2) Autocomplete – vyplníme suggList
  input.addEventListener("input", () => {
    const q = input.value.trim();
    // pokud prázdné, smažeme a končíme
    if (q.length < 1) {
      suggList.innerHTML = "";
      return;
    }

    fetch(`${autoUrl}?q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(data => {
        suggList.innerHTML = "";
        // žádné výsledky
        if (!data.results || data.results.length === 0) {
          const li = document.createElement("li");
          li.className = "list-group-item disabled";
          li.textContent = "Žádné výsledky";
          suggList.appendChild(li);
          return;
        }
        // naplnit seznam
        data.results.forEach(item => {
          const li = document.createElement("li");
          li.className = "list-group-item list-group-item-action";
          li.textContent = item;
          // klik na jednu z položek
          li.addEventListener("click", () => {
            input.value = item;
            suggList.innerHTML = "";
            doSearch();
          });
          suggList.appendChild(li);
        });
      })
      .catch(err => {
        console.error("Autocomplete chyba:", err);
        suggList.innerHTML = "";
      });
  });

  // 3) schovat autocomp když kliknu mimo
  document.addEventListener("click", e => {
    if (!document.getElementById("search-wrapper").contains(e.target)) {
      suggList.innerHTML = "";
    }
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const input    = document.getElementById("search-input");
  const btn      = document.getElementById("search-button");
  const suggList = document.getElementById("suggestions");

  // URL k vaší search view a autocomplete endpoint
  const baseSearch = "{% url 'book_list' %}";      // nebo "/eshop/" dle nastavení
  const autoUrl    = "/eshop/autocomplete-search/";

  // Pomocná funkce pro odeslání
  function doSearch() {
    const q = input.value.trim();
    if (!q) return;
    window.location.href = `${baseSearch}?q=${encodeURIComponent(q)}`;
  }

  // 1) ENTER v inputu
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      doSearch();
    }
  });

  // 2) klik na lupičku
  btn.addEventListener("click", doSearch);

  // 3) autocomplete – načítání návrhů
  input.addEventListener("input", () => {
    const q = input.value.trim();
    if (q.length < 1) {
      suggList.innerHTML = "";
      return;
    }

    fetch(`${autoUrl}?q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(data => {
        suggList.innerHTML = "";

        if (!Array.isArray(data.results) || data.results.length === 0) {
          const li = document.createElement("li");
          li.className = "list-group-item disabled";
          li.textContent = "Žádné výsledky";
          suggList.appendChild(li);
          return;
        }

        data.results.forEach(item => {
          const li = document.createElement("li");
          li.className = "list-group-item list-group-item-action";
          li.textContent = item;
          li.addEventListener("click", () => {
            input.value = item;
            suggList.innerHTML = "";
            doSearch();
          });
          suggList.appendChild(li);
        });
      })
      .catch(err => {
        console.error("Autocomplete chyba:", err);
      });
  });

  // 4) klik mimo – schovat návrhy
  document.addEventListener("click", e => {
    if (!document.getElementById("search-wrapper").contains(e.target)) {
      suggList.innerHTML = "";
    }
  });
});
*/
/*
document.addEventListener('DOMContentLoaded', () => {
  const wrapper    = document.getElementById('search-wrapper');
  const input      = document.getElementById('search-input');
  const button     = document.getElementById('search-button');
  const suggestions= document.getElementById('suggestions');
  const searchUrl  = wrapper.dataset.searchUrl;
  const autoUrl    = wrapper.dataset.autocompleteUrl;

  // Když kliknu na lupičku, přesměruju na ?q=…
  button.addEventListener('click', () => {
    const q = input.value.trim();
    if (q) window.location.href = `${searchUrl}?q=${encodeURIComponent(q)}`;
  });

  // Enter v inputu se chová stejně jako klik na tlačítko
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      button.click();
    }
  });

  // Autocomplete při zadávání
  input.addEventListener('input', () => {
    const q = input.value.trim();
    if (q.length < 1) {
      suggestions.innerHTML = '';
      return;
    }
    fetch(`${autoUrl}?q=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(data => {
        suggestions.innerHTML = '';
        if (!data.results.length) {
          suggestions.innerHTML = `
            <li class="list-group-item disabled">Žádné výsledky</li>`;
          return;
        }
        data.results.forEach(item => {
          const li = document.createElement('li');
          li.className = 'list-group-item list-group-item-action';
          li.textContent = item;
          li.addEventListener('click', () => {
            input.value = item;
            suggestions.innerHTML = '';
            button.click();
          });
          suggestions.appendChild(li);
        });
      });
  });
});
*//*
document.addEventListener('DOMContentLoaded', () => {
  const wrapper     = document.getElementById('search-wrapper');
  const input       = document.getElementById('search-input');
  const button      = document.getElementById('search-button');
  const suggestions = document.getElementById('suggestions');
 const searchUrl   = wrapper.dataset.searchUrl;          // např. "/eshop/search/"
  const detailUrl   = wrapper.dataset.detailUrlTemplate;  // nově: "/eshop/book_detail/{id}/"
  const autoUrl     = wrapper.dataset.autocompleteUrl;    // např. "/eshop/autocomplete-search/"
 // URL pro detail, získaná s pomocí Django tagu:
  const detailBase  = '{% url "book_detail" 0 %}'.replace(/0\/$/, '');

  // klasické zadání do výsledků full‑textového vyhledávání
  button.addEventListener('click', () => {
    const q = input.value.trim();
    if (q) window.location.href = `${wrapper.dataset.searchUrl}?q=${encodeURIComponent(q)}`;
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      button.click();
    }
  });

 // autocomplete
  input.addEventListener('input', () => {
    const q = input.value.trim();
    if (!q) {
      suggestions.innerHTML = '';
      return;
    }
    fetch(`${autoUrl}?q=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(json => {
        suggestions.innerHTML = '';
        if (!json.results.length) {
          suggestions.innerHTML = `
            <li class="list-group-item disabled">Žádné výsledky</li>`;
          return;
        }
        json.results.forEach(item => {
          const li = document.createElement('li');
          li.className = 'list-group-item list-group-item-action';
          li.textContent = item.name;
          // tady už nepřepisujeme input, ale rovnou jdeme na detail:
          li.addEventListener('click', () => {
            window.location.href = detailUrl.replace('{id}', item.id);
          });
          suggestions.appendChild(li);
        });
      });
  });
});*/
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
