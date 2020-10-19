import numpy as np

from bokeh.layouts import gridplot
from bokeh.models import TapTool,HoverTool
from bokeh.plotting import curdoc, figure

import pandas as pd

df = pd.read_csv('xy.csv',header=None)
x = df[0].values # g-r
y = df[1].values # r

spectra = pd.read_csv('spectra.csv')
lambdas = spectra.columns.values.astype(np.float)

#TOOLS="pan,wheel_zoom,box_select,lasso_select,reset"
#TOOLS="tap,reset"
hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("(G-R,R)", "(@x, @y)"),
])

# create the scatter plot
p = figure(tools=[hover,"tap","reset"], plot_width=800, plot_height=300, min_border=10, min_border_left=50, min_border_right=50,
           toolbar_location="above",y_axis_location="right",x_axis_location="below",
           title=None)
p.background_fill_color = "#fafafa"
p.sizing_mode = 'scale_both'

r = p.scatter(x, y, size=10, color="#3A5785", alpha=0.6) #, xlabel="G-R",ylabel="R")

LINE_ARGS = dict(color="#3A5785", line_color=None)

ph = figure(toolbar_location=None, plot_width=p.plot_width, plot_height=100,
            min_border=10, min_border_left=50, y_axis_location="right")
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4
ph.background_fill_color = "#fafafa"
ph.sizing_mode='scale_both'
#ph.xlabel = "Wavelength (Å)"
#ph.ylabel = "Luminosity"

#ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white", line_color="#3A5785")
#hh1 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
#hh2 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)
spec_plt = ph.line(lambdas,spectra.iloc[0,:].values)

layout = gridplot([[p], [ph]], merge_tools=False)

curdoc().add_root(layout)
curdoc().title = "Hertzsprung-Russell Diagram"

def update(attr, old, new):
    inds = new
    if len(inds) == 0 or len(inds) == len(x):
        return
    elif len(inds) > 1:
        print("More than one point selected, picking last...")

    spec_plt.data_source.data["y"] = spectra.iloc[inds[-1],:].values

r.data_source.selected.on_change('indices', update)
