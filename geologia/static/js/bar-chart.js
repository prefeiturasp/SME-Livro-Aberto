window.addEventListener('load', function(){
    let barchart = d3.select('table.bar-chart');
    let container = d3.select(barchart.node().parentNode);
    barchart.selectAll('tr')
      .style('cursor', 'pointer')
      .on('click', function(){
        const year = this.dataset.year;
        if(!year) return;
        container.select(`.card.active`).classed('active', false);
        container.select(`.card[data-year="${year}"]`).classed('active', true);
      })
    d3.selectAll('table.bar-chart a').on('click', function(){
        d3.event.preventDefault();
    });
})
