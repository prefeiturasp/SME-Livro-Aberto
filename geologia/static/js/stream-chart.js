function emptyObj(keys){
    let obj = {};
    keys.forEach(key => {
        obj[key] = 0;
    });
    return obj;
}

function getStreamData(rows, gnds, executed){
    let grouped = Array.from(rows, row => row.dataset).reduce(function(accumulator, curr){
        accumulator[curr.year] = accumulator[curr.year] || emptyObj(gnds);
        accumulator[curr.year][curr.name] = curr.value;
        if(executed){
            accumulator[curr.year][curr.name] *= curr.execution;
        }
        return accumulator;
    }, {});

    let data = []
    let years = []
    for(key in grouped){
        years.push(key)
        data.push(grouped[key])
    }

    return {data: data, years: years}
}

function updateData(selection, layers, x, y){
    const area = d3.area()
        .curve(d3.curveMonotoneX)
        .x(x)
        .y0(d => y(d[0]))
        .y1(d => y(d[1]));

    selection.selectAll('path')
      .data(layers)
      .enter().append('path')
      .attr('class', d => d.key);

    selection.selectAll('path').transition().attr('d', area);
}

window.addEventListener('load', function(){
    let container = document.querySelector('.stream-chart');
    let table = container.querySelector('table');
    let svg = d3.select(container).append('svg');

    let legendItems = document.querySelectorAll('#camadas ul.legend [data-gnd]');
    let gnds = Array.from(legendItems, item => item.dataset.gnd);
    let rows = document.querySelectorAll('.stream-chart tbody tr');

    let executionSwitch = document.getElementById('executed-switch');
    let stream = getStreamData(rows, gnds, executionSwitch.checked);
    let streamChart = new StreamChart(svg, stream.years, gnds);
    streamChart.render(stream.data);

    executionSwitch.addEventListener('change', function(){
        let stream = getStreamData(rows, gnds, this.checked);
        streamChart.render(stream.data);
    });

    table.style.display = 'none';
})

function StreamChart(svg, years, gnds){
    const parentNode = svg.node().parentNode;
    let getDimension = (node, attr) => parseFloat(getComputedStyle(node)[attr]);
    let parentWidth = getDimension(parentNode, 'width');
    let parentHeight = 500;

    d3.select(parentNode).style('height', parentHeight + 'px');
    svg.attr('height', parentHeight)
       .style('left', 0)
       .style('right', 0)
       .style('position', 'absolute');

    let fullWidth = getDimension(svg.node(), 'width');
    let side = (fullWidth - parentWidth) / 2;
    let margin = {top: 0, right: side, bottom: 40, left: side};

    const height = parentHeight - margin.top - margin.bottom;

    const x = d3.scaleLinear()
        .domain(d3.extent(years))
        .range([0, parentWidth]);

    const background = svg.append("g")
        .attr('class', 'background')
        .style('opacity', 0.5)

    const foreground = svg.append("g")
        .attr('class', 'foreground')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

    const stack = d3.stack()
        .keys(gnds)
        .offset(d3['stackOffsetExpand'])

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

    this.render = function (data){
        const layers = stack(data);

        const y = d3.scaleLinear()
            .range([height, 0])
            .domain([
                d3.min(layers, l => d3.min(l, d => d[0])),
                d3.max(layers, l => d3.max(l, d => d[1]))
            ]);

        const bgData = [data[0], data[0], data[data.length - 1], data[data.length - 1]]
        const bgLayers = stack(bgData)
        const bgDomain = [0, side, parentWidth, fullWidth];

        updateData(background, bgLayers, (d, i) => bgDomain[i], y);
        updateData(foreground, layers, (d, i) => x(i + x.domain()[0]), y);
    }
}
