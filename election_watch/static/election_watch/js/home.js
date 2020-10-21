var navList = document.getElementById("nav-lists");
function Show() {
navList.classList.add("_Menus-show");
}

function Hide(){
navList.classList.remove("_Menus-show");
}

let result = document.querySelector('#result');
document.body.addEventListener('change', function (e) {
    let target = e.target;
    let message;
    switch (target.id) {
        case 'National':
            message = 'National';
            break;

        case 'Region':
            message = 'Region';
            break;
        
        case 'Constituency':
            message = 'Constituency';
            break;
    
    }
    result.textContent = message;
})

