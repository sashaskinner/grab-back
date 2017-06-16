        // map
        var width = 960,
            height = 700,
            centered;
        var projection = d3.geoAlbersUsa()
          .scale(1280)
          .translate([width / 2, height / 2]);
        var path = d3.geoPath()
          .projection(projection);
        d3.select("#map-container").append("h3")
            .attr("id", "currentYear")
            .text("Percent women in labor force in 2015");
        
        var svg = d3.select("#map-container").append("svg")
            .attr("width", width)
            .attr("height", height);
        svg.append("rect")
            .attr("class", "background")
            .attr("width", width)
            .attr("height", height)
            .on("click", clicked);
        var map_g = svg.append("g")
            .attr("id", "map");
        // make threshold bar key
        var formatPercent = d3.format(".0%"),
            formatNumber = d3.format(".0f");
        var x = d3.scaleLinear()
            .domain([0.1, 0.7])
            .range([0, 300]);
        var threshold = d3.scaleThreshold()
            .domain([0.20, 0.30, 0.40, 0.50, 0.60])
            .range(['#eff3ff','#c6dbef','#9ecae1','#6baed6','#3182bd','#08519c']);
        var key_g = svg.append("g")
            .attr("id", "key")
            .attr("transform", "translate(600, 15)");
        key_g.selectAll("rect")
          .data(threshold.range().map(function(color) {
            var d = threshold.invertExtent(color);
            if (d[0] == null) d[0] = x.domain()[0];
            if (d[1] == null) d[1] = x.domain()[1];
            return d;
          }))
          .enter().append("rect")
            .attr("height", 8)
            .attr("x", function(d) { return x(d[0]); })
            .attr("width", function(d) { return x(d[1]) - x(d[0]); })
            .attr("fill", function(d) { return threshold(d[0]); });
        key_g.append("text")
            .attr("class", "caption")
            .attr("x", x.range()[0])
            .attr("y", -6)
            .attr("fill", "#000")
            .attr("font-weight", "bold")
            .attr("text-anchor", "start")
            .text("% Women");
        key_g.call(d3.axisBottom(x)
              .tickSize(13)
              .tickFormat(function(x, i) { return x*100 + "%"; })
              .tickValues(threshold.domain()))
            .select(".domain")
              .remove();
    // minimum & maximum population values (default)
    var minimum = 0.28,
        maximum = 0.62;
    var color = d3.scaleLinear().domain([0.20, 0.30, 0.40, 0.50, 0.60])
                .range(['#eff3ff','#c6dbef','#9ecae1','#6baed6','#3182bd','#08519c']);
                // .range(['#eff3ff','#bdd7e7','#6baed6','#3182bd','#08519c']);
                // .range(['#edf8e9','#c7e9c0','#7bccc4','#74c476','#41ab5d','#238b45','#005a32']);
                // .range(['#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45','#005a32']);   
    
    // zoom function
    function clicked(d) {
        var x, y, k;
        if (d && centered !== d) {
          var centroid = path.centroid(d);
          x = centroid[0];
          y = centroid[1];
          k = 4;
          centered = d;
        } else {
          x = width / 2;
          y = height / 2;
          k = 1;
          centered = null;
        }
        map_g.selectAll("path")
            .classed("active", centered && function(d) { return d === centered; });
        map_g.transition()
            .duration(750)
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
            .style("stroke-width", 1.5 / k + "px");
    } 
    // load data
    queue()
        .defer(d3.json, "/us.json")
        .defer(d3.json, "/us-congress-113.json")
        .defer(d3.json, "/district-manager-info.json")
        .await(ready);
    // bind data to visual elements
    function ready(error, us, congress, district) {
      if (error) throw error;
      map_g.append("defs").append("path")
          .attr("id", "land")
          .datum(topojson.feature(us, us.objects.land))
          .attr("d", path);
      map_g.append("clipPath")
          .attr("id", "clip-land")
        .append("use")
          .attr("xlink:href", "#land");
          
      // congressional districts
      map_g.append("g")
          .attr("class", "districts")
          .attr("clip-path", "url(#clip-land)")
          .selectAll("path")
          .data(topojson.feature(congress, congress.objects.districts).features)
      .enter().append("path")
          .attr("d", path)
          .style("fill", function (d) {
            if (district[d.id]) {
              return color(district[d.id]); }
            else {
              return "#F2F3F4"; }
          })
          .on("click", clicked)
        // show congressional district id on hover
        .append("title")
          .text(function(d) { return d.id; });
      // draw district & state boundaries
      map_g.append("path")
          .attr("class", "district-boundaries")
          .datum(topojson.mesh(congress, congress.objects.districts,
            function(a, b) { return a !== b && (a.id / 1000 | 0) === (b.id / 1000 | 0); }))
          .attr("d", path);
      map_g.append("path")
          .attr("class", "state-boundaries")
          .datum(topojson.mesh(us, us.objects.states,
            function(a, b) { return a !== b; }))
          .attr("d", path);
      
        d3.select(self.frameElement).style("height", height + "px");
    }

  createRankChartManager();

  