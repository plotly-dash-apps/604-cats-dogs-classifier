import datetime
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State


########### Define your variables ######

myheading1='Try out a palindrome here!'
tabtitle = 'racecar'
sourceurl = 'https://www.grammarly.com/blog/16-surprisingly-funny-palindromes/'
githublink = 'https://github.com/plotly-dash-apps/202-palindrome-callbacks'


######## Define helper functions

def parse_contents_a(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


def parse_contents(contents):
    return html.Img(src=contents)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


########### Set up the layout

app.layout = html.Div([
    html.H1('This is the header'),
    html.Img(id='top-image'),
    html.Div(id='try-this'),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # DO NOT allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-image-upload'),
    html.Button(children='Submit', id='submit-val', n_clicks=0,
                    style={
                    'background-color': 'red',
                    'color': 'white',
                    'margin-left': '5px',
                    'verticalAlign': 'center',
                    'horizontalAlign': 'center'}
                    ),
    html.Div(id='output-div'),
    dcc.Store(id='intermediate-value')
])


@app.callback(Output('output-image-upload', 'children'),
              # Output('top-image', 'src'),
              Output('intermediate-value', 'data'),
              Input('upload-image', 'contents'),
              )
def update_output(contents):
    # print(contents)
    if contents is not None:
        # store_data = contents.to_json(date_format='iso', orient='split')
        return html.Img(src=contents),  contents
    else:
        return None, None


@app.callback(Output('try-this', 'children'),
              Input('intermediate-value', 'data')
              )
def update_output(contents):
    # print(contents)
    if contents is not None:
        return str(contents)
    else:
        return 'waiting for inputs'




@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='output-image-upload', component_property='children')
)
def update_output_div(clicks, input_value):

    if clicks==0:
        return "waiting for inputs"
    if clicks==1:
        return f"You've pressed the button {clicks} time"
    else:
        return f"You've pressed the button {clicks} times"

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
