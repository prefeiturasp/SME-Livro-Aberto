// Inspired by Lee Byron’s test data generator.
function bump(a, n) {
    const x = 1 / (0.1 + Math.random());
    const y = 2 * Math.random() - 0.5;
    const z = 10 / (0.1 + Math.random());
    for (let i = 0; i < n; ++i) {
        const w = (i / n - y) * z;
        a[i] += x * Math.exp(-w * w);
    }
}

function bumps(n, m) {
    const a = [];
    for (let i = 0; i < n; ++i) a[i] = 0;
    for (let i = 0; i < m; ++i) bump(a, n);
    return a;
}

window.addEventListener('load', function(){
    let container = document.querySelector('.stream-chart');
    let table = container.querySelector('table');
    let svg = d3.select(container).append('svg');
    let parentWidth = parseInt(getComputedStyle(svg.node())['width']);
    var margin = {top: 0, right: 0, bottom: 40, left: 0},
    width = parentWidth - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;
    svg.attr('height', height + margin.top + margin.bottom);

    let n = 4;
    let m = 15;
    let k = 10;
    let data = d3.transpose(Array.from({length: n}, () => bumps(m, k)));

    stack = d3.stack()
        .keys(d3.range(n))
        .offset(d3['stackOffsetExpand'])

    const x = d3.scaleLinear()
        .domain([0, m - 1])
        .range([0, width]);

    const layers = stack(data)

    const y = d3.scaleLinear()
        .range([height, 0])
        .domain([
            d3.min(layers, l => d3.min(l, d => d[0])),
            d3.max(layers, l => d3.max(l, d => d[1]))
        ]);

    const z = d3.scaleOrdinal()
          .domain(d3.range(n))
          .range(['investment', 'people', 'debt', 'other']);

    const area = d3.area()
        .curve(d3.curveMonotoneX)
        .x((d, i) => x(i))
        .y0(d => y(d[0]))
        .y1(d => y(d[1]));

    const path = svg.selectAll('path')
      .data(layers)
      .enter().append('path')
        .attr('d', area)
        .attr('class', (d, i) => z(i));

    table.style.display = 'none';
})
