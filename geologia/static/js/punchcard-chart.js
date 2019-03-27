function toggleActive(selection){
    selection.classed('active', !selection.classed('active'));
}

window.addEventListener('load', function(){
    let punchcard = d3.select('.punchcard');
    let container = d3.select(punchcard.node().parentNode);
    let nav = container.selectAll('aside');

    function updatePuchcard(actives){
        const bars = actives[0].parentNode.querySelectorAll('tr.active .bar');

        const headers = container.selectAll('.column header').data(actives);
        headers.text(d => d.dataset.name);
        headers.exit().text('');

        const items = container.selectAll('.column').data(bars);
        items.enter().merge(items).classed('active', true)
        items.exit().classed('active', false)

        const percent = d => d.dataset.percent + '%';

        const gnds = items.selectAll('ul.axis .gnd')
            .data(d => d.querySelectorAll('.value'), function(d){return d ? d.dataset.name : this.dataset.gnd})
        gnds.style('height', percent)
            .style('width', percent)
        gnds.select('.percent').text(percent)
        gnds.select('.value').text(d => 'R$ ' + d.dataset.currencyValue)
        gnds.exit()
            .style('height', 0)
            .style('width', 0)
        gnds.exit().select('.percent').text('0%')
        gnds.exit().select('.value').text('R$ 0,00')
    }

    nav.selectAll('header a')
      .on('click', function(){
        const id =  new URL(this.href).hash;
        const curr = container.select(id);
        const prev = container.selectAll('.chart-set .card.active');
        prev.classed('active', false);
        prev.selectAll('tr.active').classed('active', false);
        curr.classed('active', true)

        const first = curr.select('tr:first-child');
        const second = d3.select(first.node().nextElementSibling);
        const third = d3.select(second.node().nextElementSibling);
        first.dispatch('click');
        second.dispatch('click');
        third.dispatch('click');

        d3.event.preventDefault();
      })
    nav.selectAll('tr')
       .style('cursor', 'pointer')
       .on('click', function(){
         const selection = d3.select(this);
         let actives = container.selectAll('tr.active');
         const crowded = ! selection.classed('active') && actives.size() == 3;
         if(crowded) d3.select(actives.node()).call(toggleActive);
         const empty = selection.classed('active') && actives.size() == 1;
         if(empty) return;

         selection.call(toggleActive);
         actives = container.selectAll('tr.active');
         updatePuchcard(actives.nodes());
       })

    d3.select('#por-subgrupo-filtro').on('change', function(){
        const container = d3.select('#por-subgrupo');
        container.select('.chart-set > :nth-child(1)').classed('active', this.checked);
        container.select('.chart-set > :nth-child(2)').classed('active', !this.checked);
        container.select('.chart-set > .active header a').dispatch('click');
        d3.event.preventDefault();
        d3.event.stopPropagation();
    }).dispatch('change');

})
