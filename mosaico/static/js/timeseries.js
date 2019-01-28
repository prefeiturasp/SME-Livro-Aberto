function toArray(nodeList){
    return [].slice.call(nodeList, 0)
}

window.addEventListener('load', function(){
    let rows = document.querySelectorAll('.timeseries tr');
    let cell = x => +(x.dataset.year || x.dataset.updated || x.dataset.paid);
    let row = x => toArray(x.children).map(cell)
    let data = toArray(rows).map(row);

    let container = d3.select('.timeseries');
    let parentWidth = realWidth(container.node());
    var margin = {top: 40, right: 80, bottom: 40, left: 40},
    width = parentWidth - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    let year = d => d[0];
    let serie1 = d => d[1];
    let serie2 = d => d[2];

    var color = d3.scaleQuantize()
        .domain([0, 1])
        .range(['updated', 'payed']);

    var x = d3.scaleLinear()
        .domain(d3.extent(data, year))
        .range([0, width]);

    let qtyYTicks = Math.ceil(d3.max(data, serie1) / 1000)
    let maxY = qtyYTicks * 1000
    let xTicks = d3.range(x.domain()[0], x.domain()[1])
    let yTicks = d3.range(0, maxY+1, maxY / 5)

    var y = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);

    let defined = d => d[0] && d[1] && d[2];

    let svg = container.append('svg').datum(data)
        .attr('height', height + margin.top + margin.bottom)
      .append('g')
        .attr('transform', 'translate(0,' + margin.top + ')');

    svg.append('g')
        .attr('class', 'axis axis--x')
        .attr('transform', 'translate(' + margin.left + ',' + height + ')')
        .call(d3.axisBottom(x).ticks(xTicks.length, 'i'));

    svg.append('g')
        .attr('class', 'axis axis--y')
        .call(d3.axisLeft(y)
                .tickSize(-parentWidth)
                .tickFormat(shortCurrency)
                .tickValues(yTicks))
        .selectAll('text').attr('dy', '-0.4em')
                           .attr('x', '0');

    [serie1, serie2].forEach(function(serie, i){
        var line = d3.line()
            .defined(defined)
            .curve(d3.curveMonotoneX)
            .x(d => x(year(d)))
            .y(d => y(serie(d)));

        let g = svg.append('g')
            .attr('class', 'serie_' + i)
            .attr('transform', 'translate(' + margin.left + ',0)')

        g.append('path')
            .attr('class', 'line')
            .classed(color(i), true)
            .attr('d', line);

        g.selectAll('.dot')
          .data(data.filter(defined))
          .enter().append('circle')
            .attr('class', 'dot')
            .classed(color(i), true)
            .attr('cx', line.x())
            .attr('cy', line.y())
            .attr('r', 3.5)
            .append('title').text(d => {
                return `Ano: ${year(d)}\nValor: ${currency(serie(d))}`;
            })
    });

    let legend = container.append('ul')
            .attr('class', 'legend')

    legend.append('li')
            .classed(color(1), true)
            .text('Valor empenhado')
    legend.append('li')
            .classed(color(0), true)
            .text('Valor atualizado')
    container.select('table').style('display', 'none')
})
