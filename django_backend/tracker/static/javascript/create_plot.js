function strToDate(dateStr, sep="-") {
    // for some reason this is unreliable... you get some weird results
    // should double check this.

    console.log(new Date(dateStr))

    return new Date(dateStr)
}

function plotChart(
    fp_single, ticker_id,
    svgWidth, svgHeight,
    tag_id)
{

    /*
        EXTRACT PRICE DATA
    */

    fp_dates = Object.keys(fp_single["low"]);
    fp_low = Object.values(fp_single["low"]);
    fp_high = Object.values(fp_single["high"]);

    console.log(fp_dates)

    // We see later we can use d3.extent() to return min and max.
    max_price = Math.max(...fp_low.concat(fp_high));
    min_price = Math.min(...fp_low.concat(fp_high));

    var fp_low_data = [];
    var fp_high_data = [];

    // for (var i = 0; i < fp_dates.length; i++){
    //     fp_low_data.push({
    //         date: strToDate(fp_dates[i], sep="-"), value: fp_low[i]
    //     })
    //     fp_high_data.push({
    //         date: strToDate(fp_dates[i], sep="-"), value: fp_high[i]
    //     })
    // }
    for (var i = 0; i < fp_dates.length; i++){
        fp_low_data.push({
            date: strToDate(fp_dates[i]), value: fp_low[i]
        })
        fp_high_data.push({
            date: strToDate(fp_dates[i]), value: fp_high[i]
        })
    }

    console.log(fp_low_data)

    /*
        MARGINS
    */

    var margin = {
        top: 50,
        bottom: 60,
        right: 20,
        left: 50
    }

    var width = svgWidth - margin.left - margin.right
    var height = svgHeight - margin.top - margin.bottom

    /*
        SCALES AND AXIS
    */

    // var xScale = d3.scaleLinear()
    //     .domain([0, fp_dates.length])
    //     .range([0, svgWidth]);

    // var yScale = d3.scaleLinear()
    //     .domain([min_price * 0.8, max_price])
    //     .range([svgHeight, 0]);

    var xScale = d3.scaleTime()
        .rangeRound([0, width]);

    var yScale = d3.scaleLinear()
        .rangeRound([height, 0]);

    /*
        CREATE THE OBJECT
    */

    var svg = d3.select(tag_id)
        .attr("width", svgWidth)
        .attr("height", svgHeight);

    var line = d3.line()
        .x(function(d) {return xScale(d.date)})
        .y(function(d) {return yScale(d.value)});

    yScale.domain(
        d3.extent(fp_low.concat(fp_high))
    );
    xScale.domain(
        d3.extent(fp_dates.map(strToDate))
    );
    console.log(fp_dates.map(strToDate))

    /*
        translate(a, b), as value increases, we have
        a: is L -> R
        b: is U -> D

        behaviour for x-axis and y-axis is the same.
    */

    // svg.append('g')
    //     .attr("transform", "translate(50, -17.5)")
    //     .call(y_axis)

    // svg.append('g')
    //     .attr("transform", "translate(50, -17.5)")
    //     .call(x_axis)

    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x_axis = d3.axisBottom()
        .scale(xScale);
    var y_axis = d3.axisLeft()
        .scale(yScale);

    g.append("g")
        .attr("transform", "translate(0, " + height + ")")
        .call(x_axis);

    g.append("g")
        .call(y_axis);

    /*
        CREATE LINES AND DOTS
    */

    /*

    is-info: #209CEE
    is-link: #3273DC
    is-primary: #00D1B2
    is-warning: #FFFF03
    is-black-ter: #242424

    */

    g.append("path")
        .datum(fp_low_data)
        .attr("fill", "None")
        .attr("stroke", "#00D1B2")
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 2.5)
        .attr("d", line);

    g.append("path")
        .datum(fp_high_data)
        .attr("fill", "None")
        .attr("stroke", "#242424")
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 2.5)
        .attr("d", line);

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 65)
      .attr("x", -40 - (height/2))
      // .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Price ($ US)");

    svg.append("text")
      .attr("transform", "translate(" + (width/2 + 50) + " ," + (height + margin.top + 40) + ")")
      .style("text-anchor", "middle")
      .text("Date");

}

/*
First JSON.parse gets rid of the \"low\" etc.
Second JSON.parse converts it into an actual JSON object.
*/
var fprice = JSON.parse(document.getElementById('fprices').textContent);
var price_data = JSON.parse(fprice);

document.addEventListener('DOMContentLoaded', function(e) {
    /*
    First JSON.parse gets rid of the \"low\" etc.
    Second JSON.parse converts it into an actual JSON object.
    */
    var fprice = JSON.parse(document.getElementById('fprices').textContent);
    var price_data = JSON.parse(fprice);

    fund_id = Object.keys(price_data)

    console.log(fund_id)

    fund_id.forEach(function(fund_id){
        plotChart(
          price_data[fund_id], fund_id,
          488, 366, "#ticker_" + fund_id
        )
    });
});