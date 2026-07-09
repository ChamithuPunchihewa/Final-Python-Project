import json

def update_phase1():
    path = "notebooks/Technical_Appendix.ipynb"
    
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Define the code content for each cell
    cell_updates = {
        "# 2. Initial Assessment": [
            "# 2. Initial Assessment\n",
            "print(\"--- Data Info ---\")\n",
            "print(df_raw.info())\n",
            "\n",
            "print(\"\\n--- Missing Values ---\")\n",
            "print(df_raw.isnull().sum())\n",
            "\n",
            "print(\"\\n--- Raw Columns in df_raw ---\")\n",
            "print(df_raw.columns.tolist())\n",
            "\n",
            "# Check demographic column values to understand raw codes\n",
            "demographics = ['SEX', 'EDUCATION', 'MARRIAGE']\n",
            "for col in demographics:\n",
            "    if col in df_raw.columns:\n",
            "        print(f\"\\nValue counts for {col}:\")\n",
            "        print(df_raw[col].value_counts(dropna=False))\n"
        ],
        "# 3. Rename Columns to python_friendly_names": [
            "# 3. Rename Columns to python_friendly_names\n",
            "rename_dict = {\n",
            "    'LIMIT_BAL': 'limit_balance',\n",
            "    'SEX': 'sex',\n",
            "    'EDUCATION': 'education',\n",
            "    'MARRIAGE': 'marriage',\n",
            "    'AGE': 'age',\n",
            "    'PAY_0': 'pay_status_1',  # In UCI, PAY_0 is the first month's repayment status\n",
            "    'PAY_2': 'pay_status_2',\n",
            "    'PAY_3': 'pay_status_3',\n",
            "    'PAY_4': 'pay_status_4',\n",
            "    'PAY_5': 'pay_status_5',\n",
            "    'PAY_6': 'pay_status_6',\n",
            "    'BILL_AMT1': 'bill_amount_1',\n",
            "    'BILL_AMT2': 'bill_amount_2',\n",
            "    'BILL_AMT3': 'bill_amount_3',\n",
            "    'BILL_AMT4': 'bill_amount_4',\n",
            "    'BILL_AMT5': 'bill_amount_5',\n",
            "    'BILL_AMT6': 'bill_amount_6',\n",
            "    'PAY_AMT1': 'pay_amount_1',\n",
            "    'PAY_AMT2': 'pay_amount_2',\n",
            "    'PAY_AMT3': 'pay_amount_3',\n",
            "    'PAY_AMT4': 'pay_amount_4',\n",
            "    'PAY_AMT5': 'pay_amount_5',\n",
            "    'PAY_AMT6': 'pay_amount_6',\n",
            "    'default payment next month': 'default_next_month'\n",
            "}\n",
            "\n",
            "# Handle minor name variations if any\n",
            "if 'default payment next month' not in df_raw.columns and 'default.payment.next.month' in df_raw.columns:\n",
            "    rename_dict['default.payment.next.month'] = 'default_next_month'\n",
            "\n",
            "df_clean = df_raw.rename(columns=rename_dict)\n",
            "\n",
            "# Drop ID column since it has no predictive power\n",
            "if 'ID' in df_clean.columns:\n",
            "    df_clean = df_clean.drop(columns=['ID'])\n",
            "\n",
            "print(\"Columns renamed successfully!\")\n",
            "print(df_clean.columns.tolist())\n"
        ],
        "# 4. Decode Categories (Sex, Education, Marriage)": [
            "# 4. Decode Categories (Sex, Education, Marriage)\n",
            "# Decode numeric codes to business-friendly readable labels\n",
            "\n",
            "# SEX: 1 = Male, 2 = Female\n",
            "sex_map = {1: 'Male', 2: 'Female'}\n",
            "\n",
            "# EDUCATION: 1 = Graduate School, 2 = University, 3 = High School, 4,5,6,0 = Others/Unknown\n",
            "edu_map = {\n",
            "    1: 'Graduate School',\n",
            "    2: 'University',\n",
            "    3: 'High School',\n",
            "    4: 'Others',\n",
            "    5: 'Others',\n",
            "    6: 'Others',\n",
            "    0: 'Others'\n",
            "}\n",
            "\n",
            "# MARRIAGE: 1 = Married, 2 = Single, 3 = Others (0 is undocumented/unknown)\n",
            "marriage_map = {\n",
            "    1: 'Married',\n",
            "    2: 'Single',\n",
            "    3: 'Others',\n",
            "    0: 'Others'\n",
            "}\n",
            "\n",
            "df_clean['sex'] = df_clean['sex'].map(sex_map)\n",
            "df_clean['education'] = df_clean['education'].map(edu_map)\n",
            "df_clean['marriage'] = df_clean['marriage'].map(marriage_map)\n",
            "\n",
            "print(\"--- Decoded Category Distributions ---\")\n",
            "print(\"\\nSex:\\n\", df_clean['sex'].value_counts())\n",
            "print(\"\\nEducation:\\n\", df_clean['education'].value_counts())\n",
            "print(\"\\nMarriage:\\n\", df_clean['marriage'].value_counts())\n"
        ],
        "# 5. Handle Duplicates & Invalid Values": [
            "# 5. Handle Duplicates & Invalid Values\n",
            "# Find duplicate rows\n",
            "dups = df_clean.duplicated().sum()\n",
            "print(f\"Number of duplicate rows: {dups}\")\n",
            "if dups > 0:\n",
            "    df_clean = df_clean.drop_duplicates()\n",
            "    print(\"Duplicate rows removed.\")\n",
            "\n",
            "# Age range validation\n",
            "print(f\"Age range: {df_clean['age'].min()} to {df_clean['age'].max()} years\")\n",
            "\n",
            "# Check limit balance range\n",
            "print(f\"Limit Balance range: {df_clean['limit_balance'].min()} to {df_clean['limit_balance'].max()} TWD\")\n",
            "\n",
            "# Verify repayment status ranges\n",
            "pay_cols = [f'pay_status_{i}' for i in range(1, 7)]\n",
            "print(\"\\nRepayment status ranges (should be between -2 and 9):\")\n",
            "for col in pay_cols:\n",
            "    print(f\"{col}: min={df_clean[col].min()}, max={df_clean[col].max()}\")\n"
        ],
        "# 6. Feature Engineering": [
            "# 6. Feature Engineering\n",
            "bill_cols = [f'bill_amount_{i}' for i in range(1, 7)]\n",
            "pay_amt_cols = [f'pay_amount_{i}' for i in range(1, 7)]\n",
            "pay_status_cols = [f'pay_status_{i}' for i in range(1, 7)]\n",
            "\n",
            "# A. Average bill amount\n",
            "df_clean['average_bill'] = df_clean[bill_cols].mean(axis=1)\n",
            "\n",
            "# B. Average payment amount\n",
            "df_clean['average_payment'] = df_clean[pay_amt_cols].mean(axis=1)\n",
            "\n",
            "# C. Payment-to-bill ratio (overall sum of payments / sum of bills to avoid divide-by-zero on individual months)\n",
            "total_bills = df_clean[bill_cols].sum(axis=1)\n",
            "total_payments = df_clean[pay_amt_cols].sum(axis=1)\n",
            "df_clean['payment_to_bill_ratio'] = np.where(total_bills > 0, total_payments / total_bills, 0.0)\n",
            "\n",
            "# D. Number of delayed months (pay_status > 0 indicates delay)\n",
            "df_clean['delayed_months'] = (df_clean[pay_status_cols] > 0).sum(axis=1)\n",
            "\n",
            "# E. Maximum delay in repayment status\n",
            "df_clean['max_delay'] = df_clean[pay_status_cols].max(axis=1)\n",
            "\n",
            "# F. Balance trend (recent bill - oldest bill)\n",
            "df_clean['balance_trend'] = df_clean['bill_amount_1'] - df_clean['bill_amount_6']\n",
            "\n",
            "# G. Credit utilization (recent bill amount / limit balance)\n",
            "df_clean['credit_utilization'] = df_clean['bill_amount_1'] / df_clean['limit_balance']\n",
            "\n",
            "print(\"Behavioral features engineered successfully. Preview:\")\n",
            "preview_cols = ['limit_balance', 'average_bill', 'average_payment', 'payment_to_bill_ratio', 'delayed_months', 'max_delay', 'credit_utilization']\n",
            "print(df_clean[preview_cols].head())\n"
        ],
        "# df_cleaned.to_csv(\"../data/processed/cleaned_credit_data.csv\", index=False)": [
            "# 7. Persist Cleaned Data\n",
            "import os\n",
            "output_dir = \"../data/processed\"\n",
            "os.makedirs(output_dir, exist_ok=True)\n",
            "output_path = os.path.join(output_dir, \"cleaned_credit_data.csv\")\n",
            "\n",
            "df_clean.to_csv(output_path, index=False)\n",
            "print(f\"Cleaned dataset saved successfully to: {output_path}\")\n",
            "print(f\"Cleaned dataset shape: {df_clean.shape}\")\n"
        ]
    }

    # Apply updates to cells
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            for target_prefix, replacement_code in cell_updates.items():
                if any(target_prefix in line for line in cell["source"]):
                    cell["source"] = replacement_code
                    break

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Phase 1 cells updated successfully!")

if __name__ == "__main__":
    update_phase1()
