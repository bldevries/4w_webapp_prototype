

function make_scatter_plot(data, tag_id, xlabel, ylabel, x_width, y_height, tooltips) {


    var margin = {top: 20, right: 155, bottom: 60, left: 80}
      , width = x_width - margin.left - margin.right
      , height = y_height - margin.top - margin.bottom;

    var x = d3.scaleLinear()//scale.linear()
              .domain([0, d3.max(data, function(d) { return d[0]; })])
              .range([ 0, width ]);

    var y = d3.scaleLinear()//scale.linear()
              .domain([0, d3.max(data, function(d) { return d[1]; })])
              .range([ height, 0 ]);

    // var chart = d3.select('body')
    var chart = d3.select("#".concat(tag_id))//graph1")
    .append('svg:svg')
    .attr('width', width + margin.right + margin.left)
    .attr('height', height + margin.top + margin.bottom)
    .attr('class', 'chart')

    var main = chart.append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
    .attr('width', width)
    .attr('height', height)
    .attr('class', 'main')   
        
    // draw the x axis
    // var xAxis = d3.svg.axis()
    // .scale(x)
    // .orient('bottom');

    var xAxis = d3.axisBottom().scale(x)

    main.append('g')
    .attr('transform', 'translate(0,' + height + ')')
    .attr('class', 'main axis date')
    .call(xAxis)
    .append("text")
    .attr("y", 40)
    .attr("x", width)
    .attr("text-anchor", "end")
    .attr("stroke", "black")
    .text(xlabel);

    // draw the y axis
    var yAxis = d3.axisLeft().scale(y)
    // var yAxis = d3.svg.axis()
    // .scale(y)
    // .orient('left');

    main.append('g')
    .attr('transform', 'translate(0,0)')
    .attr('class', 'main axis date')
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", "-5.1em")
    .attr("text-anchor", "end")
    .attr("stroke", "black")
    .text(ylabel);//Email length (characters)");

    var g = main.append("svg:g"); 


    // Add the tooltip for the graph!
    var div = d3.select("body").append("div")   
        .attr("class", "tooltip")               
        .style("opacity", 0);

    g.selectAll("scatter-dots")
        .data(data)
        .enter().append("svg:circle")
            .attr("cx", function (d,i) { return x(d[0]); } )
            .attr("cy", function (d) { return y(d[1]); } )
            .attr("r", 4)
            .on("mouseover", function(d,i){
                d3.select(this)
                    .style("fill", "orange");
                div.transition()        
                    .duration(200)      
                    .style("opacity", .9);
                div .html(tooltips[i])//String(d[0]).concat(", ").concat(d[1]))
                    .style("left", (d3.event.pageX) + "px")     
                    .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function(){
                d3.select(this)
                    .style("fill", "steelblue")
                div.transition()        
                    .duration(500)      
                    .style("opacity", 0);  
            });
          
}