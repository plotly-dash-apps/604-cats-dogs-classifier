import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# https://stackoverflow.com/questions/67711358/valueerror-attempt-to-convert-a-value-none-with-an-unsupported-type-class/68049002#68049002

########### Define your variables ######

tabtitle = 'cats vs dogs'

# Load the trained model
# file = tarfile.open('model.tar.gz')
# file.extractall('DVC2.h5')
model = load_model('DVC2.h5',compile=True)


######## Define helper functions


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

    html.Button(children='Submit', id='submit-val', n_clicks=0,
                    style={
                    'background-color': 'red',
                    'color': 'white',
                    'margin-left': '5px',
                    'verticalAlign': 'center',
                    'horizontalAlign': 'center'}
                    ),
    html.Div(id='output-div'),

])

@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    )
def update_output_div(clicks):

    if clicks==0:
        return "waiting for inputs"
    else:
        return make_prediction('image/cat.jpg')


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)