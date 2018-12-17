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
