from bokeh.io impoort show, output_figure
from bokeh.plotting import figure
import bokeh.resources





def create_bapper_stats_plot(bappers, bap_counts):
    """
    """
    plot = figure(xrange=bappers, )
    plot.vbar(x=bappers, top=bap_counts)
    plot_html = bokeh.embed.file_html(plot, bokeh.resources.CDN, title='bapper stats')
    return plot_html
