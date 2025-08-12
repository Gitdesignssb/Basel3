import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import io

app = dash.Dash(__name__)
server = app.server  # for deployment

app.layout = html.Div([
    html.H2("Basel III CET1 Ratio Calculator"),
    
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV'),
        multiple=False
    ),
    
    html.Div(id='output-message'),
    html.Div(id='output-table'),
    html.Div(id='output-results')
])

@app.callback(
    [Output('output-message', 'children'),
     Output('output-table', 'children'),
     Output('output-results', 'children')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def process_file(contents, filename):
    if contents is None:
        return "Please upload a CSV file.", None, None

    try:
        content_type, content_string = contents.split(',')
        decoded = io.StringIO(io.BytesIO(base64.b64decode(content_string)).read().decode('utf-8'))
        df = pd.read_csv(decoded)

        required_columns = ["Exposure Amount (USD)", "Current RW (%)", "Basel III RW (%)"]
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            return f"Missing columns: {', '.join(missing)}", None, None

        df["Current RWA"] = df["Exposure Amount (USD)"] * df["Current RW (%)"] / 100
        df["Basel III RWA"] = df["Exposure Amount (USD)"] * df["Basel III RW (%)"] / 100

        total_current_rwa = df["Current RWA"].sum()
        total_basel_rwa = df["Basel III RWA"].sum()
        cet1_capital = 12000000
        cet1_current_ratio = cet1_capital / total_current_rwa
        cet1_basel_ratio = cet1_capital / total_basel_rwa

        results = html.Div([
            html.P(f"Current CET1 Ratio: {cet1_current_ratio:.2%}"),
            html.P(f"Basel III CET1 Ratio: {cet1_basel_ratio:.2%}"),
            html.P(f"Capital Impact: {(cet1_basel_ratio - cet1_current_ratio):.2%}")
        ])

        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10
        )

        return f"File '{filename}' processed successfully.", table, results

    except Exception as e:
        return f"Error processing file: {str(e)}", None, None

if __name__ == '__main__':
    app.run_server(debug=True)
