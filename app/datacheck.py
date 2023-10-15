# -*- coding: utf-8 -*-
"""
Module checking incoming dataframes
"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

def data_check(redis_client, dataframe,tasks, task_id):
    """
    Checks a dataframe and clears it for clustering

    Args:
        dataframe (pd.DataFrame): The uploaded CSV data.
        cleaned_df (pd.DataFrame): The cleaned CSV data.
        
    Returns:
        cleaned_df (pd.DataFrame): The cleaned CSV data.
    """

    try:
        tasks[task_id]["status"] = "Data Preparation"
        redis_client.hset(task_id,'status',"Data Preparation")
        # Löscht alle Zeilen mit null-Werten
        cleaned_df = dataframe.dropna()
        tasks[task_id]["message"] += "Removed rows with null values. "
        redis_client.hset(task_id,'message',tasks[task_id]["message"])

        # Löscht alle Zeilen mit nicht alphanumerischen Werten
        #for column in cleaned_df.columns:
         #   #cleaned_df = cleaned_df[cleaned_df[column].apply(lambda x: str(x).isalnum())]
         #   cleaned_df = cleaned_df[cleaned_df[column].apply(lambda x: isinstance(x, (int, float)) or str(x).isalnum())]
         #   tasks[task_id]["message"] += "Removed rows with non-alphanumeric values. "
         #   redis_client.hset(task_id,'message',tasks[task_id]["message"])

        #löscht alle Zeilen, die Buchstaben UND Zanhlen enthalten
        # Iteriert über die Spalten und erstellt eine Liste der zu löschenden Spalten
        columns_to_drop = [col for col in cleaned_df.columns if contains_numbers_and_letters(cleaned_df[col])]
        # Löscht die ausgewählten Spalten
        cleaned_df = cleaned_df.drop(columns=columns_to_drop)
        
        if columns_to_drop:
            tasks[task_id]["message"] += "Removed columns with inconsistent data(letters and numbers). "
            redis_client.hset(task_id,'message',tasks[task_id]["message"])

        cleaned_df = cleaned_df.reset_index(drop=True)
        return cleaned_df
    except Exception as exception:
        # Wenn ein Fehler auftritt, wird die Nachricht an `tasks[task_id]` angehangen.
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] += str("data_check: " + str(exception))
        redis_client.hset(task_id,'status',"Bad Request")
        redis_client.hset(task_id,'message',tasks[task_id]["message"])
        return None

def ohe(redis_client, cleaned_df,tasks, task_id):
    """
    Filtern der kategorischen Spalten und Durchführung von OHE
    """
    # Filter columns by data type (categorical)
    try:
        categorical_columns = cleaned_df.select_dtypes(include=['object']).columns.tolist()

        # One-Hot-Encoding for categorical columns
        encoder = OneHotEncoder(sparse_output=False, drop='first')
        encoded_columns = encoder.fit_transform(cleaned_df[categorical_columns])
        encoded_feature_names = encoder.get_feature_names_out(input_features=categorical_columns)
        encoded_df = pd.DataFrame(encoded_columns, columns=encoded_feature_names)

        # Drop original categorical columns
        cleaned_df = cleaned_df.drop(columns=categorical_columns)

        # Concatenate encoded DataFrame with the original DataFrame
        ohe_df = pd.concat([cleaned_df, encoded_df], axis=1)

        tasks[task_id]["message"] += "One-Hot encoded. "
        redis_client.hset(task_id,'message',tasks[task_id]["message"])
        ohe_df = df.reset_index(drop=True)
        return ohe_df
    except Exception as exception:
        # Wenn ein Fehler auftritt, wird die Nachricht an `tasks[task_id]` angehangen.
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] += str("OHE: " + str(exception))
        redis_client.hset(task_id,'status',"Bad Request")
        redis_client.hset(task_id,'message',tasks[task_id]["message"])
        return None

def run_normalization(redis_client, dataframe,tasks, task_id, normalization):
    """
    Normalisierung der Daten
    """
    try:
        if normalization == 'z':
            # Skalierung der numerischen Spalten (Standardisierung - Z-Transformation)
            numerical_columns = dataframe.select_dtypes(include=['int', 'float']).columns
            scaler = StandardScaler()
            dataframe[numerical_columns] = scaler.fit_transform(dataframe[numerical_columns])

        if normalization == 'min-max':
            # Skalierung der numerischen Spalten (Min-Max-Skalierung)
            numerical_columns = dataframe.select_dtypes(include=['int', 'float']).columns
            scaler = MinMaxScaler()  # Min-Max-Skalierung anstelle von Standardisierung
            dataframe[numerical_columns] = scaler.fit_transform(dataframe[numerical_columns])
            tasks[task_id]["message"] += "Min-Max scaled). "
            tasks[task_id]["status"] = "Data prepared. Processing"
            redis_client.hset(task_id,'status',"Data prepared. Processing")
            redis_client.hset(task_id,'message',tasks[task_id]["message"])

        return dataframe
    except Exception as exception:
        # Wenn ein Fehler auftritt, wird die Nachricht an `tasks[task_id]` angehangen.
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] += str("Normalization: " + str(exception))
        redis_client.hset(task_id,'status',"Bad Request")
        redis_client.hset(task_id,'message',tasks[task_id]["message"])
        return None


def contains_numbers_and_letters(column):
    """
    Checks if a column contains numbers and letters 
    """
    return any(str(c).isalpha() for c in column) and any(str(c).isdigit() for c in column)
