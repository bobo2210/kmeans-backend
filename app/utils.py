# -*- coding: utf-8 -*-
"""
Module containing different methods
"""

import json
import io
import pandas as pd

def dataframe_to_json_str(dataframe, cluster_labels, centroids):
    """
    merges dataframe to a json str  
        
    Returns:
        json str for frontend
    """
    data = []

    unique_clusters = set(cluster_labels)

    for cluster in unique_clusters:
        cluster_data = {
            "centroids": centroids[cluster].tolist(),
            "data_points": dataframe[cluster_labels == cluster].values.tolist()
        }
        data.append(cluster_data)

    result = {
        "data_Points": data
    }

    return json.dumps(result, indent=2)


def read_file(file, filename):
    """
        function to read data out of file in a dataframe
    """
    if filename.endswith(".json"):

        #json Datei öffnen
        with file as json_file:
            data = json.load(json_file)

        # Zugriff auf die Datenpunkte
        data_points = data.get("data_points", [])

        # Erstellen eines  Pandas DataFrame
        dataframe = pd.DataFrame(data_points)
        return dataframe
    if filename.endswith(".csv"):
        # Read the uploaded CSV file
        csv_data = file.read()
        # Create a DataFrame from the CSV data
           # Versuche, das Trennzeichen automatisch zu erkennen
        try:
            dataframe = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), sep=None)
        except pd.errors.ParserError:
            # Wenn das automatische Erkennen fehlschlägt, verwende ';' als Fallback-Trennzeichen
            dataframe = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), sep=";")
        return dataframe
    if filename.endswith(".xlsx"):
        # Read the uploaded Excel file
        excel_data = file.read()

        # Verwende pandas, um die Excel-Datei einzulesen
        dataframe = pd.read_excel(io.BytesIO(excel_data), engine='openpyxl')
        return dataframe
    return {"error": "Die hochgeladene Datei ist keine json, xlsx oder csv Datei."}