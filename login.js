const myBody = document.querySelector('body');
const myform = document.querySelector('form');
const modes = document.querySelector('.modeToggler');
const modeTog = document.querySelector('.modeToggler div');
const aTags = document.querySelectorAll('form button');
const sun = document.querySelector('.sunny');
const moon = document.querySelector('.moon');









modes.addEventListener('click',()=>{
    myBody.classList.toggle('dark');
    if (myBody.classList.contains('dark')) {
        myform.classList.add('bg-dark');
        myform.classList.add('border-light');
        myform.classList.remove('border-dark');
        aTags.forEach(element => {
        element.classList.add('btn-primary');
        element.classList.remove('btn-dark');
        });
        modeTog.classList.add('change');
        sun.classList.add('hide');
        moon.classList.remove('hide');
    }else{
        myform.classList.remove('bg-dark');
        myform.classList.remove('border-light');
        myform.classList.add('border-dark');
        aTags.forEach(element => {
        element.classList.remove('btn-primary');   
        element.classList.add('btn-dark');
        });   
        modeTog.classList.remove('change')
        moon.classList.add('hide');
        sun.classList.remove('hide');
    }
})

