function year(tr){
    return parseInt(tr.querySelector('[data-year]').dataset.year);
}

function value(tr){
    return parseFloat(tr.querySelector('[data-value]').dataset.value);
}

function name(tr){
    return tr.querySelector('[data-name]').dataset.name;
}

function item(tr){
    return {'year': year(tr), 'value': value(tr), 'name': name(tr)};
}

function emptyObj(keys){
    let obj = {};
    keys.forEach(key => {
        obj[key] = 0;
    });
    return obj;
}

window.addEventListener('load', function(){
    let container = document.querySelector('.stream-chart');
    let table = container.querySelector('table');
    let svg = d3.select(container).append('svg');
    let parentWidth = parseInt(getComputedStyle(svg.node())['width']);
    var margin = {top: 0, right: 0, bottom: 40, left: 0},
    width = parentWidth - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
    svg.attr('height', height + margin.top + margin.bottom);
    let grds = ['contributions', 'operational', 'previous', 'consulting',
              'realty', 'construction', 'people', 'outsourced'];

    let rows = document.querySelectorAll('.stream-chart tbody tr');

    stack = d3.stack()
        .keys(grds)
        .offset(d3['stackOffsetExpand'])

    let grouped = Array.from(rows, item).reduce(function(accumulator, curr){
        accumulator[curr.year] = accumulator[curr.year] || emptyObj(grds);
        accumulator[curr.year][curr.name] = curr.value;
        return accumulator;
    }, {});

    let data = []
    let years = []
    for(key in grouped){
        years.push(key)
        data.push(grouped[key])
    }
    const layers = stack(data)

    const x = d3.scaleLinear()
        .domain(d3.extent(years))
        .range([0, width]);

    const y = d3.scaleLinear()
        .range([height, 0])
        .domain([
            d3.min(layers, l => d3.min(l, d => d[0])),
            d3.max(layers, l => d3.max(l, d => d[1]))
        ]);

    const area = d3.area()
        .curve(d3.curveMonotoneX)
        .x((d, i) => x(i + x.domain()[0]))
        .y0(d => y(d[0]))
        .y1(d => y(d[1]));

    const path = svg.selectAll('path')
      .data(layers)
      .enter().append('path')
        .attr('d', area)
        .attr('class', d => d.key);

    table.style.display = 'none';
})
