import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import os
from app.utils.chatgpt import generate_summary
from app.services.supabase_client import get_data
from app.utils.data_normalization import normalize_column, normalize_term, normalize_emp_length
from app.constants.database import TABLE_NAME  # Import TABLE_NAME from constants

# Set the matplotlib backend to a non-GUI backend
matplotlib.use("Agg")  # This ensures plots are not rendered visually

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def analyze_loan_amount_distribution():
    """Analyze and visualize the distribution of loan amounts and generate a summary."""
    data = await get_data(TABLE_NAME)
    df = pd.DataFrame(data)
    
    if "loan_amnt" not in df:
        raise ValueError("Column 'loan_amnt' is missing in the dataset.")
    
    # Ensure 'loan_amnt' is numeric and valid
    df["loan_amnt"] = pd.to_numeric(df["loan_amnt"], errors="coerce")
    if df["loan_amnt"].isnull().all():
        raise ValueError("Loan amount data contains only invalid values.")

    # Generate a histogram
    plt.figure(figsize=(10, 6))
    df["loan_amnt"].plot(kind="hist", bins=50, color="skyblue", edgecolor="black")
    plt.title("Distribution of Loan Amounts")
    plt.xlabel("Loan Amount")
    plt.ylabel("Frequency")
    plt.tight_layout()

    # Save to base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close()  # Close the plot to free memory

    # Generate a summary using ChatGPT
    summary = await generate_summary(
        statistics=df["loan_amnt"].describe(),
        prompt=(
            "The dataset contains information about the distribution of loan amounts (loan_amt). "
            "Analyze the following statistical summary and provide an insightful interpretation:\n\n"
            "{statistics}\n\n"
            "In your analysis, include the following points:\n"
            "1. The total number of loans in the dataset.\n"
            "2. The range of loan amounts (minimum and maximum values).\n"
            "3. The average (mean) loan amount and what it suggests about the dataset.\n"
            "4. Key percentiles (25th, 50th/median, and 75th) and how they reflect the data distribution.\n"
            "5. Any significant trends or clusters in the data (e.g., most common loan amount ranges or outliers).\n"
            "6. Any observations on how the loan amounts are distributed (e.g., skewed, uniform, or normal).\n\n"
            "Write the summary in a simple and easy-to-understand manner, suitable for someone without a technical background."
        ),
    )

    return {"image": f"data:image/png;base64,{encoded_image}", "summary": summary}

async def grade_vs_defaults():
    """Identify which loan grade is most frequently associated with defaults and generate a summary."""
    # Fetch data
    data = await get_data(TABLE_NAME)
    df = pd.DataFrame(data)

    # Check for required columns
    if "grade" not in df or "is_bad" not in df:
        raise ValueError("Columns 'grade' or 'is_bad' are missing in the dataset.")

    # Group by grade and calculate default counts
    grade_defaults = df[df["is_bad"] == 1].groupby("grade").size()
    grade_defaults = grade_defaults.sort_values(ascending=False)

    # Visualization
    plt.figure(figsize=(8, 5))
    grade_defaults.plot(kind="bar", color="salmon")
    plt.title("Loan Grades Associated with Defaults")
    plt.xlabel("Grade")
    plt.ylabel("Number of Defaults")
    plt.tight_layout()

    # Save the chart to base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close()  # Close the plot to free memory

    # Generate a summary using ChatGPT
    grade_summary_stats = grade_defaults.to_string()  # Convert summary stats to a string format
    prompt = (
        f"The dataset contains information about loan grades and their default counts. "
        f"Below are the default counts for each grade:\n\n"
        f"{grade_summary_stats}\n\n"
        f"Using this information, provide a concise summary that includes:\n"
        f"1. The grade most frequently associated with defaults.\n"
        f"2. How the distribution of defaults varies across grades.\n"
        f"3. Any notable patterns or observations from the data.\n\n"
        f"Make the summary simple and easy to understand for someone without a technical background."
    )
    summary = await generate_summary(statistics=grade_summary_stats, prompt=prompt)

    return {
        "image": f"data:image/png;base64,{encoded_image}",
        "table": grade_defaults.to_dict(),
        "summary": summary,
    }

