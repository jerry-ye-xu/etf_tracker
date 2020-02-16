// import * as d3 from '../../../node_modules/d3/d3.js';

// import * as d3 from 'd3';

// match first tag or all equivalent criteria.
// d3.select();
// d3.selectAll();

// d3.select('h1').style('color', 'red')
// .attr('class', 'heading')
// .text('Updated h1 tag')

var price_data = {"1": {"low": {"2019-12-20": 279.7333, "2019-12-21": 279.7333, "2019-12-22": 279.7333, "2019-12-23": 281.1533, "2019-12-24": 282.57, "2019-12-25": 282.57, "2019-12-26": 286.06, "2019-12-27": 287.9933, "2019-12-28": 287.9933, "2019-12-29": 287.9933, "2019-12-30": 290.41, "2019-12-31": 291.6567, "2020-01-01": 291.6567, "2020-01-02": 295.1733, "2020-01-03": 297.1433, "2020-01-04": 297.1433, "2020-01-05": 297.1433, "2020-01-06": 299.1933, "2020-01-07": 298.54, "2020-01-08": 300.46, "2020-01-09": 303.7367, "2020-01-10": 307.7167, "2020-01-11": 307.7167, "2020-01-12": 307.7167, "2020-01-18": 307.7167}, "high": {"2019-12-20": 275.225, "2019-12-21": 275.225, "2019-12-22": 275.225, "2019-12-23": 276.933, "2019-12-24": 278.512, "2019-12-25": 278.512, "2019-12-26": 280.426, "2019-12-27": 282.26, "2019-12-28": 282.26, "2019-12-29": 282.26, "2019-12-30": 283.897, "2019-12-31": 285.276, "2020-01-01": 285.276, "2020-01-02": 287.27, "2020-01-03": 289.039, "2020-01-04": 289.039, "2020-01-05": 289.039, "2020-01-06": 291.017, "2020-01-07": 292.912, "2020-01-08": 294.831, "2020-01-09": 297.367, "2020-01-10": 299.409, "2020-01-11": 299.409, "2020-01-12": 299.409, "2020-01-18": 299.409}}, "2": {"low": {"2019-12-20": 54.046, "2019-12-21": 54.046, "2019-12-22": 54.046, "2019-12-23": 53.948, "2019-12-24": 53.85, "2019-12-25": 53.85, "2019-12-26": 53.808, "2019-12-27": 53.788, "2019-12-28": 53.788, "2019-12-29": 53.788, "2019-12-30": 53.69, "2019-12-31": 53.724, "2020-01-01": 53.724, "2020-01-02": 53.904, "2020-01-03": 53.892, "2020-01-04": 53.892, "2020-01-05": 53.892, "2020-01-06": 53.874, "2020-01-07": 53.912, "2020-01-08": 53.942, "2020-01-09": 53.882, "2020-01-10": 53.936, "2020-01-11": 53.936, "2020-01-12": 53.936, "2020-01-18": 53.936}, "high": {"2019-12-20": 52.6727, "2019-12-21": 52.6727, "2019-12-22": 52.6727, "2019-12-23": 52.707, "2019-12-24": 52.7457, "2019-12-25": 52.7457, "2019-12-26": 52.7957, "2019-12-27": 52.8567, "2019-12-28": 52.8567, "2019-12-29": 52.8567, "2019-12-30": 52.9083, "2019-12-31": 52.953, "2020-01-01": 52.953, "2020-01-02": 53.021, "2020-01-03": 53.0653, "2020-01-04": 53.0653, "2020-01-05": 53.0653, "2020-01-06": 53.124, "2020-01-07": 53.182, "2020-01-08": 53.2417, "2020-01-09": 53.295, "2020-01-10": 53.345, "2020-01-11": 53.345, "2020-01-12": 53.345, "2020-01-18": 53.345}}}

var price_data_single = {"1":
        {"low": {
            "2019-12-20": 279.7333, "2019-12-21": 279.7333, "2019-12-22": 279.7333, "2019-12-23": 281.1533, "2019-12-24": 282.57, "2019-12-25": 282.57, "2019-12-26": 286.06, "2019-12-27": 287.9933, "2019-12-28": 287.9933, "2019-12-29": 287.9933, "2019-12-30": 290.41, "2019-12-31": 291.6567, "2020-01-01": 291.6567, "2020-01-02": 295.1733, "2020-01-03": 297.1433, "2020-01-04": 297.1433, "2020-01-05": 297.1433, "2020-01-06": 299.1933, "2020-01-07": 298.54, "2020-01-08": 300.46, "2020-01-09": 303.7367, "2020-01-10": 307.7167, "2020-01-11": 307.7167, "2020-01-12": 307.7167, "2020-01-18": 307.7167
        },
        "high": {
            "2019-12-20": 275.225, "2019-12-21": 275.225, "2019-12-22": 275.225, "2019-12-23": 276.933, "2019-12-24": 278.512, "2019-12-25": 278.512, "2019-12-26": 280.426, "2019-12-27": 282.26, "2019-12-28": 282.26, "2019-12-29": 282.26, "2019-12-30": 283.897, "2019-12-31": 285.276, "2020-01-01": 285.276, "2020-01-02": 287.27, "2020-01-03": 289.039, "2020-01-04": 289.039, "2020-01-05": 289.039, "2020-01-06": 291.017, "2020-01-07": 292.912, "2020-01-08": 294.831, "2020-01-09": 297.367, "2020-01-10": 299.409, "2020-01-11": 299.409, "2020-01-12": 299.409, "2020-01-18": 299.409
        }
    }}

// d3.select("#my_dataviz")

function strToDate(dateStr, sep="-") {
    // for some reason this is unreliable... you get some weird results
    // should double check this.
    dateArr = dateStr.split(sep)
    console.log("dateStr is " + dateStr)
    console.log("dateArr is " + dateArr)

    return new Date(dateStr)
}

// var svgWidth = 800; var svgHeight = 600;

function plotChart(
    fp_single, ticker_id,
    svgWidth, svgHeight,
    tag_id)
{

    /*
        EXTRACT PRICE DATA
    */

    fp_dates = Object.keys(fp_single[ticker_id]["low"]);
    fp_low = Object.values(fp_single[ticker_id]["low"]);
    fp_high = Object.values(fp_single[ticker_id]["high"]);

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
        top: 20,
        bottom: 30,
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

    g.append("path")
        .datum(fp_low_data)
        .attr("fill", "None")
        .attr("stroke", "steelblue")
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 1.5)
        .attr("d", line);

    g.append("path")
        .datum(fp_high_data)
        .attr("fill", "None")
        .attr("stroke", "steelblue")
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 1.5)
        .attr("d", line);

}

document.addEventListener("DOMContentLoaded", function(event) {
        plotChart(
            price_data_single, "1",
            svgWidth=800, svgHeight=450,
            tag_id="#my_dataviz"
        )
    }
);

// document.getElementbyId("fp_single").value = price_data_single

// console.log(price_data_single["1"])