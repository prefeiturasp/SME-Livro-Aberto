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
    function submit(eventHandler){
        let form = eventHandler.currentTarget;
        let input = eventHandler.target;
        if(input.name == 'simples')
            window.location = input.dataset.href;
        else
            form.submit();
    }
    for(form of document.forms){
        form.go.remove();
        form.addEventListener('change', submit);
    }
});