async def state_wise_defaults():
    """Evaluate state-wise loan distributions and default rates."""
    data = await get_data(TABLE_NAME)
    df = pd.DataFrame(data)

    if "addr_state" not in df or "is_bad" not in df:
        raise ValueError("Columns 'addr_state' or 'is_bad' are missing in the dataset.")

    # Calculate state-wise loan counts and default rates
    state_loan_counts = df.groupby("addr_state").size()
    state_defaults = df[df["is_bad"] == 1].groupby("addr_state").size()
    default_rates = (state_defaults / state_loan_counts).fillna(0).sort_values(ascending=False)

    # Highlight states with the highest and lowest default rates
    highest_default_rate = default_rates.head(5)
    lowest_default_rate = default_rates.tail(5)

    # Visualization
    plt.figure(figsize=(12, 6))
    default_rates.plot(kind="bar", color="orange")
    plt.title("State-Wise Default Rates")
    plt.xlabel("State")
    plt.ylabel("Default Rate")
    plt.tight_layout()

    # Save to base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close()  # Close the plot to free memory

    # Generate summary using ChatGPT
    summary_prompt = (
        f"The dataset contains information about state-wise loan distributions and default rates. "
        f"Here are the calculated default rates for each state:\n\n"
        f"{default_rates.to_string()}\n\n"
        f"Using this information, provide a concise summary that includes:\n"
        f"1. The states with the highest default rates and their rates.\n"
        f"2. The states with the lowest default rates and their rates.\n"
        f"3. Observations on how default rates vary across states.\n"
        f"4. Any significant trends or clusters observed in the data.\n\n"
        f"Write the summary in simple terms for easy understanding."
    )
    summary = await generate_summary(default_rates.to_string(), summary_prompt)

    return {
        "image": f"data:image/png;base64,{encoded_image}",
        "highest_default_rate": highest_default_rate.to_dict(),
        "lowest_default_rate": lowest_default_rate.to_dict(),
        "summary": summary,
    }

async def risk_factors_analysis():
    """Analyze factors contributing to high-default loans."""
    # Fetch data from Supabase
    data = await get_data(TABLE_NAME)
    df = pd.DataFrame(data)

    # Check for required columns
    if "is_bad" not in df:
        raise ValueError("Column 'is_bad' is missing in the dataset.")

    # Normalize 'is_bad' column
    df["is_bad"] = normalize_column(df, "is_bad", dtype="int")

    # Normalize other columns
    if "term" in df.columns:
        df["term"] = df["term"].apply(normalize_term).fillna(0).astype(float)

    if "grade" in df.columns:
        df["grade"] = df["grade"].str.strip().fillna("Unknown")

    if "sub_grade" in df.columns:
        df["sub_grade"] = df["sub_grade"].str.strip().fillna("Unknown")

    if "emp_length" in df.columns:
        df["emp_length"] = df["emp_length"].apply(normalize_emp_length)

    # Ensure numeric columns are used for correlation
    numeric_columns = df.select_dtypes(include=["number"]).columns

    # Ensure all numeric columns have valid values
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Calculate correlations with 'is_bad'
    correlation = df[numeric_columns].corr()["is_bad"].fillna(0).sort_values(ascending=False)

    # Convert correlation values to JSON-compliant data
    correlation_data = correlation.replace([float("inf"), float("-inf")], 0).to_dict()

    # Prepare most and least correlated factors
    most_correlated = {k: v for k, v in sorted(correlation_data.items(), key=lambda item: -item[1])[:5]}
    least_correlated = {k: v for k, v in sorted(correlation_data.items(), key=lambda item: item[1])[:5]}

    # Visualization: Create a bar chart for the top 10 correlated factors
    plt.figure(figsize=(12, 6))
    correlation[:10].plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Top 10 Factors Correlated with Defaults")
    plt.xlabel("Factors")
    plt.ylabel("Correlation Coefficient")
    plt.tight_layout()

    # Save to base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close()  # Free up memory

    # Generate a summary using ChatGPT
    statistics = {
        "most_correlated": most_correlated,
        "least_correlated": least_correlated,
    }

    # Format the statistics for better readability
    most_correlated_list = "\n".join([f"- {k}: {v:.2f}" for k, v in most_correlated.items()])
    least_correlated_list = "\n".join([f"- {k}: {v:.2f}" for k, v in least_correlated.items()])

    # Update the prompt for clarity
    prompt = (
        f"Based on the following correlations between loan attributes and defaults (is_bad=1):\n\n"
        f"Most Correlated Factors:\n{most_correlated_list}\n\n"
        f"Least Correlated Factors:\n{least_correlated_list}\n\n"
        f"Analyze and identify the factors contributing to high-default loans and provide insights on how these factors "
        f"could be used to refine risk assessment models. Include actionable recommendations for improving creditworthiness evaluation."
    )

    try:
        summary = await generate_summary(statistics, prompt)
    except ValueError as e:
        summary = f"Error generating summary: {str(e)}"

    return {
        "correlation_with_defaults": correlation_data,
        "most_correlated": most_correlated,
        "least_correlated": least_correlated,
        "summary": summary,
        "image": f"data:image/png;base64,{encoded_image}",
    }


