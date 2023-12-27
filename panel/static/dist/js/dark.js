document.querySelector('#btn1').style.display = "none"
      
function alerta()
{   //sidebar
    document.querySelector('#btn1').style.display = ""
    console.log('presionaste')
    document.querySelector('.left-sidebar').setAttribute("data-sidebarbg","skin5")
    document.querySelector('#btn2').style.display = "none"
    //navbar
    document.querySelector('#main-wrapper').setAttribute("data-navbarbg","skin5")
    document.querySelector('.topbar').setAttribute("data-navbarbg","skin5")
    document.querySelector('#navbarSupportedContent').setAttribute("data-navbarbg","skin5")
    //body
    document.querySelector('#body').setAttribute("data-theme","dark")
    //logo        
    document.querySelector('.navbar-header').style.background = "#1d2126"
    //document.querySelector('#navbar').classList.replace("navbar-light","navbar-dark")
}


function alerta2()
{   //sidebar
    document.querySelector('#btn2').style.display = ""
    document.querySelector('#btn1').style.display = "none"
    document.querySelector('.left-sidebar').setAttribute("data-sidebarbg","skin6")
    //sidebar
    document.querySelector('#main-wrapper').setAttribute("data-navbarbg","skin6")
    document.querySelector('.topbar').setAttribute("data-navbarbg","skin6")
    document.querySelector('#navbarSupportedContent').setAttribute("data-navbarbg","skin1")
    //body
    document.querySelector('#body').setAttribute("data-theme","light")
    //logo
    document.querySelector('.navbar-header').style.background = "#1e88e5"
    //document.querySelector('#navbar').classList.replace("navbar-dark","navbar-light")
}