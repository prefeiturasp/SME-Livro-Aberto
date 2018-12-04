function toArray(nodeList){
    return [].slice.call(nodeList, 0)
}

window.addEventListener('load', function(){
    let rows = document.querySelectorAll('.timeseries tr');
    let thSeries= rows[0].querySelectorAll('.serie')
    // let serieNames = toArray(thSeries).map(th => th.textContent);
    let cell = x => +(x.dataset.year || x.dataset.updated || x.dataset.paid);
    let row = x => toArray(x.children).map(cell)
    let data = toArray(rows).map(row);

    var margin = {top: 40, right: 40, bottom: 40, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    let year = d => d[0];
    let serie1 = d => d[1];
    let serie2 = d => d[2];

    var x = d3.scaleLinear()
        .domain(d3.extent(data, year))
        .range([0, width]);

    let qtyYTicks = Math.ceil(d3.max(data, serie1) / 1000)
    let maxY = qtyYTicks * 1000
    let yTicks = d3.range(0, maxY+1, maxY / 5)

    var y = d3.scaleLinear()
        .domain([0, maxY])
        .range([height, 0]);

    let defined = d => d[0] && d[1] && d[2];

    var svg = d3.select(".timeseries").append("svg")
        .datum(data)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    svg.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y).tickSize(-width).tickValues(yTicks));

    [serie1, serie2].forEach(function(serie){
        var line = d3.line()
            .defined(defined)
            .curve(d3.curveMonotoneX)
            .x(d => x(year(d)))
            .y(d => y(serie(d)));

        svg.append("path")
            .attr("class", "line")
            .attr("d", line);

        svg.selectAll(".dot")
          .data(data.filter(defined))
          .enter().append("circle")
            .attr("class", "dot")
            .attr("cx", line.x())
            .attr("cy", line.y())
            .attr("r", 3.5);
    });

    d3.select(".timeseries table").style('display', 'none')
})
