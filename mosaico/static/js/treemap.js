window.addEventListener('load', function(event){
    let px = v => v + 'px';
    let value = d => d.dataset.value;

    var color = d3.scaleQuantize()
        .domain([0, 1])
        .range(['#e94363', '#f09564', '#edb93b', '#66d2b4', '#277fcd']);

    function each(f, iterable){
        for(let i = 0; i < iterable.length; i++){
            f(iterable[i]);
        }
    }

    function setNodeStyle(node){
        node.data.style.width = px(node.x1 - node.x0);
        node.data.style.height = px(node.y1 - node.y0)
        node.data.style.left = px(node.x0);
        node.data.style.top = px(node.y0);
        node.data.style.backgroundColor = color(node.data.dataset.execution);
        node.data.style.color = '#fff';
    }

    function setToolTip(node) {
        let tooltipDiv = document.querySelector("#tooltip");
        let width = window.innerWidth || 
                    document.documentElement.clientWidth || 
                    document.body.clientWidth;
        
        width /= 2;
        tooltipDiv.style.left = `${event.clientX + 15}px`;

        node.data.addEventListener("mousemove", event => {
            tooltipDiv.innerHTML = node.data.innerText.replace(/\n/g,'<br>');
            let tooltipWidth = parseInt(getComputedStyle(tooltipDiv)['width']);
            tooltipDiv.style.top = `${event.clientY - 15}px`;
            tooltipDiv.style.padding = "15px";

            if(event.clientX > width) {
                tooltipDiv.style.left = `${event.clientX - tooltipWidth - 40}px`;
            } else {
                tooltipDiv.style.left = `${event.clientX + 30}px`;
            }
        });
        node.data.addEventListener("mouseout", () => {
            tooltipDiv.innerHTML = "";
            tooltipDiv.style.padding = "0";
        });
    }

    let rootEl = document.querySelector('.treemap');
    let root = d3.hierarchy(rootEl, d => d.children);
    let width = parseInt(getComputedStyle(rootEl)['width']);
    let height = parseInt(getComputedStyle(rootEl)['height']);

    var treemap = d3.treemap()
        .tile(d3.treemapSquarify)
        .size([width, height])
        .padding(2);

    var nodes = treemap(root.sum(value)
                            .sort((a, b) => b.value - a.value));

    each(setNodeStyle, nodes.children)
    each(setToolTip,nodes.children)
})
