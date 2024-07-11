import os
import re

# Base directories for output and time logs for CPLEX, Max-SAT, OR-Tools, Max-cdcl, Maxhs, and open-wbo
base_output_dir_ceplex = "./PcMisCeplex"
base_output_dir_maxsat = "./PcMisMax-sat/RC2"
base_output_dir_ortools = "./PcMisOrTools"
base_output_dir_maxcdcl = "./PcMisMax-sat/Max-cdcl"
base_output_dir_maxhs = "./PcMisMax-sat/Maxhs"
base_output_dir_openwbo = "./PcMisMax-sat/open-wbo"

# Function to read objective value from CPLEX output file
def read_ceplex_result(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "Objective value:" in line:
                    return float(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

# Function to read cost from Max-SAT output file
def read_maxsat_result(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "Model has cost:" in line:
                    return float(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

# Function to read cost from other Max-SAT solvers (Max-cdcl, Maxhs, open-wbo) output file
def read_other_maxsat_result(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("o"):
                    return float(line.split()[1].strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

# Function to read objective value from OR-Tools output file
def read_ortools_result(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "Objective value:" in line:
                    return float(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

# Function to convert time in various formats to seconds
def time_to_seconds(time_str):
    try:
        # Match format '0m8,383s' or '0m8.383s'
        match = re.match(r'(\d+)m(\d+)[,.](\d+)s', time_str)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            milliseconds = int(match.group(3))
            total_seconds = minutes * 60 + seconds + milliseconds / 1000
            return total_seconds
        # Match format '8.383s'
        match = re.match(r'(\d+)[,.](\d+)s', time_str)
        if match:
            seconds = int(match.group(1))
            milliseconds = int(match.group(2))
            total_seconds = seconds + milliseconds / 1000
            return total_seconds
        # Match format '8s'
        match = re.match(r'(\d+)s', time_str)
        if match:
            return int(match.group(1))
    except Exception as e:
        print(f"Error converting time '{time_str}': {e}")
    return None

# Function to read real time from time file and convert to seconds
def read_time(file_path):
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith("real"):
                    time_str = line.split()[1].strip()  # Extract time string
                    return time_to_seconds(time_str)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

# Function to generate combined LaTeX table for CPLEX, Max-SAT, OR-Tools, Max-cdcl, Maxhs, and open-wbo
def generate_combined_latex_table():
    latex_table = "\\begin{table}[ht]\n"
    latex_table += "\\centering\n"
    latex_table += "\\caption{Summary of CPLEX, Max-SAT, OR-Tools, Max-cdcl, Maxhs, and open-wbo results}\n"
    latex_table += "\\hspace*{-4cm}\\resizebox{1.7\\linewidth}{!}{\n"
    latex_table += "\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|} \\hline\n"
    latex_table += "Instance & CPLEX Obj. Value & CPLEX Time (s) & Max-SAT Cost & Max-SAT Time (s) & OR-Tools Obj. Value & OR-Tools Time (s) & Max-cdcl Cost & Max-cdcl Time (s) & Maxhs Cost & Maxhs Time (s) & open-wbo Cost & open-wbo Time (s) \\\\ \\hline\n"
    
    for i in range(1, 41):  # Instances from pmed1 to pmed40
        instance_name = f"pmed{i}"
        
        # File paths for CPLEX
        ceplex_output_file = os.path.join(base_output_dir_ceplex, instance_name, f"output{instance_name}.txt")
        ceplex_time_file = os.path.join(base_output_dir_ceplex, instance_name, f"time{instance_name}.txt")
        
        # File paths for Max-SAT
        maxsat_output_file = os.path.join(base_output_dir_maxsat, instance_name, f"output{instance_name}.txt")
        maxsat_time_file = os.path.join(base_output_dir_maxsat, instance_name, f"time{instance_name}.txt")
        
        # File paths for OR-Tools
        ortools_output_file = os.path.join(base_output_dir_ortools, instance_name, f"output{instance_name}.txt")
        ortools_time_file = os.path.join(base_output_dir_ortools, instance_name, f"time{instance_name}.txt")

        # File paths for Max-cdcl
        maxcdcl_output_file = os.path.join(base_output_dir_maxcdcl, instance_name, f"output_{instance_name}.txt")
        maxcdcl_time_file = os.path.join(base_output_dir_maxcdcl, instance_name, f"time_{instance_name}.txt")
        
        # File paths for Maxhs
        maxhs_output_file = os.path.join(base_output_dir_maxhs, instance_name, f"output_{instance_name}.txt")
        maxhs_time_file = os.path.join(base_output_dir_maxhs, instance_name, f"time_{instance_name}.txt")
        
        # File paths for open-wbo
        openwbo_output_file = os.path.join(base_output_dir_openwbo, instance_name, f"output_{instance_name}.txt")
        openwbo_time_file = os.path.join(base_output_dir_openwbo, instance_name, f"time_{instance_name}.txt")
        
        # Read results and execution times
        ceplex_objective_value = read_ceplex_result(ceplex_output_file)
        ceplex_execution_time = read_time(ceplex_time_file)
        maxsat_cost = read_maxsat_result(maxsat_output_file)
        maxsat_execution_time = read_time(maxsat_time_file)
        ortools_objective_value = read_ortools_result(ortools_output_file)
        ortools_execution_time = read_time(ortools_time_file)
        maxcdcl_cost = read_other_maxsat_result(maxcdcl_output_file)
        maxcdcl_execution_time = read_time(maxcdcl_time_file)
        maxhs_cost = read_other_maxsat_result(maxhs_output_file)
        maxhs_execution_time = read_time(maxhs_time_file)
        openwbo_cost = read_other_maxsat_result(openwbo_output_file)
        openwbo_execution_time = read_time(openwbo_time_file)
        
        # Populate LaTeX table row
        latex_table += f"{instance_name} & "
        latex_table += f"{ceplex_objective_value:.2f} " if ceplex_objective_value is not None else ""
        latex_table += f"& {ceplex_execution_time:.3f} " if ceplex_execution_time is not None else "& "
        latex_table += f"& {maxsat_cost:.2f} " if maxsat_cost is not None else "& "
        latex_table += f"& {maxsat_execution_time:.3f} " if maxsat_execution_time is not None else "& "
        latex_table += f"& {ortools_objective_value:.2f} " if ortools_objective_value is not None else "& "
        latex_table += f"& {ortools_execution_time:.3f} " if ortools_execution_time is not None else "& "
        latex_table += f"& {maxcdcl_cost:.2f} " if maxcdcl_cost is not None else "& "
        latex_table += f"& {maxcdcl_execution_time:.3f} " if maxcdcl_execution_time is not None else "& "
        latex_table += f"& {maxhs_cost:.2f} " if maxhs_cost is not None else "& "
        latex_table += f"& {maxhs_execution_time:.3f} " if maxhs_execution_time is not None else "& "
        latex_table += f"& {openwbo_cost:.2f} " if openwbo_cost is not None else "& "
        latex_table += f"& {openwbo_execution_time:.3f} \\\\ \\hline\n" if openwbo_execution_time is not None else "& \\\\ \\hline\n"
    
    latex_table += "\\end{tabular}}\n"
    latex_table += "\\end{table}\n"
    
    return latex_table

# Main function to generate and print LaTeX table
def main():
    latex_table_combined = generate_combined_latex_table()
    
    print("LaTeX table for CPLEX, Max-SAT, OR-Tools, Max-cdcl, Maxhs, and open-wbo results:\n")
    print(latex_table_combined)

if __name__ == "__main__":
    main()
