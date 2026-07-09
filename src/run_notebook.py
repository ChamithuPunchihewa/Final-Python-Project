import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def run_notebook():
    notebook_path = "notebooks/Technical_Appendix.ipynb"
    print(f"Executing notebook: {notebook_path}")
    
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        
        # Execute the notebook cells using the active python kernel
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})
        
        # Save the notebook with executed outputs
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
            
        print("Notebook executed successfully!")
        
        # Check if the output CSV was created
        csv_path = "data/processed/cleaned_credit_data.csv"
        if os.path.exists(csv_path):
            print(f"Success! Cleaned dataset created at: {csv_path}")
            print(f"File size: {os.path.getsize(csv_path) / 1024:.2f} KB")
        else:
            print("Warning: Cleaned CSV was not created. Please check the notebook log for errors.")
            
    except Exception as e:
        print(f"Error executing notebook: {e}")

if __name__ == "__main__":
    run_notebook()
