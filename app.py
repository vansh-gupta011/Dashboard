import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import os
import re

# Directory to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(layout="wide")
st.title("Population Analysis")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    
    if os.path.exists(file_path):
        st.warning(f"⚠️ File '{uploaded_file.name}' already exists.")
    else:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ File uploaded and stored successfully!")
        
        # Send file to FastAPI backend
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/upload", files=files)

        if response.status_code == 200:
            st.success("File processed successfully!")
        else:
            st.error("Error processing file.")

    # Load processed data
    with open("files.json", "r") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    
    # Identify year columns
    year_columns = [col for col in df.columns if col.isdigit()]
    df[year_columns] = df[year_columns].apply(pd.to_numeric, errors='coerce')
    df["Mean Population"] = df[year_columns].mean(axis=1) / 1e9  # Convert to billions

    # User Query Input
    st.subheader("🔍 Filter Data")
    user_query = st.text_input("Type your query (e.g., 'Show me data for China and India from 2001 to 2015.')")

    if user_query:
        # Extract Countries using Regex
        country_pattern = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b', user_query)
        
        # Extract Year Range
        year_pattern = re.findall(r'\b(19[0-9]{2}|20[0-9]{2})\b', user_query)
        if len(year_pattern) >= 2:
            start_year, end_year = int(year_pattern[0]), int(year_pattern[1])
        else:
            start_year, end_year = None, None

        # Apply Country Filtering
        if country_pattern:
            country_list = [c.lower() for c in country_pattern]
            df = df[df["Country Name"].str.lower().isin(country_list)]

        # Apply Year Filtering
        if start_year and end_year:
            selected_years = [col for col in year_columns if start_year <= int(col) <= end_year]
            df = df[["Country Name"] + selected_years]

        # Graph Selection
        graph_type = st.selectbox("Choose graph type", ["Bar Chart", "Line Chart", "Pie Chart", "Choropleth Map"])
        
        # Plot Graph
        if graph_type == "Bar Chart":
            fig = px.bar(df.melt(id_vars=["Country Name"], var_name="Year", value_name="Population"),
            
                         x="Country Name", y="Population", color="Year", title="Population by Country and Year")
        elif graph_type == "Line Chart":
            fig = px.line(df.melt(id_vars=["Country Name"], var_name="Year", value_name="Population"),
               
                          x="Year", y="Population", color="Country Name", title="Population Trend")
        elif graph_type == "Pie Chart":
            if len(country_pattern) == 1 and len(selected_years) >= 2:
                country = country_pattern[0]
                df_country = df[df["Country Name"].str.lower() == country.lower()]

                if not df_country.empty:
                    df_pie = df_country.melt(id_vars=["Country Name"], var_name="Year", value_name="Population")
                    df_pie = df_pie[df_pie["Year"].astype(int).between(start_year, end_year)]

                    if not df_pie.empty:
                        fig = px.pie(df_pie, names="Year", values="Population", 
                             title=f"Population Distribution in {country} ({start_year}-{end_year})")
                    else:
                        st.warning("⚠️ No population data available for the selected range.")
                        fig = None
                else:
                    st.warning("⚠️ Selected country not found in data.")
                    fig = None
            else:
                st.warning("⚠️ Please select exactly one country and a valid year range (start and end year).")
                fig = None

        elif graph_type == "Choropleth Map":
            latest_year = selected_years[-1] if selected_years else None
            if latest_year:
                fig = px.choropleth(df, locations="Country Name", locationmode="country names",
                                    color=latest_year, title=f"Population Map for {latest_year}",
                                    color_continuous_scale="Viridis",  # Updated color scale for better contrast
                                    range_color=(df[latest_year].min(), df[latest_year].max()))
            else:
                st.warning("⚠️ No data available for selected years.")
                fig = None

        if fig:
            st.plotly_chart(fig, use_container_width=True)
