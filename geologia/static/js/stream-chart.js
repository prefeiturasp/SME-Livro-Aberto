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

    let legendItems = document.querySelectorAll('#camadas ul.legend [data-gnd]');
    let gnds = Array.from(legendItems, item => item.dataset.gnd)
    let rows = document.querySelectorAll('.stream-chart tbody tr');

    stack = d3.stack()
        .keys(gnds)
        .offset(d3['stackOffsetExpand'])

    let grouped = Array.from(rows, row => row.dataset).reduce(function(accumulator, curr){
        accumulator[curr.year] = accumulator[curr.year] || emptyObj(gnds);
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

    const xAxis = svg.append("g")
        .attr('class', 'axis axis--x')
        .attr('font-size', '1em')
        .attr('text-anchor', 'middle')
        .attr('fill', 'currentColor')
        .attr('stroke', '#000')
        .attr('transform', 'translate(' + margin.left + ',' + height + ')')

    xAxis.append('line').attr('x2', x.range()[1])

    const ticks = xAxis.selectAll('g.tick')
      .data(years)
      .enter().append('g')
      .attr('class', 'tick')
      .attr('transform', d => 'translate(' + x(d) + ',0)')

    ticks.append('circle').attr('r', 4)

    ticks.append('text')
      .attr('stroke', 'none')
      .attr('dy', '1.5em')
      .text(d => d3.format("d")(d));

    table.style.display = 'none';
})
