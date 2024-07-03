#!/bin/bash

# Define the timeout duration (if needed)
timeout_duration="3600s"

# Base directories for output and time logs
base_output_dir="./PcMisMax-sat"

# Ensure base directory exists
mkdir -p "$base_output_dir"

# Loop through each instance number from 1 to 40
for ((i = 1; i <= 40; i++)); do
    instance_name="pmed${i}"
    instance_file="./instances/${instance_name}.txt"
    
    # Directories for each instance
    instance_output_dir="${base_output_dir}/${instance_name}"
    mkdir -p "$instance_output_dir"
    
    # Output and time files
    output_file="${instance_output_dir}/output${instance_name}.txt"
    time_file="${instance_output_dir}/time${instance_name}.txt"
    
    # Run the program and log output and time
    {
        time timeout --signal=INT "$timeout_duration" python3 ParmMax-sat_read_from_file.py "$instance_file" > "$output_file"
    } 2> "$time_file"
    
    echo "Execution times and outputs for instance $instance_name recorded in respective files."
done

echo "Execution times and outputs for all pmed instances recorded in respective files."
