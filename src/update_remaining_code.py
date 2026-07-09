import json

def update_remaining():
    path = "notebooks/Technical_Appendix.ipynb"
    
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Define the code content for Phase 3, Phase 4, and Phase 5
    cell_updates = {
        "# 1. Define scoring functions for Delinquency, Capacity, and Exposure": [
            "# 1. Define scoring functions for Delinquency, Capacity, and Exposure\n",
            "def get_delinquency_score(row):\n",
            "    # Delinquency score (higher delay = higher risk)\n",
            "    delay = row['delayed_months']\n",
            "    if delay == 0:\n",
            "        return 1\n",
            "    elif delay == 1:\n",
            "        return 2\n",
            "    elif delay == 2:\n",
            "        return 3\n",
            "    elif delay <= 4:\n",
            "        return 4\n",
            "    else:\n",
            "        return 5\n",
            "\n",
            "def get_capacity_score(row):\n",
            "    # Repayment Capacity score (lower payment-to-bill ratio = higher risk)\n",
            "    ratio = row['payment_to_bill_ratio']\n",
            "    if ratio >= 0.8:\n",
            "        return 1\n",
            "    elif ratio >= 0.4:\n",
            "        return 2\n",
            "    elif ratio >= 0.2:\n",
            "        return 3\n",
            "    elif ratio >= 0.05:\n",
            "        return 4\n",
            "    else:\n",
            "        return 5\n",
            "\n",
            "def get_exposure_score(row):\n",
            "    # Exposure score (higher utilization = higher risk)\n",
            "    util = row['credit_utilization']\n",
            "    if util <= 0.1:\n",
            "        return 1\n",
            "    elif util <= 0.3:\n",
            "        return 2\n",
            "    elif util <= 0.6:\n",
            "        return 3\n",
            "    elif util <= 0.8:\n",
            "        return 4\n",
            "    else:\n",
            "        return 5\n",
            "print(\"Scoring functions defined successfully.\")\n"
        ],
        "# 2. Calculate dimension scores (1-5) using pd.qcut or custom binning rules": [
            "# 2. Calculate dimension scores (1-5) using pd.qcut or custom binning rules\n",
            "df_clean['delinquency_score'] = df_clean.apply(get_delinquency_score, axis=1)\n",
            "df_clean['capacity_score'] = df_clean.apply(get_capacity_score, axis=1)\n",
            "df_clean['exposure_score'] = df_clean.apply(get_exposure_score, axis=1)\n",
            "\n",
            "# Calculate combined score (ranges from 3 to 15)\n",
            "df_clean['total_risk_score'] = df_clean['delinquency_score'] + df_clean['capacity_score'] + df_clean['exposure_score']\n",
            "\n",
            "print(\"Dimension scores computed. Summary stats:\")\n",
            "print(df_clean[['delinquency_score', 'capacity_score', 'exposure_score', 'total_risk_score']].describe())\n"
        ],
        "# 3. Combine scores and map to business-friendly segments": [
            "# 3. Combine scores and map to business-friendly segments\n",
            "def map_to_segment(total_score):\n",
            "    if total_score <= 5:\n",
            "        return 'Healthy'\n",
            "    elif total_score <= 8:\n",
            "        return 'Watchlist'\n",
            "    elif total_score <= 11:\n",
            "        return 'At-Risk'\n",
            "    else:\n",
            "        return 'Critical'\n",
            "\n",
            "df_clean['risk_segment'] = df_clean['total_risk_score'].apply(map_to_segment)\n",
            "print(\"Decoded segments sizes:\")\n",
            "print(df_clean['risk_segment'].value_counts())\n"
        ],
        "# 4. Validate segments by computing actual default rates per segment": [
            "# 4. Validate segments by computing actual default rates per segment\n",
            "segment_stats = df_clean.groupby('risk_segment').agg(\n",
            "    count=('default_next_month', 'count'),\n",
            "    defaults=('default_next_month', 'sum'),\n",
            "    default_rate=('default_next_month', 'mean')\n",
            ").reset_index()\n",
            "segment_stats['default_rate'] = segment_stats['default_rate'] * 100\n",
            "\n",
            "# Sort in risk order\n",
            "segment_stats['risk_order'] = segment_stats['risk_segment'].map({'Healthy': 1, 'Watchlist': 2, 'At-Risk': 3, 'Critical': 4})\n",
            "segment_stats = segment_stats.sort_values('risk_order')\n",
            "\n",
            "print(\"--- Risk Segment Validation stats ---\")\n",
            "print(segment_stats)\n",
            "\n",
            "# Visual validation of default rates\n",
            "fig, ax = plt.subplots(figsize=(8, 5))\n",
            "colors = ['#2ca02c', '#bcbd22', '#ff7f0e', '#d62728']\n",
            "sns.barplot(data=segment_stats, x='risk_segment', y='default_rate', palette=colors, ax=ax)\n",
            "ax.set_title('Validation: Actual Default Rate by Credit-Risk Segment', fontsize=14, weight='bold', pad=15)\n",
            "ax.set_xlabel('Credit-Risk Segment', fontsize=12)\n",
            "ax.set_ylabel('Actual Default Rate (%)', fontsize=12)\n",
            "for p in ax.patches:\n",
            "    ax.annotate(f\"{p.get_height():.1f}%\", (p.get_x() + p.get_width() / 2., p.get_height() + 0.5),\n",
            "                ha='center', va='center', fontsize=11, weight='bold', color='black', xytext=(0, 5),\n",
            "                textcoords='offset points')\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ],
        "# Boxplot / Histogram of credit utilization across different segments": [
            "# Boxplot / Histogram of credit utilization across different segments\n",
            "fig, ax = plt.subplots(figsize=(10, 6))\n",
            "sns.boxplot(data=df_clean, x='risk_segment', y='credit_utilization', palette='Set3', showfliers=False, ax=ax)\n",
            "ax.set_title('Credit Utilization Ratio across Risk Segments', fontsize=14, weight='bold', pad=15)\n",
            "ax.set_xlabel('Risk Segment', fontsize=12)\n",
            "ax.set_ylabel('Credit Utilization Ratio', fontsize=12)\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "\n",
            "# Print average credit utilization\n",
            "util_stats = df_clean.groupby('risk_segment')['credit_utilization'].mean().reset_index()\n",
            "print(\"\\n--- Average Credit Utilization by Segment ---\")\n",
            "print(util_stats)\n"
        ],
        "# Define API endpoint (e.g. ExchangeRate-API or Open Exchange Rates)": [
            "# Define API endpoint (e.g. ExchangeRate-API or Open Exchange Rates)\n",
            "# Fetching currency rates using USD as base\n",
            "url = \"https://open.er-api.com/v6/latest/USD\"\n",
            "print(f\"Fetching exchange rates from: {url}\")\n",
            "\n",
            "try:\n",
            "    response = requests.get(url, timeout=10)\n",
            "    response.raise_for_status()\n",
            "    data = response.json()\n",
            "    \n",
            "    # Output sample response metadata\n",
            "    print(\"API Response Status:\", data.get(\"result\"))\n",
            "    print(\"Base Currency:\", data.get(\"base_code\"))\n",
            "    print(\"TWD rate found:\", data.get(\"rates\", {}).get(\"TWD\"))\n",
            "    \n",
            "    usd_to_twd = data.get(\"rates\", {}).get(\"TWD\")\n",
            "    if usd_to_twd:\n",
            "        twd_to_usd_rate = 1.0 / usd_to_twd\n",
            "        print(f\"Success: 1 TWD = {twd_to_usd_rate:.6f} USD\")\n",
            "    else:\n",
            "        twd_to_usd_rate = 1.0 / 32.5\n",
            "        print(\"TWD rate not in API response. Using fallback: 1 TWD = 0.0307 USD\")\n",
            "except Exception as e:\n",
            "    print(f\"API request failed: {e}\")\n",
            "    twd_to_usd_rate = 1.0 / 32.5\n",
            "    print(\"Using fallback exchange rate: 1 TWD = 0.0307 USD\")\n"
        ],
        "# Apply enrichment to the main DataFrame (e.g., LIMIT_BAL_USD)": [
            "# Apply enrichment to the main DataFrame (e.g., LIMIT_BAL_USD)\n",
            "# Convert LIMIT_BAL and average_bill to USD\n",
            "df_clean['limit_balance_usd'] = df_clean['limit_balance'] * twd_to_usd_rate\n",
            "df_clean['average_bill_usd'] = df_clean['average_bill'] * twd_to_usd_rate\n",
            "\n",
            "print(\"Dataset enriched with USD converted columns. Preview:\")\n",
            "print(df_clean[['limit_balance', 'limit_balance_usd', 'average_bill', 'average_bill_usd']].head())\n",
            "\n",
            "# Save the final processed dataset\n",
            "output_path = \"../data/processed/cleaned_credit_data.csv\"\n",
            "df_clean.to_csv(output_path, index=False)\n",
            "print(f\"\\nFinal enriched and cleaned dataset saved to: {output_path}\")\n"
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
    print("All remaining notebook cells populated successfully!")

if __name__ == "__main__":
    update_remaining()
