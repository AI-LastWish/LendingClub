import re
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from app.services.supabase_client import get_data
from app.utils.data_normalization import normalize_column, normalize_term, normalize_emp_length

# Set the matplotlib backend to a non-GUI backend
matplotlib.use("Agg")  # This ensures plots are not rendered visually

async def analyze_loan_amount_distribution():
    """Analyze and visualize the distribution of loan amounts."""
    data = await get_data("lending_club_loans")
    df = pd.DataFrame(data)
    
    if "loan_amnt" not in df:
        raise ValueError("Column 'loan_amnt' is missing in the dataset.")
    
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
    
    return {"image": f"data:image/png;base64,{encoded_image}"}

async def grade_vs_defaults():
    """Identify which loan grade is most frequently associated with defaults."""
    data = await get_data("lending_club_loans")
    df = pd.DataFrame(data)

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

    # Save to base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close()  # Close the plot to free memory

    return {
        "image": f"data:image/png;base64,{encoded_image}",
        "table": grade_defaults.to_dict(),
    }

async def state_wise_defaults():
    """Evaluate state-wise loan distributions and default rates."""
    data = await get_data("lending_club_loans")
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

    return {
        "image": f"data:image/png;base64,{encoded_image}",
        "highest_default_rate": highest_default_rate.to_dict(),
        "lowest_default_rate": lowest_default_rate.to_dict(),
    }

async def risk_factors_analysis():
    """Analyze factors contributing to high-default loans."""
    # Fetch data from Supabase
    data = await get_data("lending_club_loans")
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
    correlation = correlation.replace([float("inf"), float("-inf")], 0).to_dict()

    return {
        "correlation_with_defaults": correlation,
        "most_correlated": {k: v for k, v in sorted(correlation.items(), key=lambda item: -item[1])[:5]},
        "least_correlated": {k: v for k, v in sorted(correlation.items(), key=lambda item: item[1])[:5]},
    }


async def temporal_default_trends():
    """Analyze temporal trends in loan defaults."""
    data = await get_data("lending_club_loans")
    df = pd.DataFrame(data)

    if "earliest_cr_line" not in df or "is_bad" not in df:
        raise ValueError("Columns 'earliest_cr_line' or 'is_bad' are missing in the dataset.")

    # Extract year from 'earliest_cr_line'
    df["issue_year"] = pd.to_datetime(df["earliest_cr_line"], errors="coerce").dt.year
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

    return {"image": f"data:image/png;base64,{encoded_image}"}
