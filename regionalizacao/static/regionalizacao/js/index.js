function byLabel(a, b) {
    let nameA = a.dataset.label.toUpperCase();
    let nameB = b.dataset.label.toUpperCase();
    if (nameA < nameB) { return -1; }
    if (nameA > nameB) { return 1;  }
    return 0;
}

function byValue(a, b) {
    return b.dataset.value - a.dataset.value;
}

window.addEventListener("DOMContentLoaded", function(){
    document.querySelector('#localidade-order').addEventListener('change', function(){
        let barsEl = document.querySelectorAll('#localidade .barchart > .bar');
        let bars = Array.prototype.slice.call(barsEl);

        if(this.checked){
            bars.sort(byLabel)
        }else{
            bars.sort(byValue)
        }

        let barchart = document.querySelector('#localidade .barchart');
        barchart.style.position = 'relative';
        barchart.style.height = '20em';
        bars.forEach((bar, i) => {
            bar.style.position = 'absolute';
            bar.style.top = (5 * i) + 'em';
        });
        bars.forEach(bar => barchart.appendChild(bar));
        bars.forEach(bar => {
            bar.style.opacity = '1';
        });
    });
});
