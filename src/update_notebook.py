import json

def update_notebook():
    path = "notebooks/Technical_Appendix.ipynb"
    
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Find the cell containing "# 1. Load Data"
    updated = False
    for cell in nb["cells"]:
        if cell["cell_type"] == "code" and any("# 1. Load Data" in line for line in cell["source"]):
            cell["source"] = [
                "# 1. Load Data\n",
                "import os\n",
                "\n",
                "raw_dir = \"../data/raw\"\n",
                "files = [f for f in os.listdir(raw_dir) if f.startswith(\"default of credit card\")]\n",
                "\n",
                "if files:\n",
                "    file_name = files[0]\n",
                "    data_path = os.path.join(raw_dir, file_name)\n",
                "    print(f\"Found dataset: {data_path}\")\n",
                "    \n",
                "    try:\n",
                "        if file_name.endswith('.csv'):\n",
                "            df_raw = pd.read_csv(data_path, skiprows=1)\n",
                "        elif file_name.endswith(('.xls', '.xlsx')):\n",
                "            df_raw = pd.read_excel(data_path, skiprows=1)\n",
                "        \n",
                "        print(f\"Data loaded successfully! Shape: {df_raw.shape}\")\n",
                "        print(df_raw.head())\n",
                "    except Exception as e:\n",
                "        print(f\"Error loading data: {e}\")\n",
                "else:\n",
                "    print(\"Dataset not found in data/raw folder. Please check if the file is there.\")"
            ]
            updated = True
            break

    if updated:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print("Notebook updated successfully!")
    else:
        print("Could not find the target cell to update.")

if __name__ == "__main__":
    update_notebook()
