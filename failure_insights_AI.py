#read data from excel
#summarize the data using python
#feed consolidated data to llama3 for business insights
import pandas as pd
from ollama import chat

filepath = "D:/New folder/Preparations/Learn python/Practice/py Data/AI projects/payment_ai_sample_data.xlsx"
df = pd.read_excel(filepath)

#KPI calculations
total_orders = df['Total orders'].sum()
total_revenues = df['Total revenue'].sum()
unique_banks = df['Top banks'].unique()
# Calculate failure rate using Status column
failed_orders = df[df["Status"].str.lower() == "failed"]["Total orders"].sum()
success_orders = df[df["Status"].str.lower() == "success"]["Total orders"].sum()
success_revenues = df[df["Status"].str.lower() == "success"]["Total revenue"].sum()
failure_rate = (failed_orders / total_orders) * 100 if total_orders != 0 else 0

#top bank failed volume
top_bank_failures = top_failed_bank = (
    df[df["Status"].str.lower() == "failed"]
    .groupby("Top banks")["Total orders"]
    .sum()
    .sort_values(ascending=False)
    .idxmax()
)
#top payment method failed volume
top_payment_failures = top_failed_payment = (
    df[df["Status"].str.lower() == "failed"]
    .groupby("Top methods")["Total orders"]
    .sum()
    .sort_values(ascending=False)
    .idxmax()
)
# Most common failure reason
top_failure_reason = df["Failure reasons"].value_counts().idxmax()

# Status distribution
status_distribution = df["Status"].value_counts()

# Time trend distribution
trend_summary = df["Time trend"].value_counts().to_string()

#unique bank names
unique_bank_counts = df["Top banks"].value_counts()

# Create Structured Summary
summary_text = f"""
Payment Performance Summary

Total Orders: {total_orders}
Total Revenue: ₹{total_revenues}

Failed Orders: {failed_orders}
Successful Orders: {success_orders}
Overall Failure Rate: {failure_rate:.2f}%

Highest Failure Bank (by volume): {top_failed_bank}
Highest Failure Method (by volume): {top_payment_failures}

Top Failure Reason: {top_failure_reason}

Status Distribution:
{status_distribution.to_string()}

Time Trend Distribution:
{trend_summary}

Unique bank account counts:
{unique_bank_counts}
"""

print("\n====== DATA SUMMARY ======")
print(summary_text)

# Send to Llama3

response = chat(
    model ="llama3",
    messages=[
        {
        "role": "system",
        "content": "You are a senior ecommerce payment analytics consultant."
        },
        {
            "role": "user",
            "content": f"""
            Analyze this payment performance summary.
            Provide:
            1. Key risk areas
            2. Root cause insights
            3. Business impact
            4. Actionable recommendations
            5. Strategic improvement ideas

            Summary:
            {summary_text}
            """
           }
        ]
)

print("\n====== AI BUSINESS INSIGHTS ======")
print(response.message.content)
print("-" * 60)