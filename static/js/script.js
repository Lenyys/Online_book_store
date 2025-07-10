searchForm = document.querySelector('.search-from');

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.toggle('active')
}


window.onscroll=()=>{
    searchForm.classList.remove('active')
    if(window.scrollY > 80){
        document.querySelector('.header .header-2').classList.add('active')
    }
    else{
        document.querySelector('.header .header-2').classList.remove('active')
    }

}

window.onscroll=()=>{
    if(window.scrollY > 80){
        document.querySelector('.header .header-2').classList.add('active')
    }
    else{
        document.querySelector('.header .header-2').classList.remove('active')
    }

}