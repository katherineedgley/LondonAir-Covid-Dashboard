from myapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.wrangle_data import return_figure

@app.route('/')
@app.route('/index')
def index():

    figures = [return_figure('NO2')]
    ids = ['figure-0']
    # plot ids for the html id tag
    #ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
@app.route('/O3')
def O3():
    figures = [return_figure('O3')]
    ids = ['figure-1']

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('O3.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/PM10')
def PM10():
    figures = [return_figure('PM10')]
    ids = ['figure-2']

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('PM10.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/PM25')
def PM25():
    figures = [return_figure('PM25')]
    ids = ['figure-2']

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('PM25.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

