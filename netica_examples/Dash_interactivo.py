# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from NeticaPy import Netica


def chestClinic (N, env):
    # Initialize Netica environment
    mesg = bytearray()
    res = N.InitNetica2_bn(env, mesg)
    print("\n" + "-" * 65)
    print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
    print("Chest Clinic Example - programmatically creating the network")
    print("-" * 65 + "\n")

    # Create network canvas
    net = N.NewNet_bn(b"ChestClinic", env)

    # Define nodes
    VisitAsia = N.NewNode_bn(b"VisitAsia", 2, net)
    Tuberculosis = N.NewNode_bn(b"Tuberculosis", 2, net)
    Smoking = N.NewNode_bn(b"Smoking", 2, net)
    Cancer = N.NewNode_bn(b"Cancer", 2, net)
    TbOrCa = N.NewNode_bn(b"TbOrCa", 2, net)
    XRay = N.NewNode_bn(b"XRay", 2, net)
    Dyspnea = N.NewNode_bn(b"Dyspnea", 2, net)
    Bronchitis = N.NewNode_bn(b"Bronchitis", 2, net)

    # Add states to nodes
    N.SetNodeStateNames_bn(VisitAsia, b"visit,no_visit")
    N.SetNodeStateNames_bn(Tuberculosis, b"present,absent")
    N.SetNodeStateNames_bn(Smoking, b"smoker,nonsmoker")
    N.SetNodeStateNames_bn(Cancer, b"present,absent")
    N.SetNodeStateNames_bn(TbOrCa, b"true,false")
    N.SetNodeStateNames_bn(XRay, b"abnormal,normal")
    N.SetNodeStateNames_bn(Dyspnea, b"present,absent")
    N.SetNodeStateNames_bn(Bronchitis, b"present,absent")

    # Add titles to nodes
    N.SetNodeTitle_bn(TbOrCa, b"Tuberculosis or Cancer")
    N.SetNodeTitle_bn(Cancer, b"Lung Cancer")
    N.SetNodeTitle_bn(Dyspnea, b"Dyspnea happening")

    # Define network linkages
    N.AddLink_bn(VisitAsia, Tuberculosis)
    N.AddLink_bn(Smoking, Cancer)
    N.AddLink_bn(Smoking, Bronchitis)
    N.AddLink_bn(TbOrCa, Dyspnea)
    N.AddLink_bn(Bronchitis, Dyspnea)
    N.AddLink_bn(Tuberculosis, TbOrCa)
    N.AddLink_bn(Cancer, TbOrCa)
    N.AddLink_bn(TbOrCa, XRay)

    # Feed values to CPTs
    N.SetNodeProbs(VisitAsia, 0.01, 0.99)

    N.SetNodeProbs(Tuberculosis, b"visit", 0.05, 0.95)
    N.SetNodeProbs(Tuberculosis, b"no_visit", 0.01, 0.99)

    N.SetNodeProbs(Smoking, 0.5, 0.5)

    N.SetNodeProbs(Cancer, b"smoker", 0.1, 0.9)
    N.SetNodeProbs(Cancer, b"nonsmoker", 0.01, 0.99)

    #    Tuberculosis & Cancer "deterministic node"
    N.SetNodeProbs(TbOrCa, b"present", b"present", 1.0, 0.0)
    N.SetNodeProbs(TbOrCa, b"present", b"absent", 1.0, 0.0)
    N.SetNodeProbs(TbOrCa, b"absent", b"present", 1.0, 0.0)
    N.SetNodeProbs(TbOrCa, b"absent", b"absent", 0.0, 1.0)

    N.SetNodeProbs(Dyspnea, b"true", b"present", 0.9, 0.1)
    N.SetNodeProbs(Dyspnea, b"true", b"absent", 0.7, 0.3)
    N.SetNodeProbs(Dyspnea, b"false", b"present", 0.8, 0.2)
    N.SetNodeProbs(Dyspnea, b"false", b"absent", 0.1, 0.9)

    N.SetNodeProbs(Bronchitis, b"smoker", 0.6, 0.4)
    N.SetNodeProbs(Bronchitis, b"nonsmoker", 0.3, 0.7)

    #                  TbOrCa  Abnormal Normal
    N.SetNodeProbs(XRay, b"true", 0.98, 0.02)
    N.SetNodeProbs(XRay, b"false", 0.05, 0.95)

    N.CompileNet_bn(net)

    return net

def p_chest_diags(N, net, precond):
    auto_update_on = N.SetNetAutoUpdate_bn(netica_chestClinic, 0)
    N.RetractNetFindings_bn(net)
    if "si-fuma" in precond:
        N.EnterFinding(b"Smoking", b"smoker", net)
    elif "no-fuma" in precond:
        N.EnterFinding(b"Smoking", b"nonsmoker", net)
    if "si-asia" in precond:
        N.EnterFinding(b"VisitAsia", b"visit", net)
    elif "no-asia" in precond:
        N.EnterFinding(b"VisitAsia", b"no_visit", net)
    if "si-disnea" in precond:
        N.EnterFinding(b"Dyspnea", b"present", net)
    elif "no-disnea" in "precond":
        N.EnterFinding(b"Dyspnea", b"absent", net)
    if "si-rayosX" in precond:
        N.EnterFinding(b"XRay", b"abnormal", net)
    elif "no-rayosX" in precond:
        N.EnterFinding(b"XRay", b"normal", net)
    N.SetNetAutoUpdate_bn(netica_chestClinic, auto_update_on)

    padecimiento = ["Tuberculosis o Cancer", "Bronquitis", "Tuberculosis", "Cancer"]
    p_de_padecimiento = [N.GetNodeBelief(b"TbOrCa", b"true", net) * 100]
    p_de_padecimiento.append(N.GetNodeBelief(b"Bronchitis", b"present", net) * 100)
    p_de_padecimiento.append(N.GetNodeBelief(b"Tuberculosis", b"present", net) * 100)
    p_de_padecimiento.append(N.GetNodeBelief(b"Cancer", b"present", net) * 100)
    df = pd.DataFrame({"padecimiento": padecimiento,
                       "prob": p_de_padecimiento}, index=padecimiento)
    return df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''
