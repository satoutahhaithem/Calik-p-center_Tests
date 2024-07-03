import os

# Base directories for output and time logs for CPLEX and Max-SAT
base_output_dir_ceplex = "./PcMisCeplex"
base_output_dir_maxsat = "./PcMisMax-sat"

# Function to read objective value from CPLEX output file
def read_ceplex_result(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            objective_value = None
            for line in lines:
                if line.startswith("Objective value:"):
                    objective_value = float(line.split(":")[1].strip())
                    break
            return objective_value
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to read cost from Max-SAT output file
def read_maxsat_result(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            cost = None
            for line in lines:
                if line.startswith("Model has cost:"):
                    cost = float(line.split(":")[1].strip())
                    break
            return cost
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to read time from time file
def read_time(file_path):
    try:
        with open(file_path, 'r') as f:
            time_str = f.readline().strip()  # Read time string
            return time_str
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to generate LaTeX table for CPLEX
def generate_latex_table_ceplex():
    latex_table = "\\begin{table}[ht]\n"
    latex_table += "\\centering\n"
    latex_table += "\\caption{Summary of CPLEX results}\n"
    latex_table += "\\begin{tabular}{|l|l|l|l|} \\hline\n"
    latex_table += "Instance & Objective Value & Execution Time (seconds) \\\\ \\hline\n"
    
    for i in range(1, 41):  # Assuming instances are from pmed1 to pmed40
        instance_name = f"pmed{i}"
        output_file = os.path.join(base_output_dir_ceplex, instance_name, f"output{instance_name}.txt")
        time_file = os.path.join(base_output_dir_ceplex, instance_name, f"time{instance_name}.txt")
        
        objective_value = read_ceplex_result(output_file)
        execution_time = read_time(time_file)
        
        if objective_value is not None and execution_time is not None:
            latex_table += f"{instance_name} & {objective_value:.2f} & {execution_time} \\\\ \\hline\n"
    
    latex_table += "\\end{tabular}\n"
    latex_table += "\\end{table}\n"
    
    return latex_table

# Function to generate LaTeX table for Max-SAT
def generate_latex_table_maxsat():
    latex_table = "\\begin{table}[ht]\n"
    latex_table += "\\centering\n"
    latex_table += "\\caption{Summary of Max-SAT results}\n"
    latex_table += "\\begin{tabular}{|l|l|l|l|} \\hline\n"
    latex_table += "Instance & Cost & Execution Time (seconds) \\\\ \\hline\n"
    
    for i in range(1, 41):  # Assuming instances are from pmed1 to pmed40
        instance_name = f"pmed{i}"
        output_file = os.path.join(base_output_dir_maxsat, instance_name, f"output{instance_name}.txt")
        time_file = os.path.join(base_output_dir_maxsat, instance_name, f"time{instance_name}.txt")
        
        cost = read_maxsat_result(output_file)
        execution_time = read_time(time_file)
        
        if cost is not None and execution_time is not None:
            latex_table += f"{instance_name} & {cost:.2f} & {execution_time} \\\\ \\hline\n"
    
    latex_table += "\\end{tabular}\n"
    latex_table += "\\end{table}\n"
    
    return latex_table

# Main function to generate and print LaTeX tables
def main():
    latex_table_ceplex = generate_latex_table_ceplex()
    latex_table_maxsat = generate_latex_table_maxsat()
    
    print("LaTeX table for CPLEX results:\n")
    print(latex_table_ceplex)
    
    print("\nLaTeX table for Max-SAT results:\n")
    print(latex_table_maxsat)

if __name__ == "__main__":
    main()
