function realWidth(container){
    return parseInt(getComputedStyle(container)['width']);
}

let pt_BR = {
  "decimal": ",",
  "thousands": ".",
  "grouping": [3],
  "currency": ["R$ ", ""]
}

d3.formatDefaultLocale(pt_BR);
let currency = d3.format('$,~d');

function shortCurrency(value){
    let SI = {
        'k':  ' mil',
        'M':  ' mi',
        'G':  ' bi',
    };
    formated = d3.format('$.2s')(value);
    for(si in SI){
        formated = formated.replace(si, SI[si])
    }
    return formated;
}

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
        if(form.go){
            form.go.remove();
            form.addEventListener('change', submit);
        }
    }
});
