import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State


########### Define your variables ######

myheading1='Try out a palindrome here!'
initial_value='A nut for a jar of tuna'
longtext='''
        _Suggestions you might try:_
        * A man, a plan, a canal: Panama!
        * Go hang a salami I'm a lasagna hog
        * God! Nate bit a Tibetan dog!
        '''
tabtitle = 'racecar'
sourceurl = 'https://www.grammarly.com/blog/16-surprisingly-funny-palindromes/'
githublink = 'https://github.com/plotly-dash-apps/202-palindrome-callbacks'

########### Define a function for your callback:
def my_function(letters):
    return(letters[::-1])

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1(myheading1),
    html.Div(children=[dcc.Markdown(longtext)]),
    dcc.Input(id='input-div', value=initial_value, type='text',
            style={'width':'50%'}),
    html.Button(children='Taco Cat!', id='submit-val', n_clicks=0,
                    style={
                    'background-color': 'red',
                    'color': 'white',
                    'margin-left': '5px',
                    'verticalAlign': 'center',
                    'horizontalAlign': 'center'}
                    ),
    html.Div(id='output-div'),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


########## Define Callback
@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='input-div', component_property='value')
)
def update_output_div(clicks, input_value):
    palindrome=my_function(input_value)
    if clicks==0:
        return "Was it a car or a cat I saw?"
    else:
        return f"You've entered '{input_value}', and your output is '{palindrome}'"

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
