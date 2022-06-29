import datetime
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2

########### Define your variables ######

myheading1='Try out a palindrome here!'
tabtitle = 'cats vs dogs'
sourceurl = 'https://www.grammarly.com/blog/16-surprisingly-funny-palindromes/'
githublink = 'https://github.com/plotly-dash-apps/202-palindrome-callbacks'

# Load the trained model
model = load_model('DVC2.h5',compile=True)


######## Define helper functions

def make_prediction(img_b64):
    img = image.load_img(img_b64, target_size=(64, 64))
    img = np.reshape(img,[1,64,64,3])
    img = tf.cast(img, tf.float32)
    img=img/255
    y_pred = round(model.predict(img),4)
    classes = (y_pred>0.5).astype("int32")
    if classes[0][0] == 1:
        return f'DOG probability: {y_pred}'
    else:
        return f'CAT probability: {y_pred}'


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


########### Set up the layout

app.layout = html.Div([
    html.H1('This is the header'),
    html.Img(id='top-image'),
    html.Div(id='base64-string'),
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


@app.callback(Output('base64-string', 'children'),
              Input('intermediate-value', 'data')
              )
def update_output(contents):
    # print(contents)
    if contents is not None:
        print('contents type: ',type(contents))
        return str(contents)
    else:
        return 'waiting for inputs'




@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State('intermediate-value', 'data')
)
def update_output_div(clicks, input_value):

    if clicks==0:
        return "waiting for inputs"
    else:
        if input_value is not None:
            return make_prediction(input_value)
        else:
            return "waiting for image"


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