### _Clínica del Torax_ 

Tomamos como base el clásico ejemplo de la __Clínica del Torax__ 
para construir este tablero con [Plotly Dash](https://dash.plotly.com/). Permite interactuar libremente
con la multicitada red  ejemplo [ChestClinic](https://norsys.com/tutorials/netica/secA/tut_A3.htm).

#### Nodos de la red

Puedes elegir los distintos signos y datos diagnósticos 
que apliquen al caso y las probabilidades correspondientes 
para tuberculosis, bronquitis y cancer se mostrará en la gráfica en breve.
'''

app.layout = html.Div([
    html.Div([dcc.Markdown(children=markdown_text)]),
    html.Div([
        html.Label('Proporciona la evidencia que tengas'),
        html.Label('¿Es fumador?'),
        dcc.RadioItems(
            id="fumador-input",
            options=[
                {'label': 'No lo se', 'value': 'ND-fuma'},
                {'label': 'Sí', 'value': 'si-fuma'},
                {'label': 'No', 'value': 'no-fuma'}],
            value='nd',
            labelStyle={
                'display': 'inline-block',
                'margin-right': '7px',
                'font-weight': 300},
            style={
                'display': 'inline-block',
                'margin-left': '7px'}),
        html.Label('¿Viajo a Asia?'),
        dcc.RadioItems(
            id="asia-input",
            options=[
                {'label': 'No lo se', 'value': 'ND-asia'},
                {'label': 'Sí', 'value': 'si-asia'},
                {'label': 'No', 'value': 'no-asia'}],
            value='nd',
            labelStyle={
                'display': 'inline-block',
                'margin-right': '7px',
                'font-weight': 300},
            style={
                'display': 'inline-block',
                'margin-left': '7px'}),
        html.Label('¿Padece de disnea?'),
        dcc.RadioItems(
            id="disnea-input",
            options=[
                {'label': 'No lo se', 'value': 'ND-disnea'},
                {'label': 'Sí', 'value': 'si-disnea'},
                {'label': 'No', 'value': 'no-disnea'}],
            value='nd',
            labelStyle={
                'display': 'inline-block',
                'margin-right': '7px',
                'font-weight': 300},
            style={
                'display': 'inline-block',
                'margin-left': '7px'}),
        html.Label('¿Los rayos X son Normales?'),
        dcc.RadioItems(
            id="rayosX-input",
            options=[
                {'label': 'No lo se', 'value': 'ND-rayosX'},
                {'label': 'Sí', 'value': 'si-rayosX'},
                {'label': 'No', 'value': 'no-rayosX'}],
            value='nd',
            labelStyle={
                'display': 'inline-block',
                'margin-right': '7px',
                'font-weight': 300},
            style={
                'display': 'inline-block',
                'margin-left': '7px'}),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br()
    ], style={'width': '20%', 'display': 'inline-block'}),

        html.Div(dcc.Graph(id='graph-bar'), style={'width': '78%', 'display': 'inline-block'})
 ])

@app.callback(
    Output(component_id='graph-bar', component_property='figure'),
    Input(component_id='fumador-input', component_property='value'),
    Input(component_id='asia-input', component_property='value'),
    Input(component_id='disnea-input', component_property='value'),
    Input(component_id='rayosX-input', component_property='value'))

def update_output_div(fuma, asia, disnea, rayosX):
    precond_lst = [fuma, asia, disnea, rayosX]
    p_df = p_chest_diags(N, netica_chestClinic, precond_lst)
    fig = px.bar(p_df, y="padecimiento", x="prob", color="padecimiento", orientation='h',
                 title="Probabilidad de tener el padecimiento", height=300, width=700)
    fig.update_xaxes(range=[0, 100])
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=0))

    return fig

if __name__ == '__main__':
    # Create an instance of Netica package
    N = Netica()

    # Initialize Netica and report on status
    mesg = bytearray()
    env = N.NewNeticaEnviron_ns(b"", None, b"") # if licence available provide here at "0"
    netica_chestClinic = chestClinic(N, env)

    app.run_server(debug=True)

# If you want to save your network do this
#    N.WriteNet_bn(netica_chestClinic, N.NewFileStream_ns(b"mi_chestClinic.neta", env))

    # N.DeleteNet_bn(net)
    # res = N.CloseNetica_bn(env, mesg)
    #
    # print("\n" + "-" * 65)
    # print(mesg.decode("utf-8"))
    # print("-" * 65 + "\n")
