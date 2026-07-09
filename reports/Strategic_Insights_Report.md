# FINAL PROJECT REPORT: CREDIT RISK ANALYSIS AND CUSTOMER SEGMENTATION FOR FINTRUST DIGITAL FINANCE

**Course Module:** ITS 2122 - Python for Data Science & AI  
**Group Submission:** Strategic Insight Report  
**Date of Submission:** July 9, 2026  
**Target Audience:** Executive Board of FinTrust Digital Finance  

---

## 1. Executive Summary

This report presents a data-driven credit risk analysis and customer segmentation model developed for FinTrust Digital Finance. FinTrust has scaled its personal credit and digital credit card business rapidly over recent years. However, its risk monitoring and debt collection protocols have remained manual, leaving the firm vulnerable to defaults. To address this, our team analyzed historical transaction and demographic data from 30,000 credit card accounts to build an automated early-warning framework.

Our initial exploration of the portfolio showed a baseline default rate of 22.1%. Risk is not distributed evenly across the customer base. We found that younger borrowers (under 25) and those with lower educational levels exhibit default rates exceeding 25%. Similarly, clients with low credit limits (under 50,000 TWD) present a very high default rate of 32.4%. On the other hand, clients with larger credit limits (above 300,000 TWD) default at a rate of only 13.9%, suggesting that historical underwriting was effective at filtering high-earning, low-risk clients.

Rather than treating all borrowers the same, we built a multi-dimensional risk scoring model. This model grades customers on three behavioral features: Delinquency (the number of months payments were late), Repayment Capacity (the ratio of payments to statements), and Financial Exposure (credit limit utilization). Summing these scores allowed us to segment borrowers into four distinct groups:
* **Healthy Segment (30.3% of the portfolio):** This group has an actual default rate of 13.9%. These customers pay regularly and maintain very low balances relative to their credit limits.
* **Watchlist Segment (22.0% of the portfolio):** This group defaults at a rate of 16.4%. These customers show minor payment delays or slight drops in their repayment ratios.
* **At-Risk Segment (34.7% of the portfolio):** This group exhibits a default rate of 20.7% and is characterized by revolving balances and low monthly payments.
* **Critical Segment (13.0% of the portfolio):** This group has a very high default rate of 54.9%. These borrowers have severe delays and high credit utilization.

To mitigate portfolio risk, we recommend three key actions:
1. **Apply tailored collection strategies:** Send automated SMS alerts to Watchlist accounts, offer structured payment plans to At-Risk clients, and immediately freeze credit lines for Critical accounts.
2. **Revise underwriting guidelines:** Lower initial credit limits for younger, high-risk demographics and adjust limit expansion thresholds.
3. **Macroeconomic monitoring:** Use public currency exchange rate APIs to track inflation and exchange rates to dynamically adjust underwriting limits for international reporting.

---

## 2. Introduction and Business Context

Digital lending platforms operate in a highly competitive environment where managing defaults is critical to survival. FinTrust Digital Finance has built a large customer base of salaried individuals. While the platform has successfully grown its book of loans, it has struggled to keep defaults low. Currently, collections and credit decisions are made manually by staff, which is slow and cannot scale.

To help FinTrust transition to a data-driven model, this project establishes a clean data pipeline and builds a behavioral scoring model. The primary objectives are:
* **Data Cleaning and Standardization:** Set up a reproducible pipeline to ingest raw data, handle missing or invalid category codes, and clean anomalies.
* **Behavioral Feature Engineering:** Calculate indicators that capture monthly repayment habits, bill trends, and credit utilization.
* **Exploratory Risk Profiling:** Uncover how demographic factors (age, education, marital status) and financial factors (credit limits, bill sizes) drive defaults.
* **Risk Scoring and Segmentation:** Group customers into clear financial health categories to allow the risk team to apply targeted policies.
* **Macroeconomic Enrichment:** Integrate external exchange rate data via APIs to support reporting in multiple currencies and contextualize risk.

---

## 3. Data Cleaning and Preprocessing Pipeline

### 3.1 Raw Dataset Audit
We used the public "Default of Credit Card Clients" dataset, containing records of 30,000 accounts. The data covers a six-month period from April 2005 to September 2005. Each record contains demographic data, granted credit limits, six months of billing statements, six months of repayment amounts, and a historical flag indicating if the client defaulted in October 2005.

