#!/bin/bash

# Define the timeout duration (if needed)
timeout_duration="3600s"

# Base directories for output and time logs for correctCeplex_from_file.py
base_output_dir_correct="./PcMisCeplex"
mkdir -p "$base_output_dir_correct"

# Loop through each instance number from 1 to 40 for correctCeplex_from_file.py
for ((i = 1; i <= 40; i++)); do
    instance_name="pmed${i}"
    instance_file="./instances/${instance_name}.txt"
    
    # Directories for each instance
    instance_output_dir="${base_output_dir_correct}/${instance_name}"
    mkdir -p "$instance_output_dir"
    
    # Output and time files
    output_file="${instance_output_dir}/output${instance_name}.txt"
    time_file="${instance_output_dir}/time${instance_name}.txt"
    
    # Run the program and log output and time for correctCeplex_from_file.py
    {
        time timeout --signal=INT "$timeout_duration" python3 correctCeplex_from_file.py "$instance_file" > "$output_file"
    } 2> "$time_file"
    
    echo "Execution times and outputs for instance $instance_name (correctCeplex_from_file.py) recorded in respective files."
done

echo "Execution times and outputs for all pmed instances (correctCeplex_from_file.py) recorded in respective files."


# Base directories for output and time logs for ParmMax-sat_read_from_file.py
base_output_dir_maxsat="./PcMisMax-sat"
mkdir -p "$base_output_dir_maxsat"

# Loop through each instance number from 1 to 40 for ParmMax-sat_read_from_file.py
for ((i = 1; i <= 40; i++)); do
    instance_name="pmed${i}"
    instance_file="./instances/${instance_name}.txt"
    
    # Directories for each instance
    instance_output_dir="${base_output_dir_maxsat}/${instance_name}"
    mkdir -p "$instance_output_dir"
    
    # Output and time files
    output_file="${instance_output_dir}/output${instance_name}.txt"
    time_file="${instance_output_dir}/time${instance_name}.txt"
    
    # Run the program and log output and time for ParmMax-sat_read_from_file.py
    {
        time timeout --signal=INT "$timeout_duration" python3 ParmMax-sat_read_from_file.py "$instance_file" > "$output_file"
    } 2> "$time_file"
    
    echo "Execution times and outputs for instance $instance_name (ParmMax-sat_read_from_file.py) recorded in respective files."
done

echo "Execution times and outputs for all pmed instances (ParmMax-sat_read_from_file.py) recorded in respective files."
