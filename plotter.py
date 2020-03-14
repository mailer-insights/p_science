import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def line_plot(x, y, legend, title, x_label, y_label):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x = x,
        y=y,
        name=legend

    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )


    return fig

def pie_plot(labels, values, title):
    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels = labels,
            values = values,
    ))

    fig.update_layout(
        title = title,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )

    return fig
