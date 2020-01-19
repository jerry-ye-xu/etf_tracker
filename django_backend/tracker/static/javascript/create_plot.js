var price_data = {"1": {"low": {"2019-12-20": 279.7333, "2019-12-21": 279.7333, "2019-12-22": 279.7333, "2019-12-23": 281.1533, "2019-12-24": 282.57, "2019-12-25": 282.57, "2019-12-26": 286.06, "2019-12-27": 287.9933, "2019-12-28": 287.9933, "2019-12-29": 287.9933, "2019-12-30": 290.41, "2019-12-31": 291.6567, "2020-01-01": 291.6567, "2020-01-02": 295.1733, "2020-01-03": 297.1433, "2020-01-04": 297.1433, "2020-01-05": 297.1433, "2020-01-06": 299.1933, "2020-01-07": 298.54, "2020-01-08": 300.46, "2020-01-09": 303.7367, "2020-01-10": 307.7167, "2020-01-11": 307.7167, "2020-01-12": 307.7167, "2020-01-18": 307.7167}, "high": {"2019-12-20": 275.225, "2019-12-21": 275.225, "2019-12-22": 275.225, "2019-12-23": 276.933, "2019-12-24": 278.512, "2019-12-25": 278.512, "2019-12-26": 280.426, "2019-12-27": 282.26, "2019-12-28": 282.26, "2019-12-29": 282.26, "2019-12-30": 283.897, "2019-12-31": 285.276, "2020-01-01": 285.276, "2020-01-02": 287.27, "2020-01-03": 289.039, "2020-01-04": 289.039, "2020-01-05": 289.039, "2020-01-06": 291.017, "2020-01-07": 292.912, "2020-01-08": 294.831, "2020-01-09": 297.367, "2020-01-10": 299.409, "2020-01-11": 299.409, "2020-01-12": 299.409, "2020-01-18": 299.409}}, "2": {"low": {"2019-12-20": 54.046, "2019-12-21": 54.046, "2019-12-22": 54.046, "2019-12-23": 53.948, "2019-12-24": 53.85, "2019-12-25": 53.85, "2019-12-26": 53.808, "2019-12-27": 53.788, "2019-12-28": 53.788, "2019-12-29": 53.788, "2019-12-30": 53.69, "2019-12-31": 53.724, "2020-01-01": 53.724, "2020-01-02": 53.904, "2020-01-03": 53.892, "2020-01-04": 53.892, "2020-01-05": 53.892, "2020-01-06": 53.874, "2020-01-07": 53.912, "2020-01-08": 53.942, "2020-01-09": 53.882, "2020-01-10": 53.936, "2020-01-11": 53.936, "2020-01-12": 53.936, "2020-01-18": 53.936}, "high": {"2019-12-20": 52.6727, "2019-12-21": 52.6727, "2019-12-22": 52.6727, "2019-12-23": 52.707, "2019-12-24": 52.7457, "2019-12-25": 52.7457, "2019-12-26": 52.7957, "2019-12-27": 52.8567, "2019-12-28": 52.8567, "2019-12-29": 52.8567, "2019-12-30": 52.9083, "2019-12-31": 52.953, "2020-01-01": 52.953, "2020-01-02": 53.021, "2020-01-03": 53.0653, "2020-01-04": 53.0653, "2020-01-05": 53.0653, "2020-01-06": 53.124, "2020-01-07": 53.182, "2020-01-08": 53.2417, "2020-01-09": 53.295, "2020-01-10": 53.345, "2020-01-11": 53.345, "2020-01-12": 53.345, "2020-01-18": 53.345}}}

/*
First JSON.parse gets rid of the \"low\" etc.
Second JSON.parse converts it into an actual JSON object.
*/
// var fprice = JSON.parse(document.getElementById('fprices').textContent);
// var price_data = JSON.parse(fprice);

// var data_len = Object.keys(price_data["1"]["low"]).length
document.addEventListener('DOMContentLoaded', function(e) {

});

function drawChart(fund_id, data){
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#single_plot")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // Add X axis --> it is a date format
    var x = d3.scaleTime()
      .domain(d3.extent(data, function(d) { return d.date; }))
      .range([ 0, width ]);

    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) { return +d.value; })])
      .range([ height, 0 ]);

    svg.append("g")
      .call(d3.axisLeft(y));

    // Add the line
    svg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) { return x(d.date) })
        .y(function(d) { return y(d.value) })
        )
}

    //   // When reading the csv, I must format variables:
    //   function(d){
    //     return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
    //   },

    //   // Now I can use this dataset:
    //   function(data) {

    //     // Add X axis --> it is a date format
    //     var x = d3.scaleTime()
    //       .domain(d3.extent(data, function(d) { return d.date; }))
    //       .range([ 0, width ]);
    //     svg.append("g")
    //       .attr("transform", "translate(0," + height + ")")
    //       .call(d3.axisBottom(x));

    //     // Add Y axis
    //     var y = d3.scaleLinear()
    //       .domain([0, d3.max(data, function(d) { return +d.value; })])
    //       .range([ height, 0 ]);
    //     svg.append("g")
    //       .call(d3.axisLeft(y));

    //     // Add the line
    //     svg.append("path")
    //       .datum(data)
    //       .attr("fill", "none")
    //       .attr("stroke", "steelblue")
    //       .attr("stroke-width", 1.5)
    //       .attr("d", d3.line()
    //         .x(function(d) { return x(d.date) })
    //         .y(function(d) { return y(d.value) })
    //         )

    // })