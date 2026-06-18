# modules/loader.py

import pandas as pd


def load_file(uploaded_file):
    """
    Accepts a Streamlit UploadedFile object.
    Returns a tuple: (DataFrame or None, error_message or None)
    """
    try:
        # Get the file name to check the extension
        file_name = uploaded_file.name

        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        else:
            return None, "Unsupported file type. Please upload a CSV or Excel file."

        # Basic validation: file must not be empty
        if df.empty:
            return None, "The uploaded file is empty."

        return df, None  # Success: return DataFrame, no error

    except Exception as e:
        return None, f"Error reading file: {str(e)}"