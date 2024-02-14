import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import os
import pdf
import LLms
import formatString
import sendMail

# Create Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, title="LLM-Resume",
                external_stylesheets=[dbc.themes.PULSE])


def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    path = os.path.join("./pdf/", name)
    with open(path, "wb") as fp:
        fp.write(base64.decodebytes(data))


# Define layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.P(["LLM-Resume Classification Tool"],
                                   style={'font-family': 'cursive', 'text-decoration': 'underline',
                                          'text-align': 'center', 'color': '2px solid black', 'fontSize': 10}),
                            dbc.CardImg(src="/assets/resume.jpeg", top=True)]
                        ),
                        style={"width": "10rem", "margin": "0 auto", "border": "2px solid green"}
                    ))], justify="center"),

            dbc.Label("Name"),
            dbc.Input(id='name', placeholder="enter name...", type="text"),
            dbc.FormText("Please enter name"),
            html.Hr(),

            dbc.Label("Phone Number"),
            dbc.Input(id='phone', placeholder="enter phone number...", type="number"),
            dbc.FormText("Please type phone number"),
            html.Hr(),

            dbc.Label("Email"),
            dbc.Input(id='email', placeholder="enter email...", type="text"),
            dbc.FormText("Please enter name"),
            html.Hr(),

            dbc.Label("Resume Uploads"),
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select a PDF File')
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
                    multiple=True
                ),
                html.Div(id='output-data-upload'),
            ]),
            dbc.FormText("Please Upload File"),
            # html.Hr(),

            html.Div(id='output', style={'text-align': 'center', 'color': ' 2px solid black', 'fontSize': 14}),
            html.Hr(),

            dbc.Row(id='summary'),
            html.Br(),

            html.Div([html.P(id="test2")], id='output-data1',
                     style={'marginBottom': 20, 'marginTop': 10, 'color': 'purple', 'fontSize': 14}),
            html.Br(),

            html.Div([html.P(id="test1")], id='output-data',
                     style={'marginBottom': 15, 'marginTop': 5, 'color': 'green', 'fontSize': 14}),
            html.Br(),

            html.Div([html.Button('Submit & Register Resume', id='submit', n_clicks=0)])

        ], width=6, className="m-5", md=6, sm=12, lg=6,
            style={'marginBottom': 15, 'marginTop': 5, 'color': 'green', 'fontSize': 14}),

    ], style={'marginBottom': 15, 'marginTop': 5, 'color': 'green', 'fontSize': 14}, justify="center"),

], id="container", fluid=True)


@app.callback(
    Output('output-data-upload', 'children'),
    Output('test1', 'children'),
    Output('test2', 'children'),
    Output('summary', 'children'),
    Input('name', 'value'),
    Input("phone", "value"),
    Input('email', 'value'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    Input('submit', 'n_clicks'),

)
def update_output(name, phone, email, contents, filename, n_clicks, ):
    if n_clicks:
        if contents is not None:
            for (c, n) in zip(contents, filename):
                if n.endswith('.pdf'):

                    n = "resume.pdf"

                    save_file(n, c)

                    resumeTxt = pdf.readPdf("./pdf/resume.pdf")

                    rating = LLms.flant5xxl(resumeTxt)

                    rat = [rating[0]["generated_text"]]

                    finalScore = formatString.flanUL2(rating)

                    finalScore = int(finalScore[0]["generated_text"])

                    summary = LLms.facebookBL(resumeTxt)

                    if finalScore >= 12:
                        subject = "Application Successful"
                        body = "We are reviewing your application! 🤗"
                        sendMail.sendMail(email, subject, body)
                        return html.Div(['File(s) successfully saved.']), subject, html.Div(rat), dbc.FormText(summary,
                                                                                                               style={
                                                                                                                   'margin-left': 10,
                                                                                                                   'marginBottom': 20,
                                                                                                                   'marginTop': 20,
                                                                                                                   'color': 'green',
                                                                                                                   'fontSize': 14,
                                                                                                                   'border': '2px solid #2a048a',
                                                                                                                   'border-radius': '4px'})
                    else:
                        subject = "Application Not-Successful"
                        body = "Thank you for Applying with us, we are not proceeding with you!🤔"
                        sendMail.sendMail(email, subject, body)
                        return html.Div(['File(s) successfully saved.']), subject, html.Div(rat), dbc.FormText(summary,
                                                                                                               style={
                                                                                                                   'margin-left': 10,
                                                                                                                   'marginBottom': 20,
                                                                                                                   'marginTop': 10,
                                                                                                                   'color': 'green',
                                                                                                                   'fontSize': 14,
                                                                                                                   'border': '2px solid #2a048a',
                                                                                                                   'border-radius': '4px'})
                else:
                    return "", "", "", "",
        else:
            return "", "", "", "",
    else:
        return "", "", "", "",


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
