function emptyObj(keys){
    let obj = {};
    keys.forEach(key => {
        obj[key] = 0;
    });
    return obj;
}

function groupData(rows, value){
    let rollup = array => array[0]? value(array[0]) : 0;
    return d3.nest()
        .key(d => d.dataset.year)
        .key(d => d.dataset.name)
        .rollup(rollup)
        .object(rows);
}

function getStreamData(grouped, gnds, years){
    return years.map(year => Object.assign(emptyObj(gnds), grouped[year]));
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
    let svg = d3.select(container).append('svg');

    let legendItems = document.querySelectorAll('#camadas ul.legend [data-gnd]');
    let gnds = Array.from(legendItems, item => item.dataset.gnd);

    let getValue = row => +row.dataset.value;

    let cards = container.querySelectorAll('.card-wrapper:first-child .card');
    let years = Array.from(cards, card => card.dataset.year).sort();

    let executionSwitch = document.getElementById('executed-switch');
    let streamChart = new StreamChart(svg, years, gnds);

    executionSwitch.addEventListener('change', function(){
        let cardContainerClass = this.checked? 'orcado': 'empenhado';
        let cardContainerSelector = `.card-wrapper.${cardContainerClass}`;
        let rows = container.querySelectorAll(`${cardContainerSelector} .card tr`);
        let data = getStreamData(groupData(rows, getValue), gnds, years);
        let cardContainer = d3.select(cardContainerSelector);
        streamChart.render(data, cardContainer);
    });

    executionSwitch.dispatchEvent(new Event('change'));
})

function StreamChart(svg, years, gnds){
    const parentNode = svg.node().parentNode,
          getDimension = (node, attr) => parseFloat(getComputedStyle(node)[attr]),
          parentWidth = getDimension(parentNode, 'width'),
          parentHeight = 500;

    d3.select(parentNode).style('height', parentHeight + 'px');
    svg.attr('height', parentHeight)
       .style('left', 0)
       .style('right', 0)
       .style('position', 'absolute');

    const fullWidth = getDimension(svg.node(), 'width'),
          side = (fullWidth - parentWidth) / 2,
          margin = {top: 0, right: side, bottom: 40, left: side};

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

    const data = d3.range(x.domain()[0], x.domain()[1] + 1)

    const ticks = xAxis.selectAll('g.tick')
      .data(years)
      .enter().append('g')
      .attr('class', 'tick')
      .attr('transform', d => 'translate(' + x(d) + ',0)')

    ticks.append('line').attr('y2', - height)

    ticks.append('circle').attr('r', 4)

    const container = d3.selectAll('.stream-chart .card-wrapper');
    container.selectAll('.card')
        .data(years)
        .style('display', 'none')
        .style('position', 'absolute')
        .style('margin-left', function(d){
            const width = parseFloat(getComputedStyle(this)['width']);
            return - (width / 2) + 'px';
        })
        .style('left', d => (x(d) + margin.left) + 'px')
        .style('z-index', 2);

    ticks.append('text')
      .attr('stroke', 'none')
      .attr('dy', '1.5em')
      .text(d => d3.format("d")(d));

    this.render = function (data, cardContainer){
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

        const ticks = xAxis.selectAll('g.tick')
          .attr('class', d => 'tick year-' + d)
          .on('mouseover', function(d){
            xAxis.select('.active').dispatch('mouseout')
            d3.select(this).classed('active', true);
            cardContainer.select(`.card[data-year="${d}"]`).style('display', 'inline-block');
          })
          .on('mouseout', function(d){
            d3.select(this).classed('active', false);
            cardContainer.select(`.card[data-year="${d}"]`).style('display', 'none');
          })
        function mousemove(){
            let currYear;
            return function(){
                let xCoord = d3.mouse(this)[0] - margin.left;
                let year = Math.round(x.invert(xCoord));
                if(currYear == year) return;
                xAxis.select('.active').dispatch('mouseout')
                xAxis.select(`.year-${year}`).dispatch('mouseover')
            }
        }

        svg.on('mousemove', mousemove())
        .on('mouseout', function(d){
            xAxis.select('.active').dispatch('mouseout')
        })
        cardContainer.selectAll('.card').style('pointer-events', 'none');

        updateData(background, bgLayers, (d, i) => bgDomain[i], y);
        updateData(foreground, layers, (d, i) => x(i + x.domain()[0]), y);
    }
}
