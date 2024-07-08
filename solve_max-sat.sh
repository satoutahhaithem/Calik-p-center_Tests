#!/bin/bash

# Directory containing the instances
INSTANCE_DIR="max-sat_instance"
timeout_duration="3600"
solver_dir="Solvers"




chmod +x "$solver_dir/maxcdcl_static"
chmod +x "$solver_dir/open-wbo"
chmod +x "$solver_dir/maxhs"



# Check if the instance directory exists
if [ ! -d "$INSTANCE_DIR" ]; then
  echo "Instance directory $INSTANCE_DIR does not exist."
  exit 1
fi

# Loop from pmed1 to pmed40
for i in {1..40}
do
  FILENAME="pmed$i.txt"
  FILEPATH="$INSTANCE_DIR/$FILENAME"
  
  # Check if the file exists
  if [ -f "$FILEPATH" ]; then
    echo "Processing $FILENAME..."
    { 
        time timeout "$timeout_duration" "$solver_dir/maxcdcl_static" "$FILEPATH" > "$output_dir/${max_parallel_sessions}_session_maxcdcl_static_output.txt"
    } 2> "$time_dir/${max_parallel_sessions}_session_maxcdcl_static_time.txt"
  else
    echo "File $FILENAME does not exist."
  fi
done

echo "All instances processed."










################################################################################################################################################################################################
cnf_file="max-sat_instance/${yearRodef}/${max_parallel_sessions}_session_file_new_format.wcnf"



timeout_duration="3600"
solver_dir="Solvers"



chmod +x "$solver_dir/EvalMaxSAT"
chmod +x "$solver_dir/maxcdcl"
chmod +x "$solver_dir/open-wbo"
chmod +x "$evalMaxSatFolder"
chmod +x "$maxcdclFolder"



# Loop through the years and loop through all the instance 
for yearRodef in {2021..2022}; do
    # output_dir="outputs/${yearRodef}"
    # time_dir="TimeSolver/${yearRodef}"
    output_dir="outputsPcHeythem/${yearRodef}"
    time_dir="TimeSolverPcHeythem/${yearRodef}"
    # output_dir="outputsPcHeythemChangeEncType/${yearRodef}"
    # time_dir="TimeSolverPcHeythemChangeEncType/${yearRodef}"
    # max_parallel_sessions_range_2024=($(seq 16 -1 9))
    max_parallel_sessions_range_2024=($(seq 15 -1 10))
    max_parallel_sessions_range_2023=($(seq 20 -1 13))
    max_parallel_sessions_range_2022=($(seq 15 -1 11))
    max_parallel_sessions_range_2021=($(seq 10 -1 5))
    case $yearRodef in
        2024)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2024[@]}")
            ;;
        2023)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2023[@]}")
            ;;
        2022)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2022[@]}")
            ;;
        2021)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2021[@]}")
            ;;
        *)
            echo "Year not supported"
            exit 1
    esac


    # Ensure directories exist
    # mkdir -p "$output_dir"
    # mkdir -p "$time_dir"

    # all the instance of one year
    for max_parallel_sessions in "${max_parallel_sessions_range[@]}"; do
        cnf_file="instance/${yearRodef}/${max_parallel_sessions}_session_file_new_format.wcnf"
        cnf_file_old_format="instance/${yearRodef}/${max_parallel_sessions}_session_file.wcnf"

        # This command of rc2 is "rc2.py -s 'cd' instance/2023/10_session_file.wcnf" for 10 par exemple work with rc2.py
        # { 
        #     time timeout "$timeout_duration" rc2.py -s 'cd' --verbose "$cnf_file_old_format"  >> "$output_dir/${max_parallel_sessions}_session_Rc2_output.txt"
        # } 2> "$time_dir/${max_parallel_sessions}_session_Rc2_time.txt"

        # { 
        #     time timeout "$timeout_duration" "$solver_dir/maxcdcl_static" "$cnf_file_old_format" > "$output_dir/${max_parallel_sessions}_session_maxcdcl_static_output.txt"
        # } 2> "$time_dir/${max_parallel_sessions}_session_maxcdcl_static_time.txt"

        # { 
        #     time timeout "$timeout_duration" "$solver_dir/EvalMaxSAT" "$cnf_file" > "$output_dir/${max_parallel_sessions}_session_EvalMaxSAT_output.txt"
        # } 2> "$time_dir/${max_parallel_sessions}_session_EvalMaxSAT_time.txt"

        # { 
        #     time timeout "$timeout_duration" "$solver_dir/open-wbo" "$cnf_file_old_format" > "$output_dir/${max_parallel_sessions}_session_open-wbo_output.txt"
        #  } 2> "$time_dir/${max_parallel_sessions}_session_open-wbo_time.txt"
        #  { 
        #      time timeout "$timeout_duration" "$solver_dir/maxhs" -no-printSoln "$cnf_file_old_format" > "$output_dir/${max_parallel_sessions}_session_maxhs_output.txt"
        #   } 2> "$time_dir/${max_parallel_sessions}_session_maxhs_time.txt"

        { 
            time timeout "$timeout_duration" "$solver_dir/cashwmaxsatcoreplus" "$cnf_file_old_format" > "$output_dir/${max_parallel_sessions}_session_cashwmaxsatcoreplus_output.txt"
        } 2> "$time_dir/${max_parallel_sessions}_session_cashwmaxsatcoreplus_time.txt"


    done

    echo "Execution times and outputs for year $yearRodef recorded in respective files."
done

