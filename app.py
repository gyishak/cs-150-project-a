import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


df = pd.read_csv("ad_viz_plotval_data (3).csv")

df["Local Site Name"] = pd.Series(df["Local Site Name"]).str.lower()
df["Date"] = pd.to_datetime(df["Date"])

df=(df.groupby(["Date", "Local Site Name"])[
        ["Daily Mean PM2.5 Concentration", "Daily AQI Value"]
            ].mean())

df = df.reset_index()


#App Layout
stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    [
        html.Div(
            html.H1(
                "PM 2.5 Concentration In Boston, MA", style={"textAlign": "center", "color": "red"}
            ),
            className="row",
        ),
        html.Div(dcc.Graph(id="line-chart", figure={}), className="row"),

        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="my-dropdown",
                        multi=True,
                        options=[
                            {"label": x, "value": x}
                            for x in sorted(df["Local Site Name"].unique())
                        ],
                    style={"color": "black"}

                    ),
                    className="three columns",
                ),

            ],
            className="row",
        ),
    ]
)


# Callbacks ***************************************************************
@app.callback(
    Output(component_id="line-chart", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
)
def update_graph(chosen_value):
    print(f"Values chosen by user: {chosen_value}")
    #chosen_value=list(chosen_value)

    if chosen_value is None:
        return {}
    else:
        chosen_value = list(chosen_value)
        df_filtered = df[df[
            "Local Site Name"].isin(chosen_value)]
        fig = px.line(
            data_frame=df_filtered,

            x="Date",
            y="Daily Mean PM2.5 Concentration",
            color="Local Site Name",
            log_y=True,
            labels={
                "Daily Mean PM2.5 Concentration": "Daily Mean PM2.5 Concentration",
                "Date": "Date",
                "Local Site Name": "Local Site Name",
            },

        )
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)


