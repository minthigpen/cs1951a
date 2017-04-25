var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 100};
var width = 960 - margin.right;
var height = 500 - margin.top - margin.bottom;

var xScale = d3.scaleLinear().domain([2011, 2015]).range([0, width]),
    yScale = d3.scaleLinear().domain([600, 2800]).range([height, 0]),
    colorScale = d3.scaleOrdinal(["#7116b0", "#03c942", "#7ebcb3", "#f18a72", "#08c6db", "#d7090d", "#8a97a4", "#18f8ff", "#f4325a", "#f4325a", "#cec755", "#7d6e44", "#6a2e26", "#31b3f6", "#2543e5", "#5926d9", "#ae992f", "#7ff16a", "#2ff634", "#5c4fb7", "#7d1c68", "#d2d844", "#683389", "#64b602", "#508527", "#e1adb7", "#bc2fc3", "#d34d8b", "#c94f07", "#f43ad5", "#025cc2", "#896f5c", "#5c7955", "#fbb375", "#af024c", "#fe8eb3", "#600ac4", "#bb5047", "#09435b", "#ca2acb", "#e33705", "#48cb93", "#a628db"]);

var xAxis = d3.axisBottom(xScale).ticks(5),
    yAxis = d3.axisLeft(yScale);

// Append the SVG container and set the origin
var svg = d3.select("#chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Append the x axis
svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "axis")
    .call(yAxis);

svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("transform", "translate(" + width + "," + (height - 5) + ")")
    .text("year");

svg.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("transform", "translate(7, -5)")
    .attr("transform", "rotate(270 7 -5)")
    .text("average median rent");


d3.csv("../data/median rent/averageMedianRentChangeBySubborough.csv", function (subboroughs) {
  svg.append("g")            
      .selectAll("path")
      .data(subboroughs)
      .enter()
      .append("path")
      .attr("class", "median rent change")
      .attr("d", function(d) { 
          var path = "";
          for (year of Object.keys(d)) {
            if (!isNaN(year)) {
              if (year == "2011") {
                path += ("M " + xScale(year) + " " + yScale(d[year]));
              } else {
                path += (" L " + xScale(year) + " " + yScale(d[year]));
              }  
            }
          }
          return path;
      })
      .attr("fill", "none")
      .attr("stroke", function(d) { return colorScale(d["subborough"]); });
});

    