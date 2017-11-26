var sketch = function (p) {
    // Global variables
    var plot, logScale;
	p.preload = function() {
			// Load the data here.
			//table = p.loadTable("data/lifeExpectancyDataset.csv", "header");
		};

    // Initial setup
    p.setup = function () {
        // Create the canvas
        maxCanvasWidth = document.documentElement.clientWidth - 20;
        maxCanvasHeight = document.documentElement.clientHeight - 20;

        // small plot
        smallHeight = 300; 
        padding = 100;
		canvasWidth = maxCanvasWidth;
		canvasHeight = maxCanvasHeight ;

        // bg color
        bgcolor = p.color(0,22,35);

        // line color
        linecolor = p.color(255,255,255);

        fontsize = 18;

		if (canvasWidth > maxCanvasWidth) {
			canvasHeight = canvasHeight * maxCanvasWidth / canvasWidth;
			canvasWidth = maxCanvasWidth;
		}

		// Create the canvas
		var canvas = p.createCanvas(canvasWidth, canvasHeight);

        // Prepare the points for the plot
        var points = [];

        for (var i = 0; i < 1000; i++) {
            var x = 10 + p.random(200);
            var y = 10 * p.exp(0.015 * x);
            var xErr = p.randomGaussian(0, 2);
            var yErr = p.randomGaussian(0, 2);
            points[i] = new GPoint(x + xErr, y + yErr);
        }

        // Create the plot
        plot = new GPlot(p);
        plot.setPos(0, 0);
        plot.setDim(canvasWidth - padding, canvasHeight - padding - smallHeight);
        plot.setBoxBgColor(bgcolor)
        plot.setBgColor(bgcolor)
        plot.setBoxLineColor(linecolor)
        plot.setBoxLineWidth(5);

        smallplot = new GPlot(p);
        smallplot.setPos(0,canvasHeight - smallHeight);
        smallplot.setDim(canvasWidth - padding, smallHeight - padding);
        smallplot.setBgColor(bgcolor);
        smallplot.setBoxBgColor(bgcolor);
        smallplot.setBoxLineColor(linecolor)
        smallplot.setBoxLineWidth(5);

        // Set the plot title and the axis labels
        plot.setTitleText("Hertzsprung\-Russell diagram");
        plot.getTitle().setFontSize(fontsize);
        plot.getTitle().setFontColor(linecolor);
        plot.getXAxis().setAxisLabelText("x");
        plot.getXAxis().setFontSize(fontsize);
        plot.getXAxis().setFontColor(linecolor);

        smallplot.getXAxis().setAxisLabelText("Wavelength (angstrom)");
        smallplot.getXAxis().setFontSize(fontsize);
        smallplot.getXAxis().setFontColor(linecolor);

        if (logScale) {
            plot.setLogScale("y");
            plot.getYAxis().setAxisLabelText("log y");
            plot.getYAxis().setFontSize(fontsize);
            plot.getYAxis().setFontColor(linecolor);
        } else {
            plot.setLogScale("");
            plot.getYAxis().setAxisLabelText("y");
            plot.getYAxis().setFontSize(fontsize);
            plot.getYAxis().setFontColor(linecolor);
        }
        if (logScale) {
            smallplot.setLogScale("y");
            smallplot.getYAxis().setAxisLabelText("log y");
            smallplot.getYAxis().setFontSize(fontisze);
            smallplot.getYAxis().setFontColor(linecolor);
        } else {
            smallplot.setLogScale("");
            smallplot.getYAxis().setAxisLabelText("y");
            smallplot.getYAxis().setFontSize(fontsize);
            smallplot.getYAxis().setFontColor(linecolor);
        }

        // Add the points to the plot
        plot.setPoints(points);
        plot.setPointColor(p.color(100, 100, 255, 50));
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
