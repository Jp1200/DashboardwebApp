import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

api_key = open('alpha.txt', 'r').read()
# ts = TimeSeries(key=api_key.format(api_key), output_format='JSON')


# def getStock(stock):
stock = 'MSFT'
rstocks = requests.get(
    'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&outputsize=compact&apikey=api_key')
result = rstocks.json()
result = result['Time Series (1min)']


df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])


for i, p in result.items():
    date = datetime.datetime.strptime(i, '%Y-%m-%d  %H:%M:%S')
    dataForAllTimes_row = [date, float(p['1. open']), float(p['2. high']), float(
        p['3. low']), float(p['4. close']), float(p['5. volume'])]
    df.loc[-1, :] = dataForAllTimes_row
    df.index = df.index+1

    # plt.plot(int(date), dataForAllTimes_row[3])

df = df.sort_values('date')
timeNow = datetime.datetime.now()
newTime = []
print("The current time is {}".format(timeNow))
for time in df['date']:
    correctedTime = timeNow - time
    print('This is the current time: {}'.format(
        timeNow) + " ---- Date from API: {}".format(time))
    newTime.append(correctedTime)


# print(df['open'], df['date'])
fig = px.line(df['open'], title="{} Open pricing over time.".format(stock))

app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': "Microsoft", 'value': 'MSFT'},
            {'label': "Aamazon", 'value': 'AMZN'}
        ],
        value='MSFT'
    ),
    html.Div(id='dd-output-container'),

    dcc.Graph(
        id='graph',
        figure=fig
    )
])


@ app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')]
)
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
