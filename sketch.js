var spoints = [];
var datable = [];
var xytable = [];
var sketch = function (p) {
    // Global variables
    var plot, logScale;
    var smallplot;
	p.preload = function() {
			// Load the data here.
            xytable = p.loadTable("xy.csv")
			datable = p.loadTable("test_spectrum.csv");
		};

    // Initial setup
    p.setup = function () {
        // Create the canvas
        maxCanvasWidth = document.documentElement.clientWidth - 20;
        maxCanvasHeight = document.documentElement.clientHeight - 20;

        // small plot
        smallHeight = 300; 
        padding = 100;

        // canvas
		canvasWidth = maxCanvasWidth;
		canvasHeight = maxCanvasHeight ;

        // bg color
        bgcolor = p.color(0,22,35);

        // line color
        linecolor = p.color(255,255,255);

        //font info
        fontsize = 18;
        fontcolor = p.color(255,255,255); 

		if (canvasWidth > maxCanvasWidth) {
			canvasHeight = canvasHeight * maxCanvasWidth / canvasWidth;
			canvasWidth = maxCanvasWidth;
		}

		// Create the canvas
		var canvas = p.createCanvas(canvasWidth, canvasHeight);

        // Prepare the points for the plot
        var points = [];

        for (var i = 0; i < xytable.getRowCount(); i++) {
            x = xytable.getNum(i,0);
            y = xytable.getNum(i,1);
            points[i] = new GPoint(x, y);
        }

        var spoints = [];
        var lambdas = [];
        for (var i = 0; i < datable.getColumnCount(); i++) {
            lambdas[i] = datable.getNum(0,i);
        }
        console.log(lambdas);
        for (var i = 0; i < datable.getRowCount()-1; i++) {
            spoints[i] = [];
            for (var j = 0; j < datable.getColumnCount(); j++) {
                spoints[i][j] = new GPoint(lambdas[j],datable.getNum(i+1,j));
            }
        }
        console.log(spoints);

        // Create the plot
        plot = new GPlot(p);
        plot.setPos(0, 0);
        plot.setDim(canvasWidth - padding, canvasHeight - padding - smallHeight);
        plot.setBoxBgColor(bgcolor)
        plot.setBgColor(bgcolor)
        plot.setBoxLineColor(linecolor)
        //plot.setBoxLineWidth(2);

        smallplot = new GPlot(p);
        smallplot.setPos(0,canvasHeight - smallHeight);
        smallplot.setDim(canvasWidth - padding, smallHeight - padding);
        smallplot.setBgColor(bgcolor);
        smallplot.setBoxBgColor(bgcolor);
        smallplot.setBoxLineColor(linecolor)
        smallplot.setBoxLineWidth(2);

        // Set the plot title and the axis labels
        plot.setTitleText("Hertzsprung\-Russell diagram");
        plot.getTitle().setFontSize(fontsize+5);
        plot.getTitle().setFontColor(linecolor);
        plot.getXAxis().setAxisLabelText("Temperature");
        plot.getXAxis().setFontSize(fontsize);
        plot.getXAxis().setFontColor(fontcolor);

        smallplot.getXAxis().setAxisLabelText("Wavelength (angstrom)");
        smallplot.getXAxis().setFontSize(fontsize);
        smallplot.getXAxis().setFontColor(fontcolor);

        if (logScale) {
            plot.setLogScale("y");
            plot.getYAxis().setAxisLabelText("Magnitude");
            plot.getYAxis().setFontSize(fontsize);
            plot.getYAxis().setFontColor(linecolor);
        } else {
            plot.setLogScale("");
            plot.getYAxis().setAxisLabelText("Luminosity");
            plot.getYAxis().setFontSize(fontsize);
            plot.getYAxis().setFontColor(linecolor);
        }
        if (logScale) {
            smallplot.setLogScale("y");
            smallplot.getYAxis().setAxisLabelText("Magnitude");
            smallplot.getYAxis().setFontSize(fontisze);
            smallplot.getYAxis().setFontColor(linecolor);
        } else {
            smallplot.setLogScale("");
            smallplot.getYAxis().setAxisLabelText("Luminosity");
            smallplot.getYAxis().setFontSize(fontsize);
            smallplot.getYAxis().setFontColor(linecolor);
        }

        // Add the points to the plot
        plot.setPoints(points);
        plot.setPointColor(p.color(100, 100, 255, 50));

        smallplot.setPoints(spoints[0]);
        smallplot.setPointColor(p.color(100, 100, 255, 50));
    };

    // Execute the sketch
    p.draw = function () {
        // Clean the canvas
        p.background(0);

        // Draw the plot
        plot.beginDraw();
        plot.drawBackground();
        plot.drawBox();
        plot.drawXAxis();
        plot.drawYAxis();
        plot.drawTopAxis();
        plot.drawRightAxis();
        plot.drawTitle();
        plot.drawPoints();
        plot.endDraw();
        smallplot.beginDraw();
        smallplot.drawBackground();
        smallplot.drawBox();
        smallplot.drawXAxis();
        smallplot.drawYAxis();
        smallplot.drawTopAxis();
        smallplot.drawRightAxis();
        smallplot.drawTitle();
        smallplot.drawPoints();
        smallplot.endDraw();
    };

    p.mouseClicked = function () {
        if (plot.isOverBox(p.mouseX, p.mouseY)) {
            // Change the log scale
            logScale = !logScale;

            if (logScale) {
                plot.setLogScale("y");
                plot.getYAxis().setAxisLabelText("log y");
                smallplot.setLogScale("y");
                smallplot.getYAxis().setAxisLabelText("log y");
            } else {
                plot.setLogScale("");
                plot.getYAxis().setAxisLabelText("y");
                smallplot.setLogScale("");
                smallplot.getYAxis().setAxisLabelText("y");
            }
        }
    };
};

var myp5 = new p5(sketch);
