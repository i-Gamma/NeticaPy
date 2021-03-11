# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from NeticaPy import Netica


def chestClinic (N):
    mesg = bytearray()
    env = N.NewNeticaEnviron_ns(b"", None, b"")
    # env = N.NewNeticaEnviron_ns ("",None,"");
    res = N.InitNetica2_bn(env, mesg)

    print("\n" + "-" * 65)
    print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
    print("Chest Clinic Example - programmatically creating the network")
    print("-" * 65 + "\n")

    net = N.NewNet_bn(b"ChestClinic", env)

    VisitAsia = N.NewNode_bn(b"VisitAsia", 2, net);
    Tuberculosis = N.NewNode_bn(b"Tuberculosis", 2, net);
    Smoking = N.NewNode_bn(b"Smoking", 2, net);
    Cancer = N.NewNode_bn(b"Cancer", 2, net);
    TbOrCa = N.NewNode_bn(b"TbOrCa", 2, net);
    XRay = N.NewNode_bn(b"XRay", 2, net);

    N.SetNodeStateNames_bn(VisitAsia, b"visit,   no_visit");
    N.SetNodeStateNames_bn(Tuberculosis, b"present, absent");
    N.SetNodeStateNames_bn(Smoking, b"smoker,  nonsmoker");
    N.SetNodeStateNames_bn(Cancer, b"present, absent");
    N.SetNodeStateNames_bn(TbOrCa, b"true,    false");
    N.SetNodeStateNames_bn(XRay, B"abnormal,normal");
    N.SetNodeTitle_bn(TbOrCa, b"Tuberculosis or Cancer");
    N.SetNodeTitle_bn(Cancer, b"Lung Cancer");

    N.AddLink_bn(VisitAsia, Tuberculosis);
    N.AddLink_bn(Smoking, Cancer);
    N.AddLink_bn(Tuberculosis, TbOrCa);
    N.AddLink_bn(Cancer, TbOrCa);
    N.AddLink_bn(TbOrCa, XRay);

    N.SetNodeProbs(VisitAsia, 0.01, 0.99);

    N.SetNodeProbs(Tuberculosis, b"visit", 0.05, 0.95);
    N.SetNodeProbs(Tuberculosis, b"no_visit", 0.01, 0.99);

    N.SetNodeProbs(Smoking, 0.5, 0.5);

    N.SetNodeProbs(Cancer, b"smoker", 0.1, 0.9);
    N.SetNodeProbs(Cancer, b"nonsmoker", 0.01, 0.99);

    #                   Tuberculosis Cancer
    N.SetNodeProbs(TbOrCa, b"present", b"present", 1.0, 0.0);
    N.SetNodeProbs(TbOrCa, b"present", b"absent", 1.0, 0.0);
    N.SetNodeProbs(TbOrCa, b"absent", b"present", 1.0, 0.0);
    N.SetNodeProbs(TbOrCa, b"absent", b"absent", 0.0, 1.0);

    #                  TbOrCa  Abnormal Normal

    N.SetNodeProbs(XRay, b"true", 0.98, 0.02);
    N.SetNodeProbs(XRay, b"false", 0.05, 0.95);

    N.CompileNet_bn(net)

    prob = []
    belief = N.GetNodeBelief(b"Tuberculosis", b"present", net)
    prob.append(belief)
    print("The probability of tuberculosis is {:#.4f}".format(belief))

    N.EnterFinding(b"XRay", b"abnormal", net);
    belief = N.GetNodeBelief(b"Tuberculosis", b"present", net);
    prob.append(belief)
    print("Given an abnormal X-ray, the probability of tuberculosis is {:#.4f}".format(belief))

    N.EnterFinding(b"VisitAsia", b"visit", net)
    belief = N.GetNodeBelief(b"Tuberculosis", b"present", net)
    prob.append(belief)
    print("Given an abnormal X-ray and a visit to Asia, the probability of tuberculosis is {:#.4f}".format(belief))

    N.EnterFinding(b"Cancer", b"present", net)
    belief = N.GetNodeBelief(b"Tuberculosis", b"present", net)
    prob.append(belief)
    print(
        "Given abnormal X-ray, Asia visit, and lung cancer, the probability of tuberculosis is {:#.4f}".format(belief))
    return prob


N = Netica()
net_chestclinic = chestClinic(N)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.DataFrame({
    "evidencia de Tuberculosis": ["nada", "rayos X anormales", "rayos X anormales", "rayos X anormales y cancer"],
    "Probabilidad de tener Tuberculosis": netica_results,
    "Visita a Asia": ["no indicado", "no indicado", "Visita a Asia", "Visita a Asia"]})

fig = px.bar(df, x="evidencia de Tuberculosis", y="Probabilidad de tener Tuberculosis",
             color="Visita a Asia")  # , barmode="group" si se quiere juntar barras

app.layout = html.Div(children=[
    html.H1(children='Hola Dash - Ejemplo de RED Bayesiana: Chest Clinic'),

    html.Div(children='''
             Dash: Es un marco para aplicaciones web (aquí se usa Python).
             '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

    N.DeleteNet_bn(net)
    res = N.CloseNetica_bn(env, mesg)

    print("\n" + "-" * 65)
    print(mesg.decode("utf-8"))
    print("-" * 65 + "\n")

