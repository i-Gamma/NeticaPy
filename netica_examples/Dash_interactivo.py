# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from NeticaPy import Netica


def chestClinic (N):
    mesg = bytearray()
    env = N.NewNeticaEnviron_ns(b"", None, b"")
    # env = N.NewNeticaEnviron_ns ("",None,"")
    res = N.InitNetica2_bn(env, mesg)

    print("\n" + "-" * 65)
    print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
    print("Chest Clinic Example - programmatically creating the network")
    print("-" * 65 + "\n")

    net = N.NewNet_bn(b"ChestClinic", env)

    VisitAsia = N.NewNode_bn(b"VisitAsia", 2, net)
    Tuberculosis = N.NewNode_bn(b"Tuberculosis", 2, net)
    Smoking = N.NewNode_bn(b"Smoking", 2, net)
    Cancer = N.NewNode_bn(b"Cancer", 2, net)
    TbOrCa = N.NewNode_bn(b"TbOrCa", 2, net)
    XRay = N.NewNode_bn(b"XRay", 2, net)

    N.SetNodeStateNames_bn(VisitAsia, b"visit,no_visit")
    N.SetNodeStateNames_bn(Tuberculosis, b"present,absent")
    N.SetNodeStateNames_bn(Smoking, b"smoker,nonsmoker")
    N.SetNodeStateNames_bn(Cancer, b"present,absent")
    N.SetNodeStateNames_bn(TbOrCa, b"true,false")
    N.SetNodeStateNames_bn(XRay, B"abnormal,normal")
    N.SetNodeTitle_bn(TbOrCa, b"Tuberculosis or Cancer")
    N.SetNodeTitle_bn(Cancer, b"Lung Cancer")

    N.AddLink_bn(VisitAsia, Tuberculosis)
    N.AddLink_bn(Smoking, Cancer)
    N.AddLink_bn(Tuberculosis, TbOrCa)
    N.AddLink_bn(Cancer, TbOrCa)
    N.AddLink_bn(TbOrCa, XRay)

    N.SetNodeProbs(VisitAsia, 0.01, 0.99)

    N.SetNodeProbs(Tuberculosis, b"visit", 0.05, 0.95)
    N.SetNodeProbs(Tuberculosis, b"no_visit", 0.01, 0.99)

    N.SetNodeProbs(Smoking, 0.5, 0.5)

    N.SetNodeProbs(Cancer, b"smoker", 0.1, 0.9)
    N.SetNodeProbs(Cancer, b"nonsmoker", 0.01, 0.99)

    #                   Tuberculosis Cancer
    N.SetNodeProbs(TbOrCa, b"present", b"present", 1.0, 0.0)
    N.SetNodeProbs(TbOrCa, b"present", b"absent", 1.0, 0.0)
    N.SetNodeProbs(TbOrCa, b"absent", b"present", 1.0, 0.0)
    N.SetNodeProbs(TbOrCa, b"absent", b"absent", 0.0, 1.0)

    #                  TbOrCa  Abnormal Normal

    N.SetNodeProbs(XRay, b"true", 0.98, 0.02)
    N.SetNodeProbs(XRay, b"false", 0.05, 0.95)

    N.CompileNet_bn(net)

    return net

def chestProbabilidades(N, net, precond):
    auto_update_on = N.SetNetAutoUpdate_bn(netica_chestClinic, 0)
    N.RetractNetFindings_bn(net)
    if "fuma" in precond:
        N.EnterFinding(b"Smoking", b"smoker", net)
    else:
        N.EnterFinding(b"Smoking", b"nonsmoker", net)
    if "asia" in precond:
        N.EnterFinding(b"VisitAsia", b"visit", net)
    else:
        N.EnterFinding(b"Cancer", b"present", net)

    N.SetNetAutoUpdate_bn(netica_chestClinic, auto_update_on)
    belief = N.GetNodeBelief(b"Tuberculosis", b"present", net)
    print("----", precond)
    print("-----", belief)
    return belief

N = Netica()
netica_chestClinic = chestClinic(N)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''
### _Clínica del Torax_ 

Tomamos como base el clásico ejemplo de la __Clínica del Torax__ 
para construir este tablero con [Plotly Dash](https://dash.plotly.com/). Permite interactuar libremente
con la multicitada red  ejemplo [ChestClini](https://norsys.com/tutorials/netica/secA/tut_A3.htm).

#### Nodos de la red

Puedes elegir las distintas cosas que te interese 
y la probabilidad de interés se mostrará en breve.

'''

app.layout = html.Div([
    html.Div([dcc.Markdown(children=markdown_text)]),
    html.Br(),

    html.Div([html.Label('Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'Rayos X anormales', 'value': 'rayos_X'},
                {'label': 'Viajó en algún momento a Asia', 'value': 'asia'},
                {'label': 'Tiene Cancer', 'value': 'cancer'}
            ],
            value='rayos_x'
        ),
        html.Br(),

        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'Es fumador', 'value': 'fuma'},
                {'label': 'Viajó a Asia', 'value': 'asia'},
                {'label': 'Tiene cancer', 'value': 'cancer'}
            ],
            value=['fuma', 'asia'],
            multi=True
        ),

        html.Br(),

        html.Label('Ingresar texto'),
        dcc.Input(value='Es fumador', type='text'),

        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(
            id="radio-input",
            options=[
                {'label': 'Es fumador', 'value': 'fuma'},
                {'label': 'Viajó a Asia', 'value': 'asia'},
                {'label': 'Tiene cancer', 'value': 'cancer'}],
            value='fuma'),

        html.Br(),
        html.Label('Checkboxes'),
        dcc.Checklist(
            options=[
                {'label': 'Es fumador', 'value': 'fuma'},
                {'label': 'Viajó a Asia', 'value': 'asia'},
                {'label': 'Tiene cancer', 'value': 'cancer'}
            ],
            value=['fuma', 'asia', 'cancer']
            ),
        html.Br(),

        html.Label('Slider'),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
            value=5,
            ),
        html.H6(dcc.Markdown("""Cambia el valor en la caja de texto para ver 
                                la interactividad (_callbacks_) en acción!""")),
        html.Div(["Input: ",dcc.Input(id='my-input', value='1', type='text', debounce=True)]),
        html.Br(),
        html.Div(id='my-output'),
    ], style={'columnCount': 3})
])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value'),
    Input(component_id='radio-input', component_property='value'),
)
def update_output_div(input_value, precondiciones):
    valor = int(input_value)
#    print(valor)
    probabilidad = chestProbabilidades(N, netica_chestClinic, precondiciones) * 100
    if valor == 10:
        valor = valor * 5

    print(precondiciones)
    print("The probability of tuberculosis is {:#.4f}".format(probabilidad))

    return 'Output: {}, Precondición: {}: Tuberculosis con probabilidad: {:0.2f}%'.format(valor, precondiciones, probabilidad)



if __name__ == '__main__':
    app.run_server(debug=True)

   # N.DeleteNet_bn(net)
   # res = N.CloseNetica_bn(env, mesg)

   # print("\n" + "-" * 65)
   # print(mesg.decode("utf-8"))
   # print("-" * 65 + "\n")
