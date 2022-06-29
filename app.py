import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import base64
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tarfile


########### Define your variables ######

tabtitle = 'cats vs dogs'
sourceurl = 'https://www.kaggle.com/c/dogs-vs-cats'
githublink = 'https://github.com/plotly-dash-apps/604-cats-dogs-classifier'

# Load the trained model
# file = tarfile.open('model.tar.gz')
# file.extractall('DVC2.h5')
model = load_model('DVC2.h5',compile=True)


######## Define helper functions


def b64_jpg_converter(base64_string):
    if 'base64,' in base64_string:
        img_str=base64_string.split('base64,')[1]
        imgdata = base64.b64decode(img_str)
        filename = 'temp.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

def make_prediction(img_file):
    img = image.load_img(img_file, target_size=(64, 64))
    img = tf.reshape(img,[1,64,64,3])
    img = tf.cast(img, tf.float32)
    img=img/255
    y_pred = model.predict(img)
    prediction = (y_pred>0.5).astype("int")
    classes=['DOG', 'CAT']
    dog_prob=round(y_pred[0][0].astype("float"),4)
    cat_prob=round(1-y_pred[0][0].astype("float"),4)
    # return f"It's a {classes[prediction]}! DOG probability: {dog_prob}, CAT probability: {cat_prob}"
    return f"DOG probability: {dog_prob}, CAT probability: {cat_prob}"


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


########### Set up the layout

app.layout = html.Div([
    html.H1('Cats vs Dogs!'),

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
    html.Button(children='Submit', id='submit-val', n_clicks=0,
                    style={
                    'background-color': 'red',
                    'color': 'white',
                    'margin-left': '5px',
                    'verticalAlign': 'center',
                    'horizontalAlign': 'center'}
                    ),
    html.Div(id='output-div'),
    html.Div(id='output-image-upload'),
    html.Div(id='base64-string'),
    dcc.Store(id='intermediate-value'),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


@app.callback(Output('output-image-upload', 'children'),
              Output('intermediate-value', 'data'),
              Input('upload-image', 'contents'))
def update_output(contents):
    if contents is not None:
        b64_jpg_converter(contents)
        return html.Img(src=contents, style={'height':'20%','width':'20%'}),  contents
    else:
        return None, None


@app.callback(Output('base64-string', 'children'),
              Input('intermediate-value', 'data'))
def update_output(contents):
    if contents is not None:
        return str(contents)
    else:
        return 'waiting for inputs'



@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State('intermediate-value', 'data'))
def update_output_div(clicks, input_value):

    if clicks==0:
        return "waiting for inputs"
    else:
        if input_value is not None:
            return make_prediction('temp.jpg')
        else:
            return "waiting for image"






############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
