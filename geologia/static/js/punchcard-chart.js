function toggleActive(selection){
    selection.classed('active', !selection.classed('active'));
}

window.addEventListener('load', function(){
    let punchcard = d3.select('.punchcard');
    let container = d3.select(punchcard.node().parentNode);
    let nav = container.select('aside');

    function updatePuchcard(actives){
        const bars = nav.node().querySelectorAll('tr.active .bar');

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
        const id =  new URL(this.href).hash
        nav.select('.card.active').classed('active', false);
        nav.selectAll('tr.active').classed('active', false);
        const curr = nav.select(id).classed('active', true)
        const first = curr.select('tr:first-child').dispatch('click');
        const second = d3.select(first.node().nextElementSibling).dispatch('click');
        d3.select(second.node().nextElementSibling).dispatch('click');
        d3.event.preventDefault();
      })
    nav.selectAll('tr')
       .style('cursor', 'pointer')
       .on('click', function(){
         const selection = d3.select(this);

         let actives = nav.node().querySelectorAll('tr.active');
         const crowded = ! selection.classed('active') && actives.length == 3;
         if(crowded) d3.select(actives[0]).call(toggleActive);
         const empty = selection.classed('active') && actives.length == 1;
         if(empty) return;

         selection.call(toggleActive);
         actives = nav.node().querySelectorAll('tr.active');
         updatePuchcard(actives);
       })
    nav.node().querySelector('header a').dispatchEvent(new Event('click'));
})
