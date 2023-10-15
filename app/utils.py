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
        "Cluster": data
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
        csv_data = file.read().decode('utf-8')

        # Versuche, das Trennzeichen automatisch zu erkennen
        try:
            # Versuche, das Trennzeichen automatisch zu erkennen
            dataframe = pd.read_csv(io.StringIO(csv_data, newline = ''), sep=None, decimal = ',', engine='python', thousands=None)
        except pd.errors.ParserError:
            try:
                # Versuch 2: CSV mit Komma als Dezimalzeichen
                dataframe = pd.read_csv(io.StringIO(csv_data, newline = ''), sep=";", engine='python', decimal=',')
            except pd.errors.ParserError:
                # Wenn das automatische Erkennen und beide Versuche fehlschlagen, verwende ';' als Fallback-Trennzeichen
                dataframe = pd.read_csv(io.StringIO(csv_data, newline = ''), sep=",", engine='python', decimal='.')

        return dataframe
    if filename.endswith(".xlsx"):
        # Read the uploaded Excel file
        excel_data = file.read()

        # Verwende pandas, um die Excel-Datei einzulesen
        dataframe = pd.read_excel(io.BytesIO(excel_data), engine='openpyxl')
        return dataframe
    return {"error": "Die hochgeladene Datei ist keine json, xlsx oder csv Datei."}

def check_parameter(centroids, number_runs, dataframe, k_min, k_max, init, algorithm, normalization):
    """
        checking the params for kmeans
    """

    error_message = ""
    if (not isinstance(number_runs, int) or number_runs < 1) and number_runs != 'auto':
        error_message += "The number of kmeans-runs has to be an integer > 0 or ""auto"""
    if k_min > len(dataframe) or k_max > len(dataframe) or k_min < 0 or k_max < 0:
        error_message += ("The k-value has to be an integer > 0"
                          " and smaller than the number of datapoints. ")
    if k_min > k_max:
        error_message += ("k_min has to be smaller than k_max")
    if (init not in ("k-means++","random", "centroids") or
        (init == "centroids" and centroids is None)):
        error_message += ("The parameter init has to be k-means++, random or centroids"
                          " in combination with a specification"
                          " of the initial centroid positions. ")
    if algorithm not in ("elkan","auto", "lloyd", "full"):
        error_message += ("The 'algorithm' parameter of KMeans must be a str among"
                         " ('elkan', 'auto' (deprecated), 'lloyd', 'full' (deprecated)).")
    if normalization is not None and normalization not in("min-max", "z"):
        error_message += ("The 'normalization' parameter must be None or a string among"
                         " ('min-max' or 'z').")

    return error_message

def elbow_to_json(k_min, k_max, elbow):
    """
        function to store elbow data in json string
    """
    # Erstelle ein leeres Dictionary, um die Daten zu speichern
    data = {}

    for k in range(k_min, k_max + 1):
        data[k] = elbow[k - k_min]

    # Konvertiere das Dictionary in einen  JSON-String
    json_string = json.dumps(data, indent=4)

    return json_string
