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
    var form = document.forms.filter;
    function submit(){ form.submit(); }

    form.fonte.addEventListener('change', submit);
    form.year.addEventListener('change', submit);

    form.go.remove();

    function goToValue(){ console.log(this); window.location = this.dataset.href; }
    document.getElementById('simple').addEventListener('change', goToValue);
    document.getElementById('pro').addEventListener('change', goToValue);
});
