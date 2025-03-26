Population Analysis Dashboard 🌍📊
Overview:-
This is a Streamlit-based interactive dashboard for analyzing global population data. Users can:

- Upload a CSV file with population data.

- Filter data using natural language queries.

- Visualize data using Bar Charts, Line Charts, Pie Charts, and Choropleth Maps.

- Interact with a FastAPI backend that processes the uploaded CSV and prepares it for visualization.



🚀 Features
- Upload & Store CSV Data – Avoids re-uploading the same file.
- AI-Free Query-Based Filtering – Extracts countries and years using regex.
- Multiple Data Visualizations:

📊 Bar Chart – Compare country populations.

📈 Line Chart – Track population trends over time.

🥧 Pie Chart – Show a single country’s population distribution across years.

🗺️ Choropleth Map – Visualize global population density.
✔ FastAPI Backend – Processes CSV files into JSON format.




📂 Project Structure

📦 Population-Analysis-Dashboard
├── 📜 app.py        # Streamlit frontend for visualization
├── 📜 main.py       # FastAPI backend for processing uploaded CSVs
├── 📂 uploads       # Directory to store uploaded CSV files
├── 📜 files.json    # Processed JSON data used by the app
├── 📜 requirements.txt  # List of dependencies
└── 📜 README.md     # Project documentation
