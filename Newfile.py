#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:55:28 2023

@author: expert
"""


import streamlit as st
import pandas as pd
import os
import time
from decimal import Decimal

st.title("Sensor Data Analysis Report Dashboard")

# Input and output folder paths
input_folder_path = "streaming_data"
output_folder_path = "output"
output_file_path = os.path.join(output_folder_path, "output.txt")

# Check if output folder exists, if not create one
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Function to count total records in CSV and calculate summary statistics for each sensor ID
def count_records(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        return 0, {}
    unique_ids = df['Sensor ID'].unique()
    counts = df['Sensor ID'].value_counts().to_dict()
    sensor_data = {}
    
    for sensor_id in unique_ids:
        # Calculate summary statistics
        sensor_df = df[df['Sensor ID'] == sensor_id]
        time_diffs = sensor_df['Time Difference (s)'].dropna()
        mean_interval = round(time_diffs.mean(), 2) if len(time_diffs) > 0 else None
        max_interval = round(time_diffs.max(), 2) if len(time_diffs) > 0 else None
        min_interval = round(time_diffs.min(), 2) if len(time_diffs) > 0 else None
        sensor_data[sensor_id] = {
            'count': counts.get(sensor_id, 0),
            'Average Interval': mean_interval,
            'Maximum Interval': max_interval,
            'Minimum Interval': min_interval
        }
    return len(df), sensor_data

# Function to update output file with new total
def update_output_file(total):
    with open(output_file_path, "a") as f:
        f.write(str(Decimal(total)) + "\n")

# Streamlit app
def main():
    st.subheader("Data Report and Summary Statistics")

    # Check if output file exists, if not create one with initial value of 0
    if not os.path.exists(output_file_path):
        update_output_file(0)

    # Read current total from output file
    with open(output_file_path, "r") as f:
        current_totals = f.readlines()
        current_total = sum([Decimal(x.strip()) for x in current_totals])

    processed_csv_files = set()
    total_records = 0
    sensor_data = {} 

    # Initialize session state variables
    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = time.time()
    if 'current_total' not in st.session_state:
        st.session_state.current_total = current_total
    if 'total_records' not in st.session_state:
        st.session_state.total_records = total_records
    if 'sensor_data' not in st.session_state:
        st.session_state.sensor_data = sensor_data

    # Check for new CSV files
    # Streamlit app
#def main():
    #st.subheader("Data Report and Summary Statistics")

    # Check if output file exists, if not create one with initial value of 0
    if not os.path.exists(output_file_path):
        update_output_file(0)

    # Read current total from output file
    with open(output_file_path, "r") as f:
        current_totals = f.readlines()
        current_total = sum([Decimal(x.strip()) for x in current_totals])

    processed_csv_files = set()
    total_records = 0
    sensor_data = {} 

    while True:
        # Check for new CSV files in input folder
        csv_files = [f for f in os.listdir(input_folder_path) if f.endswith(".csv")]
        if len(csv_files) > 0:
            for csv_file in csv_files:
                if csv_file not in processed_csv_files:
                    csv_path = os.path.join(input_folder_path, csv_file)
                    count, data = count_records(csv_path)
                    total_records += count
                    sensor_data.update(data)
                    processed_csv_files.add(csv_file)
            current_total += total_records
            update_output_file(current_total)

            st.subheader("1. Total Number Of Records")
            st.write(f"Number of Records: {total_records}")

            #st.subheader("2. Sensor ID and its Value counts")
            #sensor_count_df = pd.DataFrame.from_dict(sensor_data, orient='index', columns=['Value counts'])
            #sensor_count_df.index.name = 'Sensor ID'
            #sensor_count_df.reset_index(inplace=True)
            #st.dataframe(sensor_count_df)

            st.subheader("2. Summary Statistics Of Sensor ID")
            sensor_df = pd.DataFrame.from_dict(sensor_data, orient='index')
            sensor_df.index.name = 'Sensor ID'
            sensor_df.reset_index(inplace=True)
            # Convert count column to float
            sensor_df['count'] = pd.to_numeric(sensor_df['count'], errors='coerce')

            # Drop rows with NaN values
            sensor_df.dropna(inplace=True)

            # Convert count column back to integer
            sensor_df['count'] = sensor_df['count'].astype(int)

            # Calculate summary statistics
            #sensor_df['Mean Time Difference (s)'] = sensor_df['Average Interval'].astype(float)
            #sensor_df['Max Time Difference (s)'] = sensor_df['Maximum Interval'].astype(float)
            #sensor_df['Min Time Difference (s)'] = sensor_df['Minimum Interval'].astype(float)
            #sensor_df.drop(['Average Interval', 'Maximum Interval', 'Minimum Interval'], axis=1, inplace=True)

            st.dataframe(sensor_df)

        # Refresh the app every 5 seconds
        st.experimental_rerun()
        time.sleep(5)


if __name__ == "__main__":
    main()

