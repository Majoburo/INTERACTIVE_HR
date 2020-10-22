from bokeh.layouts import gridplot
from bokeh.models import TapTool,HoverTool,CustomJS,ColumnDataSource
from bokeh.plotting import curdoc, figure
from bokeh.io import output_file,show
from bokeh.util.hex import hexbin
from bokeh.transform import log_cmap
from bokeh.palettes import Greys256
import pandas as pd
import numpy as np
output_file("/home/robbie/code/INTERACTIVE_HR/output.html")

df = pd.read_csv('xy.csv',header=None,skiprows=1)
X = df[1].values # Abs mag
Y = df[0].values # color

spectra = pd.read_csv('spectra.csv',skiprows=1)
#lambdas = spectra.iloc[0,:] #spectra.columns.values.astype(np.float)
lambdas = spectra.columns.values.astype(np.float)
# background
# Load in Full Gaia Dataset
full_gaia = pd.read_csv("HRD_light_gaia_query.csv")
bprp = full_gaia.phot_bp_mean_mag.values - full_gaia.phot_rp_mean_mag.values
mag = full_gaia.phot_g_mean_mag.values + 5.0*np.log10(full_gaia.parallax/100.)
source_gaia = ColumnDataSource(data=dict(x=bprp, y=mag))
# Define the X and Y limits for the plot
xlow = -0.6
xupp = 4.5
ylow = 17.0
yupp = -1.5
xdiff = xupp-xlow
ydiff = ylow-yupp
aspect = ydiff/xdiff

# Initialize Light Curve Plot
fig_cmd = figure(plot_height=280, plot_width=800, sizing_mode='scale_both',
                 x_range=[xlow,xupp], y_range=[ylow,yupp],
                 tools="pan,wheel_zoom,box_zoom,reset",
                 title=None,
                 min_border=10, min_border_left=50, min_border_right=50,
                 toolbar_location="above", border_fill_color="whitesmoke")
fig_cmd.toolbar.logo = None
fig_cmd.yaxis.axis_label = 'Color (BP-RP)'
fig_cmd.xaxis.axis_label = 'Absolute Magnitude (G)'
# Generate Hexbin CMD for full Gaia Sample
bins = hexbin(bprp, mag, 0.05, aspect_scale=aspect)
palette = Greys256[::-1]
fill_color = log_cmap('c', palette, 1, max(bins.counts))
source = ColumnDataSource(data=dict(q=bins.q, r=bins.r, c=bins.counts))
r = fig_cmd.hex_tile(q="q", r="r", size=0.05, aspect_scale=aspect,
                     source=source, line_color=None, fill_color=fill_color)
# Remove Grid Lines
fig_cmd.xgrid.grid_line_color = None
fig_cmd.ygrid.grid_line_color = None

# Add a simple hover tool
fig_cmd.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]))

scat = fig_cmd.scatter(X, Y, size=10, color="#3A5785", alpha=0.8) #, xlabel="G-R",ylabel="R")

# Main HRD
#p = figure(tools=["tap","reset"], plot_width=800, plot_height=300, min_border=10, min_border_left=50, min_border_right=50,
#           toolbar_location="above",y_axis_location="left",x_axis_location="below",y_axis_type="log",
#           title=None)
#p.background_fill_color = "#fafafa"
#p.sizing_mode = 'scale_both'
#p.xaxis.axis_label="G-R"
#p.yaxis.axis_label="R"
#
#r = p.scatter(x, y, size=10, color="#3A5785", alpha=0.6) #, xlabel="G-R",ylabel="R")

# Inset spectrum plot, height 1/4 of total
shover = HoverTool(tooltips = [
    ("(λ,L)", "($x, $y)"),
])
ph = figure(toolbar_location=None, plot_width=fig_cmd.plot_width, plot_height=100,
            min_border=10, min_border_left=50, y_axis_location="left",tools=[shover])
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4
ph.background_fill_color = "#fafafa"
ph.sizing_mode='scale_both'
ph.xaxis.axis_label = "Wavelength (Å)"
ph.yaxis.axis_label = "Luminosity"

spectrum = ColumnDataSource(dict(x=lambdas,y=spectra.iloc[0,:].values))
spec_plt = ph.line("x","y",source=spectrum)

hoveractive = True
code = '''
const ind = cb_data.index.indices.slice(-1)[0];
if (hoveractive && ind != undefined) {
    source.data.y = spectra[ind];
    source.change.emit();
}
'''
callback = CustomJS(args={
    'hoveractive': hoveractive,
    'spectra' :spectra.values,
    'source' :spec_plt.data_source,
    },code=code)
hover = HoverTool(tooltips=None,callback=callback,renderers=[scat])
fig_cmd.add_tools(hover)

layout = gridplot([[fig_cmd], [ph]], merge_tools=False,sizing_mode='scale_both')
#layout = gridplot([[fig_cmd]], merge_tools=False,sizing_mode='scale_height')

curdoc().add_root(layout)
curdoc().title = "Hertzsprung-Russell Diagram"

show(layout)