async def temporal_default_trends():
    """Analyze temporal trends in loan defaults."""
    data = await get_data(TABLE_NAME)
    df = pd.DataFrame(data)

    if "earliest_cr_line" not in df or "is_bad" not in df:
        raise ValueError("Columns 'earliest_cr_line' or 'is_bad' are missing in the dataset.")

    # Ensure consistent date parsing
    try:
        df["earliest_cr_line"] = pd.to_datetime(df["earliest_cr_line"], format="%m/%d/%Y", errors="coerce")
    except ValueError:
        df["earliest_cr_line"] = pd.to_datetime(df["earliest_cr_line"], errors="coerce")

    # Extract the year from 'earliest_cr_line'
    df["issue_year"] = df["earliest_cr_line"].dt.year

    # Filter rows with valid years
    df = df[df["issue_year"].notnull()]

    # Group by year and calculate default counts
    yearly_defaults = df[df["is_bad"] == 1].groupby("issue_year").size()

    # Visualization
    plt.figure(figsize=(10, 6))
    yearly_defaults.plot(kind="line", marker="o", color="blue")
    plt.title("Yearly Default Trends")
    plt.xlabel("Year")
    plt.ylabel("Number of Defaults")
    plt.tight_layout()

    # Save to base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close()  # Close the plot to free memory

    # Generate a summary using ChatGPT
    statistics = {
        "yearly_defaults": yearly_defaults.to_dict()
    }

    # Prepare the prompt for ChatGPT
    prompt = (
        f"The dataset contains yearly trends in loan defaults based on the column 'earliest_cr_line'.\n\n"
        f"Yearly Default Counts:\n{yearly_defaults.to_string()}\n\n"
        f"Analyze the trends and provide insights, including:\n"
        f"1. Identification of significant increases or decreases in defaults over the years.\n"
        f"2. Discussion of possible external factors or events (e.g., economic downturns) influencing the trends.\n"
        f"3. Propose one additional analysis or hypothesis related to the dataset, such as exploring correlations with external datasets "
        f"(e.g., unemployment rates) or identifying underserved user segments.\n"
        f"4. Justify why this additional analysis is important and outline a preliminary exploration or plan."
    )

    try:
        summary = await generate_summary(statistics, prompt)
    except ValueError as e:
        summary = f"Error generating summary: {str(e)}"

    return {
        "image": f"data:image/png;base64,{encoded_image}",
        "summary": summary,
    }

async def generate_final_report(
    loan_distribution, grade_defaults, state_defaults, risk_factors, temporal_trends
):
    """Generate a single analysis report with a final summary and one visualization."""
    try:
        # Combine key findings for ChatGPT prompt
        findings = (
            f"Loan Distribution Summary: {loan_distribution['summary']}\n\n"
            f"Grade Defaults Summary: {grade_defaults['summary']}\n\n"
            f"State Defaults Summary: {state_defaults['summary']}\n\n"
            f"Risk Factors Summary: {risk_factors['summary']}\n\n"
            f"Temporal Trends Summary: {temporal_trends['summary']}\n\n"
        )

        # Create a single visualization summarizing key findings
        # Example: Comparing most significant risk factors
        df_risk_factors = pd.DataFrame(
            risk_factors["most_correlated"].items(), columns=["Factor", "Correlation"]
        )
        plt.figure(figsize=(10, 6))
        plt.barh(
            df_risk_factors["Factor"],
            df_risk_factors["Correlation"],
            color="skyblue",
        )
        plt.title("Top Risk Factors Associated with Loan Defaults")
        plt.xlabel("Correlation with Defaults")
        plt.ylabel("Risk Factor")
        plt.tight_layout()

        # Save the visualization to a base64 image
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()
        plt.close()  # Free memory

        # Generate final summary using ChatGPT
        prompt = (
            f"Provide a concise analysis report based on the following findings:\n\n"
            f"{findings}\n\n"
            f"Summarize the key insights and provide actionable recommendations. "
            f"Keep the summary concise and easy to understand."
        )
        final_summary = await generate_summary(findings, prompt)

        return {
            "summary": final_summary,
            "image": f"data:image/png;base64,{encoded_image}",
        }

    except Exception as e:
        return {"error": f"Failed to generate report: {str(e)}"}
