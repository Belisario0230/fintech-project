from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base de datos
engine = create_engine('postgresql://user:pass@postgres:5432/fintech')
df = pd.read_sql('SELECT * FROM stocks', engine)

# Debug: Verificar columnas
print("Columnas en la base de datos:", df.columns.tolist())

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Financiero"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': t, 'value': t} for t in df['ticker'].unique()],  # ← minúsculas
        value='AAPL'
    ),
    dcc.Graph(id='price-chart')
])

@app.callback(
    Output('price-chart', 'figure'),
    Input('ticker-dropdown', 'value')
)
def update_chart(selected_ticker):
    filtered = df[df['ticker'] == selected_ticker]  # ← minúsculas
    fig = px.line(filtered, 
                 x='Date',       # ← Así aparece en tu tabla
                 y='Price',      # ← Así aparece en tu tabla
                 title=f'Precio de {selected_ticker}')
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)