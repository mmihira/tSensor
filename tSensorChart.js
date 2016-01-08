/**
 * Generates the temperature chart.
 */

// app global variable 
tSensor = {};

/**
 * Format the text data into format usable by d3
 * The format looks like this :
 * {date:<date object>,value:<Float value of temperature in degrees>}
 */
tSensor.formatData = function(){

    var reg = /(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}),(.*)/

    tSensor.data = tData.map(function(e){
        var parsed = reg.exec(e);

        return {date:new Date(parsed[1],parseInt(parsed[2])-1,parsed[3],parsed[4],parsed[5],parsed[6]),
                value:parseFloat(parsed[7])/1000}

    });


};

// The responsive function to detect screen resolution and adapt accordingly
tSensor.responsive = function(){

    var dynWidth = window.innerWidth;

    var tickScale = d3.scale.linear()
                    .domain([300,1920])
                    .range([3,20]);

    if( dynWidth > 1920){
        tSensor.numberOfTicks = 20;
    }else{
        tSensor.numberOfTicks = parseInt(tickScale(dynWidth));
    }

    var maxFont = 22;
    var minFont = 10;
    var fontScale= d3.scale.linear()
                    .domain([300,1920])
                    .range([minFont,maxFont]);

    if( dynWidth > 1920){

        tSensor.fontSize= maxFont;
        tSensor.xfontSize = maxFont -2;

    }else{

        tSensor.fontSize = parseInt(fontScale(dynWidth));
        tSensor.xfontSize = parseInt(fontScale(dynWidth)) -2;

    }

    // Initialise the tempChart variables
    tSensor.jcWidth = dynWidth*.95;
    if(dynWidth < 500){

        tSensor.jcHeight = tSensor.jcWidth * 0.45;

    }else{

        tSensor.jcHeight = tSensor.jcWidth * 0.35;

    }

    // Let the margin take up 10% of the width (on both sides) 
    tSensor.jcMarginTopBot = dynWidth * 0.05;
    tSensor.jcMarginLeftRight = dynWidth * 0.1;


    // Initialise the tempChart variables
    tSensor.lngWidth = dynWidth*.95;
    if(dynWidth < 500){

        tSensor.lngHeight = tSensor.lngWidth * 0.45;

    }else{

        tSensor.lngHeight = tSensor.lngWidth * 0.35;

    }

    // Let the margin take up 10% of the width (on both sides) 
    tSensor.lngMarginTopBot = dynWidth * 0.05;
    tSensor.lngMarginLeftRight = dynWidth * 0.1;

    tSensor.legendRectSize = tSensor.lngWidth * .01;
    tSensor.legendSpacing = tSensor.legendRectSize/3;

};


// Create the main count chart
tSensor.tempChart = function(){
    
    var margin = {top: tSensor.jcMarginTopBot, 
                  right: tSensor.jcMarginLeftRight, 
                  bottom: tSensor.jcMarginTopBot, 
                  left: tSensor.jcMarginLeftRight},

        width = tSensor.jcWidth - margin.left - margin.right,
        height = tSensor.jcHeight - margin.top - margin.bottom;
    
    // How to parse the date value
    var parseDate = d3.time.format("%d/%m/%Y, %X %p").parse;
    
    var _data = tSensor.data.map(function(e){return {date:parseDate(e.date.toLocaleString()),value:e.value};});
    
      
    /***** Set up the axis *****/
    var x = d3.time.scale()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    // The format for the x-axis
    var xFormat = d3.time.format("%H:%M");

    var xAxis = d3.svg.axis()
        .scale(x)
        .tickFormat(xFormat)
        .ticks(tSensor.numberOfTicks)
        .orient("bottom");
    

    var yAxis = d3.svg.axis()
        .scale(y)
        .ticks(5)
        .orient("left");
    /**************************/

    /** Set up the svg **/

    $("#tChart").empty()
    var svg = d3.select("#tChart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("float","left")
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    var line = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.value); });
      
    /** Set up the x domain and the y domain **/
    x.domain(d3.extent(_data, function(d) { return d.date; }));
   
    y.domain([
        d3.min(_data , function(v) { return v.value; }),
        d3.max(_data , function(v) { return v.value; }) 
      ]);
    
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style('font-size',String(tSensor.xfontSize)+'px')
      .call(xAxis)
    .append("text")
      .attr("transform", "translate("+width+"," + 0 + ")")
      .attr("y",tSensor.xfontSize + 15 )
      .attr("dy", ".71em")
      .attr("font-size",String(tSensor.fontSize) + 'px')
      .attr("fill",'blue')
      .style("text-anchor", "end")
      .text("Time");


    svg.append("g")
      .attr("class", "y axis")
      .style('font-size',String(tSensor.fontSize)+'px')
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .attr("font-size",String(tSensor.fontSize) + 'px')
      .attr("fill",'blue')
      .style("text-anchor", "end")
      .text("Temperature('C)");

    svg.append("path")
        .attr("d",line(_data))
        .style({'stroke-width':'2px','stroke': 'red',fill:"none"});
};



