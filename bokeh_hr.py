import numpy as np

from bokeh.layouts import gridplot
from bokeh.models import TapTool,HoverTool,CustomJS,ColumnDataSource
from bokeh.plotting import curdoc, figure

import pandas as pd

df = pd.read_csv('xy.csv',header=None)
x = df[0].values # g-r
y = df[1].values # r

spectra = pd.read_csv('spectra.csv')
lambdas = spectra.columns.values.astype(np.float)

# create the scatter plot
p = figure(tools=["tap","reset"], plot_width=800, plot_height=300, min_border=10, min_border_left=50, min_border_right=50,
           toolbar_location="above",y_axis_location="left",x_axis_location="below",y_axis_type="log",
           title=None)
p.background_fill_color = "#fafafa"
p.sizing_mode = 'scale_both'
p.xaxis.axis_label="G-R"
p.yaxis.axis_label="R"

r = p.scatter(x, y, size=10, color="#3A5785", alpha=0.6) #, xlabel="G-R",ylabel="R")

LINE_ARGS = dict(color="#3A5785", line_color=None)

shover = HoverTool(tooltips = [
    ("(λ,L)", "($x, $y)"),
])
ph = figure(toolbar_location=None, plot_width=p.plot_width, plot_height=100,
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
hover = HoverTool(tooltips=None,callback=callback,renderers=[r])
p.add_tools(hover)

layout = gridplot([[p], [ph]], merge_tools=False)

curdoc().add_root(layout)
curdoc().title = "Hertzsprung-Russell Diagram"
