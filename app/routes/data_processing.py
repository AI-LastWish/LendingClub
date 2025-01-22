from fastapi import APIRouter, HTTPException, UploadFile
from app.services.supabase_client import insert_data
import pandas as pd
from io import StringIO
import simplejson as json  # Use simplejson for better NaN handling
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

TABLE_NAME = "lending_club_loans"

TABLE_SCHEMA = {
    "loan_amnt": float,
    "funded_amnt": float,
    "term": str,
    "int_rate": float,
    "installment": float,
    "grade": str,
    "sub_grade": str,
    "emp_title": str,
    "emp_length": str,
    "home_ownership": str,
    "annual_inc": float,
    "verification_status": str,
    "pymnt_plan": str,
    "url": str,
    "description": str,
    "purpose": str,
    "title": str,
    "zip_code": str,
    "addr_state": str,
    "dti": float,
    "delinq_2yrs": int,
    "earliest_cr_line": str,
    "inq_last_6mths": int,
    "mths_since_last_delinq": int,
    "mths_since_last_record": int,
    "open_acc": int,
    "pub_rec": int,
    "revol_bal": float,
    "revol_util": float,
    "total_acc": int,
    "initial_list_status": str,
    "mths_since_last_major_derog": int,
    "policy_code": int,
    "is_bad": bool,
}

def preprocess_data(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """Preprocess the DataFrame to match the table schema."""
    for column, dtype in schema.items():
        if column in df.columns:
            try:
                if column == "int_rate":  # Handle percentage strings
                    df[column] = df[column].str.rstrip('%').astype(float) / 100
                elif dtype == bool:
                    df[column] = df[column].apply(lambda x: bool(int(x)) if pd.notnull(x) else False)
                elif dtype == int:
                    df[column] = df[column].fillna(0).astype(int)
                elif dtype == float:
                    df[column] = df[column].fillna(0.0).astype(float)
                else:
                    df[column] = df[column].fillna('').astype(str)
            except Exception as e:
                logger.error(f"Error converting column '{column}' to {dtype}: {e}")
                raise ValueError(f"Column '{column}' contains invalid data for type {dtype}.")
        else:
            logger.warning(f"Column '{column}' is missing. Filling with default values.")
            if dtype == bool:
                df[column] = False
            elif dtype == int:
                df[column] = 0
            elif dtype == float:
                df[column] = 0.0
            else:
                df[column] = ''
    return df

@router.post("/upload")
async def upload_file(file: UploadFile):
    """Upload CSV file and insert data into Supabase."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        logger.info("Started processing file upload...")

        # Read the CSV file into a DataFrame
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode('utf-8')))
        logger.info(f"DataFrame loaded with {len(df)} rows and {len(df.columns)} columns.")

        # Preprocess the DataFrame
        df = preprocess_data(df, TABLE_SCHEMA)
        logger.info("DataFrame preprocessed successfully.")

        # Convert DataFrame to JSON
        rows = json.loads(df.to_json(orient="records", default_handler=str))
        logger.info(f"Converted DataFrame to {len(rows)} JSON rows.")

        # Insert data into Supabase in batches
        BATCH_SIZE = 100
        for i in range(0, len(rows), BATCH_SIZE):
            batch = rows[i:i + BATCH_SIZE]
            logger.info(f"Inserting batch {i // BATCH_SIZE + 1} with {len(batch)} records.")
            await insert_data(TABLE_NAME, batch)

        logger.info("Data uploaded successfully.")
        return {"message": "Data uploaded successfully"}
    except Exception as e:
        logger.error(f"Failed to upload data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload data: {str(e)}")



