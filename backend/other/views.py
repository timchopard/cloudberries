from django.shortcuts import render
import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

def other_index(request):
    context = {
    }
    return render(request, "other/index.html", context)

def internship(request):

    weeks = np.linspace(8, 15, 8, dtype=int)
    base_salary = 24000
    locations = {
        "Seattle": 0,
        "Minneapolis": 2000,
        "Miami": 4000,
        "Omaha": 6000
    }
    divisions = {
        "Div. C": 0,
        "Div. R": 2000,
        "Div. S": 5000,
    }
    index = {}


    for loc in locations:
        for divi in divisions:
            combination = f"{loc}, {divi}"
            bonus = locations[loc] + divisions[divi]
            index[combination] = bonus 

    index_reduced = {}
    for key in index:
        if index[key] in index_reduced: 
            index_reduced[index[key]] += f" AND {key}"
        else:
            index_reduced[index[key]] = key 
    index = {}
    for key in index_reduced:
        index[index_reduced[key]] = key

    data = pd.DataFrame(columns=weeks, index=index.keys())
    data["Division/Location"] = data.index 
    df = data.melt(id_vars="Division/Location", value_vars=weeks)
    df = df.rename(columns={df.columns[1]: "Weeks"})
    df["value"] = df.apply(
        lambda x: int(
            x["Weeks"] * ((index[x["Division/Location"]] + base_salary) / 15)
        ), 
        axis=1
    )
    print(df)

    fig = px.line(df, x="Weeks", y="value", color="Division/Location",
                  title="Cost of Hiring")
    fig.update_traces(mode="markers+lines")
    finished_plot = plot(fig, output_type="div")
    context = {'plot_div': finished_plot}
    print(data)
    return render(request, "other/internship.html", context)

def gas(request):
    context = {

    }
    return render(request, "other/gas.html", context)