The raw data contained several inconsistencies and undocumented codes that we had to resolve in Pandas:
* **Column Renaming:** Raw column names were converted to pythonic lowercase names (e.g., `LIMIT_BAL` to `limit_balance`, `PAY_0` to `pay_status_1`, and the target variable to `default_next_month`).
* **Demographic Code Mapping:** Categorical variables like `sex`, `education`, and `marriage` were stored as numbers. `sex` was decoded into 'Male' and 'Female'. In the raw data, `education` had undocumented codes (0, 5, 6), and `marriage` had an undocumented code (0). We grouped these undocumented codes into 'Others' since they could not be reliably mapped to specific levels.
* **Duplicate and Outlier Audit:** We scanned for duplicate rows and found none. We verified that age distributions were realistic (ranging from 21 to 79 years) and that bill and payment values did not contain impossible characters.

### 3.2 Engineering Behavioral Features
To capture client payment habits over time, we engineered several variables:
* **Average Bill Amount:** The mean statement balance across the six-month period.
* **Average Payment Amount:** The mean payment amount across the six-month period.
* **Payment-to-Bill Ratio:** Calculated as the sum of all payments divided by the sum of all bills over the six months. Using the sum avoids division-by-zero errors that occur if we calculate monthly ratios where the bill is zero.
* **Delayed Months:** A count of how many months (out of six) the client had a late payment status (repayment status greater than 0).
* **Maximum Delay:** The worst delinquency status recorded for the client during the six months.
* **Credit Utilization:** Calculated as the client's most recent bill statement (`bill_amount_1`) divided by their `limit_balance`.
* **Balance Trend:** The difference between the first month's bill and the sixth month's bill, indicating whether the client is accumulating or paying off debt.

---

## 4. Exploratory Data Analysis (EDA)

Our team analyzed the clean dataset to identify the main drivers of default risk. The results show strong links between client attributes and defaults.

### 4.1 Portfolio Baseline
Out of the 30,000 clients, 6,636 defaulted in the final month, representing a **22.1%** baseline default rate. This high default rate shows that FinTrust's manual risk controls are not working effectively.

### 4.2 Demographic Risk Profiles
* **Age Distribution:** We grouped clients into five age bands. The relationship between age and default rates follows a U-shape. Younger clients (under 25) have a high default rate of **26.9%**. Default rates drop for clients aged 25–34 (20.3%) and 35–44 (21.4%), before rising again for older clients aged 45–54 (22.7%) and those over 55 (**26.9%**). The high risk among young clients is likely due to lower income levels and less experience managing credit.
* **Education Levels:** Educational levels are closely related to default rates. Clients with university degrees have a default rate of **23.7%**, and high school graduates have a rate of **25.2%**. The lowest risk is found among clients with graduate school degrees (**19.2%**), indicating that higher education correlates with more stable employment and better financial management.
* **Marital Status:** Married clients exhibit a default rate of **23.5%**, while single clients have a rate of **20.9%**. This difference suggests that household financial obligations and expenses make married clients slightly more vulnerable to defaults during financial stress.

### 4.3 Credit Limit Analysis
Credit limits act as a clear indicator of borrower quality. We binned the limits into four tiers and analyzed their default rates:
* **Low Tier (<50,000 TWD):** Default rate of **32.4%**.
* **Medium Tier (50,000–150,000 TWD):** Default rate of **22.2%**.
* **High Tier (150,000–300,000 TWD):** Default rate of **17.4%**.
* **Premium Tier (>300,000 TWD):** Default rate of **13.9%**.
This distribution shows that higher credit limits correspond to lower default risk. This suggests that the underwriting team was successful in identifying low-risk borrowers, but they need to be more careful with clients granted smaller limits, as they represent the largest concentration of defaults.

### 4.4 Repayment Delays as Early Warning Signals
The strongest predictor of default is the client's repayment status. In the dataset, repayment status is coded from -2 (no consumption) to 0 (revolving credit, paid minimum) and positive integers (1, 2, 3... representing months of payment delay). 

We analyzed the most recent repayment status from September (`pay_status_1`). Clients who paid on time or used revolving credit responsibly had a default rate of only **13.1%**. However, clients who delayed their payment by just one month had a default rate of **33.9%**. For clients with a two-month delay, the default rate jumped to **69.1%**, and for a three-month delay, it reached **75.9%**. This shows that even a single missed payment is a strong warning sign that requires immediate action.

### 4.5 Billing and Payment Disparities
We compared the average bill sizes and payment sizes of defaulting and non-defaulting clients. The results show that both groups receive similar average monthly bills (defaulters average ~48,500 TWD, while non-defaulters average ~44,900 TWD). 

However, there is a massive gap in payment behavior. Non-defaulting clients pay an average of 5,200 TWD monthly, while defaulting clients pay only 2,200 TWD. Defaulters are not running up larger bills; they simply lack the liquidity to make meaningful payments, resulting in unpaid balances that roll over and eventually lead to default.

---

## 5. Credit-Risk Scoring and Customer Segmentation Model

