import json

def update_phase2():
    path = "notebooks/Technical_Appendix.ipynb"
    
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Define the code content for each cell of Phase 2
    cell_updates = {
        "# Analysis & Plot 1: Overall default rate distribution": [
            "# Analysis & Plot 1: Overall default rate distribution\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "default_counts = df_clean['default_next_month'].value_counts()\n",
            "default_rates = df_clean['default_next_month'].value_counts(normalize=True) * 100\n",
            "\n",
            "print(\"--- Default Counts ---\")\n",
            "print(default_counts)\n",
            "print(\"\\n--- Default Rates (%) ---\")\n",
            "print(default_rates)\n",
            "\n",
            "# Sleek Pie Chart\n",
            "fig, ax = plt.subplots(figsize=(6, 6))\n",
            "colors = ['#4A90E2', '#E06666']  # Sleek blue and red\n",
            "ax.pie(default_counts, labels=['No Default (0)', 'Default (1)'], autopct='%1.1f%%', \n",
            "       startangle=90, colors=colors, explode=(0, 0.1), shadow=True,\n",
            "       textprops={'fontsize': 12, 'weight': 'bold'})\n",
            "ax.set_title('Overall Credit Card Default Rate', fontsize=14, weight='bold', pad=20)\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Analysis & Plot 2: Default rate by Age Bands": [
            "# Analysis & Plot 2: Default rate by Age Bands\n",
            "# Group ages into standard bands: Under 25, 25-34, 35-44, 45-54, 55+\n",
            "age_bins = [0, 24, 34, 44, 54, 100]\n",
            "age_labels = ['Under 25', '25-34', '35-44', '45-54', '55+']\n",
            "df_clean['age_band'] = pd.cut(df_clean['age'], bins=age_bins, labels=age_labels)\n",
            "\n",
            "age_default = df_clean.groupby('age_band')['default_next_month'].mean().reset_index()\n",
            "age_default['default_rate'] = age_default['default_next_month'] * 100\n",
            "\n",
            "print(age_default)\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8, 5))\n",
            "sns.barplot(data=age_default, x='age_band', y='default_rate', palette='Blues_d', ax=ax)\n",
            "ax.set_title('Default Rate by Age Band', fontsize=14, weight='bold', pad=15)\n",
            "ax.set_xlabel('Age Band', fontsize=12)\n",
            "ax.set_ylabel('Default Rate (%)', fontsize=12)\n",
            "for p in ax.patches:\n",
            "    ax.annotate(f\"{p.get_height():.1f}%\", (p.get_x() + p.get_width() / 2., p.get_height() + 0.5),\n",
            "                ha='center', va='center', fontsize=10, weight='bold', color='black', xytext=(0, 5),\n",
            "                textcoords='offset points')\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Analysis & Plot 3: Default rate by Education Level": [
            "# Analysis & Plot 3: Default rate by Education Level\n",
            "edu_default = df_clean.groupby('education')['default_next_month'].mean().reset_index()\n",
            "edu_default['default_rate'] = edu_default['default_next_month'] * 100\n",
            "edu_default = edu_default.sort_values(by='default_rate', ascending=False)\n",
            "\n",
            "print(edu_default)\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8, 5))\n",
            "sns.barplot(data=edu_default, x='education', y='default_rate', palette='Oranges_d', ax=ax)\n",
            "ax.set_title('Default Rate by Education Level', fontsize=14, weight='bold', pad=15)\n",
            "ax.set_xlabel('Education Level', fontsize=12)\n",
            "ax.set_ylabel('Default Rate (%)', fontsize=12)\n",
            "for p in ax.patches:\n",
            "    ax.annotate(f\"{p.get_height():.1f}%\", (p.get_x() + p.get_width() / 2., p.get_height() + 0.5),\n",
            "                ha='center', va='center', fontsize=10, weight='bold', color='black', xytext=(0, 5),\n",
            "                textcoords='offset points')\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Analysis & Plot 4: Default rate by Marital Status": [
            "# Analysis & Plot 4: Default rate by Marital Status\n",
            "marriage_default = df_clean.groupby('marriage')['default_next_month'].mean().reset_index()\n",
            "marriage_default['default_rate'] = marriage_default['default_next_month'] * 100\n",
            "marriage_default = marriage_default.sort_values(by='default_rate', ascending=False)\n",
            "\n",
            "print(marriage_default)\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8, 5))\n",
            "sns.barplot(data=marriage_default, x='marriage', y='default_rate', palette='Greens_d', ax=ax)\n",
            "ax.set_title('Default Rate by Marital Status', fontsize=14, weight='bold', pad=15)\n",
            "ax.set_xlabel('Marital Status', fontsize=12)\n",
            "ax.set_ylabel('Default Rate (%)', fontsize=12)\n",
            "for p in ax.patches:\n",
            "    ax.annotate(f\"{p.get_height():.1f}%\", (p.get_x() + p.get_width() / 2., p.get_height() + 0.5),\n",
            "                ha='center', va='center', fontsize=10, weight='bold', color='black', xytext=(0, 5),\n",
            "                textcoords='offset points')\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Analysis & Plot 5: Default rate by Credit Limit Tiers": [
            "# Analysis & Plot 5: Default rate by Credit Limit Tiers\n",
            "# Group limits into logical tiers: Low, Medium, High, Premium\n",
            "limit_bins = [0, 50000, 150000, 300000, 10000000]\n",
            "limit_labels = ['Low (<50k)', 'Medium (50k-150k)', 'High (150k-300k)', 'Premium (300k+)']\n",
            "df_clean['limit_tier'] = pd.cut(df_clean['limit_balance'], bins=limit_bins, labels=limit_labels)\n",
            "\n",
            "limit_default = df_clean.groupby('limit_tier')['default_next_month'].mean().reset_index()\n",
            "limit_default['default_rate'] = limit_default['default_next_month'] * 100\n",
            "\n",
            "print(limit_default)\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8, 5))\n",
            "sns.barplot(data=limit_default, x='limit_tier', y='default_rate', palette='Purples_d', ax=ax)\n",
            "ax.set_title('Default Rate by Credit Limit Tier', fontsize=14, weight='bold', pad=15)\n",
            "ax.set_xlabel('Credit Limit Tier', fontsize=12)\n",
            "ax.set_ylabel('Default Rate (%)', fontsize=12)\n",
            "for p in ax.patches:\n",
            "    ax.annotate(f\"{p.get_height():.1f}%\", (p.get_x() + p.get_width() / 2., p.get_height() + 0.5),\n",
            "                ha='center', va='center', fontsize=10, weight='bold', color='black', xytext=(0, 5),\n",
            "                textcoords='offset points')\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Analysis & Plot 6: Delinquency status vs. Default probability": [
            "# Analysis & Plot 6: Delinquency status vs. Default probability\n",
            "# Group repayment status on pay_status_1 (most recent month: September)\n",
            "df_clean['pay_group_1'] = np.where(df_clean['pay_status_1'] <= 0, 'On Time / Paid Full', \n",
            "                                   df_clean['pay_status_1'].astype(str) + ' Month(s) Delay')\n",
            "\n",
            "pay_default = df_clean.groupby('pay_group_1')['default_next_month'].mean().reset_index()\n",
            "pay_default['default_rate'] = pay_default['default_next_month'] * 100\n",
            "\n",
            "# Sort logically: On Time, then 1 month, 2 months, etc.\n",
            "pay_default['sort_val'] = np.where(pay_default['pay_group_1'] == 'On Time / Paid Full', 0, \n",
            "                                   pay_default['pay_group_1'].str.extract('(\\d+)').astype(float)[0])\n",
            "pay_default = pay_default.sort_values(by='sort_val')\n",
            "\n",
            "print(pay_default)\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(10, 5))\n",
            "sns.barplot(data=pay_default, x='pay_group_1', y='default_rate', palette='Reds_d', ax=ax)\n",
            "ax.set_title('Default Rate by Most Recent Repayment Status (September)', fontsize=14, weight='bold', pad=15)\n",
            "ax.set_xlabel('Repayment Status (PAY_1)', fontsize=12)\n",
            "ax.set_ylabel('Default Rate (%)', fontsize=12)\n",
            "plt.xticks(rotation=15)\n",
            "for p in ax.patches:\n",
            "    ax.annotate(f\"{p.get_height():.1f}%\", (p.get_x() + p.get_width() / 2., p.get_height() + 0.5),\n",
            "                ha='center', va='center', fontsize=10, weight='bold', color='black', xytext=(0, 5),\n",
            "                textcoords='offset points')\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Analysis & Plot 7: Bill amount vs. Payment amount distribution": [
            "# Analysis & Plot 7: Bill amount vs. Payment amount distribution\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "# Average Bill Boxplot\n",
            "sns.boxplot(data=df_clean, x='default_next_month', y='average_bill', palette='Set2', showfliers=False, ax=axes[0])\n",
            "axes[0].set_title('Average Monthly Bill: Defaulters vs Non-Defaulters', fontsize=12, weight='bold')\n",
            "axes[0].set_xticklabels(['No Default (0)', 'Default (1)'])\n",
            "axes[0].set_xlabel('Default Flag', fontsize=11)\n",
            "axes[0].set_ylabel('Average Bill Amount (TWD)', fontsize=11)\n",
            "\n",
            "# Average Payment Boxplot\n",
            "sns.boxplot(data=df_clean, x='default_next_month', y='average_payment', palette='Set2', showfliers=False, ax=axes[1])\n",
            "axes[1].set_title('Average Monthly Payment: Defaulters vs Non-Defaulters', fontsize=12, weight='bold')\n",
            "axes[1].set_xticklabels(['No Default (0)', 'Default (1)'])\n",
            "axes[1].set_xlabel('Default Flag', fontsize=11)\n",
            "axes[1].set_ylabel('Average Payment Amount (TWD)', fontsize=11)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Analysis & Plot 8: Correlation Heatmap": [
            "# Analysis & Plot 8: Correlation Heatmap\n",
            "corr_cols = [\n",
            "    'limit_balance', 'age', 'default_next_month', \n",
            "    'average_bill', 'average_payment', 'payment_to_bill_ratio', \n",
            "    'delayed_months', 'max_delay', 'credit_utilization', 'balance_trend'\n",
            "]\n",
            "corr_matrix = df_clean[corr_cols].corr()\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(10, 8))\n",
            "sns.heatmap(corr_matrix, annot=True, fmt=\".2f\", cmap=\"coolwarm\", vmin=-1, vmax=1, ax=ax)\n",
            "ax.set_title('Correlation Matrix of Behavioral and Credit Features', fontsize=14, weight='bold', pad=15)\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
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
    print("Phase 2 cells updated successfully!")

if __name__ == "__main__":
    update_phase2()
