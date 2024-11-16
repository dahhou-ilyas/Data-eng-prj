import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime

class SalesDashboard:
    def __init__(self, output_dir="/Users/ilyasdahhou/Desktop/ecom-front/ecom/spark_processing/notebooks/output"):
        self.output_dir = output_dir
        self.app = dash.Dash(__name__)
        self.setup_layoutt()
        self.setup_callbacks()
        
    def load_data(self, start_date, end_date):
        """
        Charge les données des fichiers entre start_date et end_date
        """
        try:
            all_data = []
            # Convertir les dates string en datetime
            start = datetime.strptime(start_date.split('T')[0], '%Y-%m-%d')
            end = datetime.strptime(end_date.split('T')[0], '%Y-%m-%d')
            
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.txt'):
                    file_date = datetime.strptime(filename[:8], '%Y%m%d')
                    
                    if start.date() <= file_date.date() <= end.date():
                        filepath = os.path.join(self.output_dir, filename)
                        try:
                            # Lire le fichier en gérant les erreurs potentielles
                            df_temp = pd.read_csv(filepath, sep='|', 
                                                names=['datetime', 'product', 'sales'],
                                                encoding='utf-8')
                            # Convertir les ventes en numérique
                            df_temp['sales'] = pd.to_numeric(df_temp['sales'], errors='coerce')
                            all_data.append(df_temp)
                        except Exception as e:
                            print(f"Erreur lors de la lecture du fichier {filename}: {e}")
                            continue
            
            if all_data:
                df = pd.concat(all_data, ignore_index=True)
                # Convertir la colonne datetime en datetime
                df['date'] = pd.to_datetime(df['datetime']).dt.date
                df['hour'] = pd.to_datetime(df['datetime']).dt.hour
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            return pd.DataFrame()

    def setup_layoutt(self):
        """
        Configure la mise en page du dashboard
        """
        self.app.layout = html.Div([
            html.H1('Dashboard E-commerce - Analyse des Ventes',
                   style={'textAlign': 'center', 'marginBottom': 30}),
            
            # Sélecteurs de date
            html.Div([
                html.Label('Sélectionner la période:'),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=datetime(2024, 1, 1),
                    max_date_allowed=datetime(2024, 12, 31),
                    initial_visible_month=datetime(2024, 11, 16),
                    start_date=datetime(2024, 11, 16),
                    end_date=datetime(2024, 11, 16)
                )
            ], style={'marginBottom': 20}),
            
            # Cartes des statistiques
            html.Div([
                html.Div([
                    html.H3('Ventes Totales', style={'textAlign': 'center'}),
                    html.H4(id='total-sales', style={'textAlign': 'center'})
                ], className='stat-card'),
                html.Div([
                    html.H3('Nombre de Produits', style={'textAlign': 'center'}),
                    html.H4(id='product-count', style={'textAlign': 'center'})
                ], className='stat-card'),
                html.Div([
                    html.H3('Produit le Plus Vendu', style={'textAlign': 'center'}),
                    html.H4(id='top-product', style={'textAlign': 'center'})
                ], className='stat-card')
            ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': 30}),
            
            # Graphiques
            html.Div([
                dcc.Graph(id='top-products-chart', style={'width': '50%'}),
                dcc.Graph(id='sales-evolution-chart', style={'width': '50%'})
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            html.Div([
                dcc.Graph(id='hourly-sales-chart', style={'width': '50%'}),
                dcc.Graph(id='product-share-chart', style={'width': '50%'})
            ], style={'display': 'flex'}),
        ])

    def setup_callbacks(self):
        """
        Configure les callbacks pour mettre à jour les graphiques
        """
        @self.app.callback(
            [Output('total-sales', 'children'),
             Output('product-count', 'children'),
             Output('top-product', 'children'),
             Output('top-products-chart', 'figure'),
             Output('sales-evolution-chart', 'figure'),
             Output('hourly-sales-chart', 'figure'),
             Output('product-share-chart', 'figure')],
            [Input('date-picker', 'start_date'),
             Input('date-picker', 'end_date')]
        )
        def update_dashboard(start_date, end_date):
            try:
                if not start_date or not end_date:
                    return "0 €", "0", "Aucun", {}, {}, {}, {}
                
                # Charger les données
                df = self.load_data(start_date, end_date)
                if df.empty:
                    return "0 €", "0", "Aucun", {}, {}, {}, {}
                
                # Calculer les statistiques
                total_sales = f"{df['sales'].sum():,.2f} €"
                product_count = str(df['product'].nunique())
                top_product = df.groupby('product')['sales'].sum().idxmax()
                
                # 1. Top produits
                top_products = df.groupby('product')['sales'].sum().nlargest(5)
                fig1 = px.bar(
                    x=top_products.values,
                    y=top_products.index,
                    orientation='h',
                    title="Top 5 des Produits par Ventes",
                    labels={'x': 'Ventes totales', 'y': 'Produit'}
                )
                
                # 2. Évolution des ventes
                daily_sales = df.groupby('date')['sales'].sum().reset_index()
                fig2 = px.line(
                    daily_sales,
                    x='date',
                    y='sales',
                    title="Évolution des Ventes Quotidiennes",
                    labels={'date': 'Date', 'sales': 'Ventes totales'}
                )
                
                # 3. Ventes par heure
                hourly_sales = df.groupby('hour')['sales'].sum().reset_index()
                fig3 = px.bar(
                    hourly_sales,
                    x='hour',
                    y='sales',
                    title="Distribution des Ventes par Heure",
                    labels={'hour': 'Heure', 'sales': 'Ventes totales'}
                )
                
                # 4. Parts de marché
                product_shares = df.groupby('product')['sales'].sum()
                fig4 = px.pie(
                    names=product_shares.index,
                    values=product_shares.values,
                    title="Parts de Marché des Produits"
                )
                
                return total_sales, product_count, top_product, fig1, fig2, fig3, fig4
                
            except Exception as e:
                print(f"Erreur dans le callback: {e}")
                return "Erreur", "Erreur", "Erreur", {}, {}, {}, {}

    def run_server(self, debug=True, port=8050):
        """
        Lance le serveur Dash
        """
        self.app.run_server(debug=debug, port=port)

# Pour lancer le dashboard
if __name__ == '__main__':
    dashboard = SalesDashboard()
    dashboard.run_server()