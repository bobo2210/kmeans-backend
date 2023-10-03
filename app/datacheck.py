# -*- coding: utf-8 -*-
"""
Module checking incoming dataframes
"""

async def data_check(dataframe):
    """
    Checks a dataframe and clears it for clustering

    Args:
        dataframe (pd.DataFrame): The uploaded CSV data.
        cleaned_df (pd.DataFrame): The cleaned CSV data.
        
    Returns:
        cleaned_df (pd.DataFrame): The cleaned CSV data.
    """
    # Löscht alle Zeilen mit null-Werten
    cleaned_df = dataframe.dropna()

    # Löscht alle Zeilen mit nicht alphanumerischen Werten
    for column in cleaned_df.columns:
        cleaned_df = cleaned_df[cleaned_df[column].apply(lambda x: str(x).isalnum())]
    
    #löscht alle Zeilen, die Buchstaben UND Zanhlen enthalten
    for column in cleaned_df.columns:
        if contains_numbers_and_letters(cleaned_df[column]).any():
            cleaned_df.drop(column, axis=1, inplace=True)
    return cleaned_df
    
async def contains_numbers_and_letters(column):
    """
    Checks if a column contains numbers and letters 
        
    Returns:
        true if a column contains numbers and letters
        else returns false
    """
    return column.str.contains(r'[0-9]') & column.str.contains(r'[a-zA-Z]')
