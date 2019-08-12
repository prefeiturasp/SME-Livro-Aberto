function toggleItem(target){
    let prevActive = target.parentNode.querySelector('.active');
    let active = target.classList.toggle('active');
    if(prevActive && active) prevActive.classList.remove('active');
    return active;
}

window.addEventListener('load', function(){
    let container = document.querySelector('#destino');
    let legendItems = container.querySelectorAll('.legend > li');
    for(let item of legendItems){
        item.addEventListener('click', function(){
            toggleItem(this);
            let bar = container.querySelector(`.value.fg-${this.dataset.slug}`);
            let active = toggleItem(bar);
            container.querySelector('.bar-parent').classList.toggle('selected', active);
        })
    }
})
