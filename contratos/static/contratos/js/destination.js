window.addEventListener('beforeunload', function(){
    let container = document.querySelector('#destino');
    let legendItems = container.querySelectorAll('.legend > li');
    for(let item of legendItems){
        item.classList.toggle('active', false);
        container.querySelector('.bar-parent').classList.toggle('selected', false);
    }
})
