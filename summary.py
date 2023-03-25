import os
import csv
import time
import statistics

# Set the path to the folders
input_folder = 'streaming_data'
output_folder = 'output'

# Create the output folder if it doesn't exist

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize the total row count, sensor count, and dictionaries to store sensor time intervals
total_rows = 0
sensor_counts = {}
sensor_avg_times = {}
sensor_max_times = {}
sensor_min_times = {}
unique_sensor_ids = set()

while True:
    # Get a list of CSV files in the input folder
    csv_files = [filename for filename in os.listdir(input_folder) if filename.endswith('.csv')]

    if not csv_files:
        print('There are no CSV files in the input folder.')
        time.sleep(5)
        continue

    # Process each CSV file
    for csv_file in csv_files:
        # Open the CSV file for reading
        with open(os.path.join(input_folder, csv_file), 'r') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row
            header_row = next(reader, None)
            if header_row is None:
                print(f'The file {csv_file} is empty or contains only a header row.')
                continue

            # Count the number of rows and sensor IDs in the file
            for row in reader:
                sensor_id = row[1]
                total_rows += 1
                if sensor_id == '' or sensor_id == '00':
                    continue  # Skip rows with empty or "00" sensor ID
                if sensor_id in sensor_counts:
                    sensor_counts[sensor_id] += 1
                else:
                    sensor_counts[sensor_id] = 1
                    unique_sensor_ids.add(sensor_id)

                if row[3] == '':
                    print(f'Time interval value is empty in file {csv_file}, row {total_rows}.')
                    continue

                try:
                    time_interval = float(row[3])
                except ValueError:
                    print(f'Invalid time interval value in file {csv_file}, row {total_rows}: {row[3]}')
                    continue

                if sensor_id in sensor_avg_times:
                    sensor_avg_times[sensor_id].append(time_interval)
                    sensor_max_times[sensor_id] = max(sensor_max_times[sensor_id], time_interval)
                    sensor_min_times[sensor_id] = min(sensor_min_times[sensor_id], time_interval)
                else:
                    sensor_avg_times[sensor_id] = [time_interval]
                    sensor_max_times[sensor_id] = time_interval
                    sensor_min_times[sensor_id] = time_interval

        # Write the updated counts and time interval statistics to the "output.txt" file in the "output" folder
        output_file_path = os.path.join(output_folder, 'output.txt')
        with open(output_file_path, 'w') as outfile:
            outfile.write(f'Total number of rows processed: {total_rows}\n\n')
            outfile.write(f'Number of unique sensor IDs: {len(unique_sensor_ids)}\n')
            outfile.write('Count of '
                          'Sensor ID\n\n')
            outfile.write('Sensor ID                  Count\n')
            outfile.write('---------------------------------\n')
            for sensor_id, count in sorted(sensor_counts.items(), key=lambda x: x[1], reverse=True):
                if sensor_id == '' or sensor_id == '00':
                    continue  # Skip rows with empty or "00" sensor ID
                formatted_sensor_id = ':'.join([s_id.upper().zfill(2) for s_id in sensor_id.split(':')])
                outfile.write(f'{formatted_sensor_id}\t\t{count:,}\n')
            outfile.write('---------------------------------\n')
            outfile.write('Summary Statistics of Sensor ID: \n\n')
            outfile.write('Sensor ID         \tAverage Interval\tMaximum Interval\tMinimum Interval\n')
            outfile.write('---------------------------------------------------------------------------------------\n')
            sorted_sensor_counts = sorted(sensor_counts.items(), key=lambda x: x[1], reverse=True)
            # for sensor_id, count in sorted_sensor_counts:
            for sensor_id in sorted(sensor_avg_times.keys()):
                if sensor_id == '' or sensor_id == '00':
                    continue  # Skip rows with empty or "00" sensor ID
                formatted_sensor_id = ':'.join([s_id.upper().zfill(2) for s_id in sensor_id.split(':')])
                avg_time = statistics.mean(sensor_avg_times[sensor_id])
                max_time_rounded = int(round(sensor_max_times[sensor_id]))
                min_time_rounded = int(round(sensor_min_times[sensor_id]))
                outfile.write(f'{formatted_sensor_id}\t\t\t{avg_time:.2f}\t\t\t'
                              f'{max_time_rounded}\t\t\t{min_time_rounded}\n')

                # outfile.write(f'{formatted_sensor_id}\t\t\t{avg_time:.2f}\t\t\t'
                #               f'{sensor_max_times[sensor_id]:.2f}\t\t\t{sensor_min_times[sensor_id]:.2f}\n')

        # Move the processed file to the output folder
        os.rename(os.path.join(input_folder, csv_file), os.path.join(output_folder, csv_file))

    # Wait for 5 seconds before checking for new files again
    time.sleep(5)
