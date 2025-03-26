from fastapi import FastAPI, UploadFile, File
import pandas as pd
import numpy as np
# import json
import uvicorn
from io import StringIO

app = FastAPI()

json_file_path = "files.json"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read CSV content
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")), skiprows=4)

    # Identify year columns
    year_columns = [col for col in df.columns if col.isdigit()]
    
    # Ensure relevant columns are selected
    columns_needed = ["Country Name"] + year_columns
    df = df[columns_needed]

    # Remove non-country groups
    excluded_groups = ["World", "High income", "Low income", "Middle income", "OECD", "Euro area"]
    df = df[~df["Country Name"].str.contains('|'.join(excluded_groups), case=False, na=False)]

    # Convert population columns to numeric
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

    # Replace NaN and Inf values with None (JSON-compliant)
    df.replace([np.nan, np.inf, -np.inf], None, inplace=True)

    # Convert DataFrame to JSON and save
    df.to_json(json_file_path, orient="records", indent=4)

    return {"message": "File processed successfully", "filename": file.filename}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
