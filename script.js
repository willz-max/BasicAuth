const myBody = document.querySelector('body');
const myform = document.querySelector('form');
const modes = document.querySelector('.modeToggler');
const modeTog = document.querySelector('.modeToggler div');
const aTags = document.querySelector('form p:last-child a');
const sun = document.querySelector('.sunny');
const moon = document.querySelector('.moon');







modes.addEventListener('click',()=>{
    myBody.classList.toggle('dark');
    if (myBody.classList.contains('dark')) {
        myform.classList.add('darkForm');
        aTags.style.color = "white";
        modeTog.classList.add('change');
        sun.classList.add('hide');
        moon.classList.remove('hide');
    }else{
        myform.classList.remove('darkForm');
        aTags.style.color = "";
        modeTog.classList.remove('change')
        moon.classList.add('hide');
        sun.classList.remove('hide');
    }
})

