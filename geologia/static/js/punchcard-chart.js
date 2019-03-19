function toggleActive(selection){
    selection.classed('active', !selection.classed('active'));
}

window.addEventListener('load', function(){
    let punchcard = d3.select('.punchcard');
    let container = d3.select(punchcard.node().parentNode);
    let nav = container.select('aside');
    nav.selectAll('header a')
      .on('click', function(){
        const id =  new URL(this.href).hash
        nav.select(`.card.active`).classed('active', false);
        nav.select(id).classed('active', true);
        d3.event.preventDefault();
      })
    nav.selectAll('tr')
       .style('cursor', 'pointer')
       .on('click', function(){
         const actives = nav.selectAll('tr.active');
           punchcard.selectAll('.column')
               .data(actives);
         d3.select(this).call(toggleActive);
       })
})
