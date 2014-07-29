/**
 * Created by dtgillis on 6/8/14.
 */




function getRawPlots() {

    var vqtl = $("#varQtl").val();
    var software = $("#software").val();
    var snpConfig = $("#snp_config").val();

    if (software == 'htree') {
        $('#rawgraph5')
                .css("display", "none");
        $('#rawgraph10')
                .css("display", "none");
    }
    else {
        $('#rawgraph5')
                .css("display", "inline");
        $('#rawgraph10')
                .css("display", "inline");
    }

    $.ajax({
        url: '/sensitive/sensitivityajax/',
        data: { 'varQtl': vqtl,
            'software': software,
            'snp_config': snpConfig
        },
        success: drawPlots
    });
}


function drawPlots(data){

    var anSvg = $('#rawgraph1');
    // dimensions stuff
    var svgWidth =  anSvg.width() ,
            svgHeight = anSvg.height(),

            MARGINS = {
                left:50,
                right:20,
                bottom:30,
                top:30
            };

    var HEIGHT =  svgHeight - MARGINS.bottom - MARGINS.top
    var WIDTH = svgWidth - MARGINS.left - MARGINS.right

    // go ahead and map the data
    var map = d3.map(data);

    // convert the data to numbers from strings
    map.forEach(function(key,element){

        element.adjpValue = + element.adjpValue;
        element.runNumber = + element.runNumber;

    });
    // set up scales for x , y
    var x = d3.scale.linear()
            .range([0,WIDTH]);

    var y = d3.scale.linear()
            .range([HEIGHT ,0])

    var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(0);
    var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

    var line = d3.svg.line()
            .x(function(d){return x(d.runNumber);})
            .y(function(d){return y(d.adjpValue);});



    function drawRawGraphs(key,element){

        x.domain(d3.extent(element,function(d){return d.runNumber;}));
        y.domain(d3.extent(element,function(d){return d.adjpValue;}));
        var id = '#rawgraph' + key;
        var svg = d3.select(id);
        var axis = svg.select('.axis');
        var software = $("#software").val();
        var snp_config = $("#snpConfig").val();



        if(axis[0][0] == null ) { // have we already drawn the axis objects?

            var main_div = d3.select("#rawScores") ;

            main_div.append("text")
                    .attr("class", "mainTitle")
                    .attr("x", $("#rawScores").width()/2)
                    .attr("y", $("#rawScores").height()/2)
                    .text( "Model " + snp_config + " : " + software);

            svg.append("text")
                    .attr("class", "title")
                    .attr("x", ((WIDTH +MARGINS.right + MARGINS.left)/2))
                    .attr("y", 0 + (MARGINS.top / 2))
                    .attr("text-anchor", "middle")
                    .style("font-size", "16px")
                    .style("text-decoration", "underline")
                    .text( software + " " + key + " Mouse Model");

            var holder = svg.attr("width", WIDTH + MARGINS.left + MARGINS.right)
                    .attr("height", HEIGHT + MARGINS.top + MARGINS.bottom)
                    .append("g")
                    .attr("transform", "translate(" + MARGINS.left + "," + MARGINS.top + ")");

            holder.append("g")
                    .attr("class", "x axis ")
                    .attr("transform", "translate(0," + HEIGHT + ")")
                    .call(xAxis);

            holder.append("g")
                    .attr("class", "y axis")
                    .attr("transform","translate( 0 ,0)" )
                    .call(yAxis);
            holder.append('svg:path')
                    .attr("class","graphline")
                    .attr("d" , line(element));


        }
        else{ // redraw them if they already exist

            svg.select(".title")
                    .text( $("#software").val() + " " + key + " Mouse Model");

            svg.select(".x.axis")
                    .call(xAxis);
            svg.select(".y.axis")
                    .call(yAxis);

            svg.selectAll('path.graphline')
                .attr('d',line(element));

            
        }



    }
    map.forEach(drawRawGraphs);
}


function get_power_curve(event){
    console.log(event);
    if(event.data.curve_type=='locus_specific') {
        var snp_config = $("#power_curve_snp_config").val();
        var url = '/home/locus_ajax/';
    }
    else if (event.data.curve_type=='overall_power'){
        var snp_config = $("#power_curve_snp_config").val();
        var url = '/home/overall_power_ajax/'
    }

    else{
        var snp_config = $("#power_curve_snp_config").val();
        var url = '/home/overall_failure_ajax/'
    }

    $.ajax({
        url: url,
        data: { 'snp_config': snp_config

        },
        success: drawPowerCurves
    });
    return 0 ;

}

function drawPowerCurves(data) {

    // go ahead and map the data
    var map = d3.map(data);


    var anSvg = $('#powergraphplink');
     // dimensions stuff
    var svgWidth =  anSvg.width() ,
            svgHeight = anSvg.height(),

            MARGINS = {
                left:50,
                right:20,
                bottom:30,
                top:30
            };

    var HEIGHT =  svgHeight - MARGINS.bottom - MARGINS.top
    var WIDTH = svgWidth - MARGINS.left - MARGINS.right

    // go ahead and map the data
    var map = d3.map(data);

    // set up scales for x , y
    var x = d3.scale.linear()
            .range([0,WIDTH]);

    var y = d3.scale.linear()
            .range([HEIGHT ,0])

    var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(4);
    var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

    var line = d3.svg.line()
            .x(function(d){return x(d.var_qtl);})
            .y(function(d){return y(d.power);});

    var color = d3.scale.category10();
    var cvalue = function(d) { return d.mouse_per;}
    map.forEach(drawPlotBySoftware);


    function drawPlotBySoftware(software, element) {


        var id = "#powergraph" + software;
        var svg = d3.select(id);
        var axis = svg.select('.axis');
        var snp_config =  $("#power_curve_snp_config").val();
        x.domain([.05,.3]);
        y.domain([0,1.0]);

        if (axis[0][0] == null) { // have we already drawn the axis objects?

            // set up the main plot area.
            var main_div = d3.select("#powerGraphs");

            svg.append("text")
                .attr("class", "title")
                .attr("x", ((WIDTH + MARGINS.right + MARGINS.left) / 2))
                .attr("y", 0 + (MARGINS.top / 2))
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("text-decoration", "underline")
                .text(software );

            var holder = svg.attr("width", WIDTH + MARGINS.left + MARGINS.right)
                .attr("height", HEIGHT + MARGINS.top + MARGINS.bottom)
                .append("g")
                .attr("transform", "translate(" + MARGINS.left + "," + MARGINS.top + ")");



            holder.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + HEIGHT + ")")
                .call(xAxis);

            holder.append("g")
                .attr("class", "y axis")
                .attr("transform", "translate( 0 ,0)")
                .call(yAxis);


            for( var k in element){

                if(software=='htree' && (k=='5' || k=='10')){
                    continue;
                }
                else {
                    var power_data = element[k];

                    holder.append('svg:path')
                        .attr("class", "graphline graphline" + k)
                        .attr("d", line(power_data))
                        .style("stroke", color(cvalue(power_data[0])));

                }
            }


        }
        else{ // we are redrawing the graphs

            for( var k in element){


                if(software=='htree' && (k=='5' || k=='10')){
                    continue;
                }
                else {
                    var power_data = element[k];

                    svg.select(".graphline.graphline" + k)
                        .attr("d", line(power_data))
                        .style("stroke", color(cvalue(power_data[0])));
                }


            }

            svg.selectAll(".y.axis")
                .call(yAxis);
            svg.selectAll(".x.axis")
                .call(xAxis);


        }
    }


}