To help FinTrust move away from manual heuristics, we developed an interpretable credit scoring model. This model scores each customer on three key behavioral areas, with each area graded from 1 (lowest risk) to 5 (highest risk):

1. **Delinquency Score:** Graded based on the count of delayed months. 0 delayed months = 1; 1 month = 2; 2 months = 3; 3–4 months = 4; 5–6 months = 5.
2. **Repayment Capacity Score:** Graded based on the overall payment-to-bill ratio. A ratio >= 0.8 = 1; 0.4 to 0.8 = 2; 0.2 to 0.4 = 3; 0.05 to 0.2 = 4; < 0.05 = 5.
3. **Exposure Score:** Graded based on credit utilization. Utilization <= 10% = 1; 10–30% = 2; 30–60% = 3; 60–80% = 4; > 80% = 5.

### 5.1 Segmentation and Risk Validation
By summing these three scores, we calculate a total risk score for each client (ranging from 3 to 15). We mapped these total scores to four segments:
* **Healthy (Scores 3–5):** Clients with low utilization, regular payments, and no delays.
* **Watchlist (Scores 6–8):** Clients with occasional short-term delays or slightly higher utilization.
* **At-Risk (Scores 9–11):** Clients with frequent delays, low payment ratios, and revolving debt.
* **Critical (Scores 12–15):** Clients with severe, persistent late payments and high credit utilization.

We validated the model by calculating the actual default rate for each segment:
* **Healthy Segment (9,085 clients):** Default rate of **13.9%**.
* **Watchlist Segment (6,594 clients):** Default rate of **16.4%**.
* **At-Risk Segment (10,402 clients):** Default rate of **20.7%**.
* **Critical Segment (3,884 clients):** Default rate of **54.9%**.

The clear, steady increase in default rates across the segments validates the model's accuracy. It separates low-risk accounts from those requiring urgent intervention, providing the risk department with a reliable framework.

---

## 6. External Data Integration via Exchange Rate API

To support international reporting and evaluate credit risk in a global context, we enriched our database using external exchange rate data. 

Using the Python `requests` library, we called the public API `https://open.er-api.com/v6/latest/USD` to fetch real-time exchange rates. The API returned a structured JSON payload. During execution, the API returned a rate of **1 USD = 32.5 TWD** (which translates to a conversion rate of **1 TWD = 0.0307 USD**).

We used this rate to convert our primary financial metrics from TWD to USD:
* `limit_balance_usd` = `limit_balance` * 0.0307
* `average_bill_usd` = `average_bill` * 0.0307

### Business Value of Data Enrichment
* **Standardized Corporate Reporting:** Converting financial exposures to USD allows FinTrust's board and international investors to assess portfolio risk using standardized global benchmarks.
* **Macroeconomic Risk Indicator:** Exchange rates are a good indicator of local economic conditions. A depreciating local currency often points to rising domestic inflation, which pressure household cash flows and drives defaults. Tracking exchange rate movements helps the risk department adjust credit margins proactively.

---

## 7. Actionable Credit Policies, Ethics, and Limitations

### 7.1 Segment-Specific Policies
* **Healthy Segment:** Offer credit limit increases, lower interest rates, and premium rewards to increase customer loyalty and loan balances.
* **Watchlist Segment:** Set up automated reminders via SMS and email 3 days before payment due dates. Offer options to change payment dates to match salary cycles.
* **At-Risk Segment:** Conduct manual reviews and stop automatic limit expansions. Contact these borrowers to offer balance conversion programs (converting high-rate revolving debt into structured, lower-rate monthly installments).
* **Critical Segment:** Immediately freeze credit cards to prevent further utilization. Route these accounts to active collections and offer settlement options before taking legal action.

### 7.2 Ethical Considerations in Credit Risk Modeling
Automated risk scoring models can easily introduce bias if not implemented carefully:
* **Demographic Discrimination:** Our data shows that younger and less-educated borrowers have higher default rates. However, using age or education directly in underwriting would systematically exclude these groups, making it harder for them to access financial services. Underwriting models should focus strictly on financial behavior (payment history, cash flow, utilization) rather than demographic attributes.
* **Transparency and Redress:** Clients placed in high-risk categories (At-Risk or Critical) must have access to clear explanations for these decisions and should be provided with actionable steps to improve their score.

### 7.3 Data and Model Limitations
* **Short Observation Window:** The dataset only covers a six-month period, which is not long enough to capture seasonal spending cycles (e.g., holiday seasons) or long-term economic shifts.
* **Missing Financial Context:** The dataset lacks critical variables like monthly income, employment status, total external debt, and overall debt-to-income (DTI) ratios. Adding these indicators would greatly improve the accuracy and predictive power of the scoring model.

---
**End of Report.**
