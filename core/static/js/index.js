function realWidth(container){
    return parseInt(getComputedStyle(container)['width']);
}

let pt_BR = {
  "decimal": ",",
  "thousands": ".",
  "grouping": [3],
  "currency": ["R$", ""]
}

d3.formatDefaultLocale(pt_BR);
let currency = d3.format('$,~d');

window.addEventListener("DOMContentLoaded", function(){
    function submit(){ form.submit(); }
    for(form of document.forms){
        form.go.remove();
        form.addEventListener('change', submit);
    }

    function goToValue(){ console.log(this); window.location = this.dataset.href; }
    document.getElementById('simple').addEventListener('change', goToValue);
    document.getElementById('pro').addEventListener('change', goToValue);
});
