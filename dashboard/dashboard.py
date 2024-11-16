import os
import pandas as pd
import dash
from dash import dcc,html

from dash.dependencies import Input,Output

import plotly.express as px

from datetime import datetime


class SalesDashboard:
    def __init__(self,output_dir="/Users/ilyasdahhou/Desktop/ecom-front/ecom/spark_processing/notebooks/output"):
        self.output_dir=output_dir
        self.app=dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def load_data(self, start_date, end_date):
        """
        Charge les données des fichiers entre start_date et end_date
        """
        all_data = []