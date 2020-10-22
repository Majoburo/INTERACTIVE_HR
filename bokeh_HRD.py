import numpy as np
import pandas as pd
from astropy.io import ascii
from astropy.time import Time
from astropy.table import Table

from bokeh.layouts import row, column, grid, layout, widgetbox
from bokeh.models import ColumnDataSource, CustomJS, HoverTool
from bokeh.models import Range1d, Whisker, Legend, LinearAxis
from bokeh.plotting import Figure, output_file, show
from bokeh.util.hex import hexbin
from bokeh.transform import log_cmap
from bokeh.palettes import Greys256

# Configure the output file
fname = "my_bokeh_plot.html"
output_file(fname)

# Load in Full Gaia Dataset
full_gaia = pd.read_csv("HRD_light_gaia_query.csv")
bprp = full_gaia.phot_bp_mean_mag.values - full_gaia.phot_rp_mean_mag.values
mag = full_gaia.phot_g_mean_mag.values + 5.0*np.log10(full_gaia.parallax/100.)

# Load in the Gaia-SDSS Crossmatched Sample
sdss_crossmatch = pd.read_csv("gaia_sdss30_match10.csv")
sdss_bprp = sdss_crossmatch.phot_bp_mean_mag.values - sdss_crossmatch.phot_rp_mean_mag.values
sdss_mag = sdss_crossmatch.phot_g_mean_mag.values + 5.0*np.log10(sdss_crossmatch.parallax/100.)


# Create CDS objects for Gaia and Crossmatched Samples
source_gaia = ColumnDataSource(data=dict(x=bprp, y=mag))
source_sdss = ColumnDataSource(data=dict(x=sdss_bprp, y=sdss_mag))

# Define the X and Y limits for the plot
xlow = -0.6
xupp = 4.5
ylow = 17.0
yupp = -1.5
xdiff = xupp-xlow
ydiff = ylow-yupp
aspect = ydiff/xdiff

# Initialize Light Curve Plot
fig_cmd = Figure(plot_height=300, plot_width=300, sizing_mode='scale_height',
                 x_range=[xlow,xupp], y_range=[ylow,yupp],
                 tools="pan,wheel_zoom,box_zoom,reset",
                 toolbar_location="above", border_fill_color="whitesmoke")
fig_cmd.toolbar.logo = None
fig_cmd.yaxis.axis_label = 'Color (BP-RP)'
fig_cmd.xaxis.axis_label = 'Absolute Magnitude (G)'


# Choose color, alpha, and size for data points
c = "cornflowerblue"
a = 1.0
s = 4

# Generate Hexbin CMD for full Gaia Sample
bins = hexbin(bprp, mag, 0.05, aspect_scale=aspect)
palette = Greys256[::-1]
fill_color = log_cmap('c', palette, 1, max(bins.counts))
source = ColumnDataSource(data=dict(q=bins.q, r=bins.r, c=bins.counts))
r = fig_cmd.hex_tile(q="q", r="r", size=0.05, aspect_scale=aspect,
                     source=source, line_color=None, fill_color=fill_color)

# Add a simple hover tool
fig_cmd.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]))

# Plot ZTF g and r light curve data
f_ztfg = fig_cmd.circle('x', 'y', source=source_sdss, size=s, 
               # Set defaults
               fill_color=c, line_color=c,
               fill_alpha=a, line_alpha=a,
               # set visual properties for selected glyphs
               selection_color=c,
               selection_alpha=a,
               # set visual properties for non-selected glyphs
               nonselection_color=c,
               nonselection_alpha=a,
               legend_label = 'SDSS Sample')

# Remoe Grid Lines
fig_cmd.xgrid.grid_line_color = None
fig_cmd.ygrid.grid_line_color = None

# Create plot grid
l = grid([fig_cmd],sizing_mode='scale_height')

# Use "show" to generate HTML file and launch plot in the browser
show(l)

# Bokeh generates an annoying HTML header (<!DOCTYPE html>") 
# which displays as raw text when embedded in the website.  
# The following code removes this line of text from the html file
with open(fname, "r") as f:
    lines = f.readlines()
with open(fname, "w") as f:
    for line in lines:
        if line.strip("\n") != "<!DOCTYPE html>":
            f.write(line)





