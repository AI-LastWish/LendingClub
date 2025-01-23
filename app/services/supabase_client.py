import httpx
import logging
import pandas as pd  # Ensure pandas is imported

from app.config import SUPABASE_URL, SUPABASE_API_KEY

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
}

# Debugging: Print Supabase variables
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_API_KEY: {SUPABASE_API_KEY}")

async def insert_data(table_name, rows):
    """Insert data into a Supabase table."""
    if not SUPABASE_URL or not SUPABASE_API_KEY:
        logger.error("Supabase URL or API key is missing.")
        raise ValueError("Supabase URL or API key is missing in environment variables.")

    # Fetch table columns from Supabase
    table_columns = await get_table_columns(table_name)
    logger.info(f"Supabase table columns: {table_columns}")
    if not table_columns:
        raise ValueError(f"Could not fetch column names for table '{table_name}'. Ensure the table exists.")

    # Clean rows to remove unsupported fields
    cleaned_rows = [clean_row(row, table_columns) for row in rows]
    logger.info(f"Cleaned rows: {cleaned_rows[:5]}")  # Log the first 5 cleaned rows

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/{table_name}",
            headers=headers,
            json=cleaned_rows,
        )
        logger.info(f"Supabase Response: {response.status_code}, {response.text}")
        if response.status_code != 201:
            logger.error(f"Supabase Error Response: {response.text}")
            response.raise_for_status()

async def get_table_columns(table_name):
    """Fetch table columns using the OpenAPI schema from Supabase REST server."""
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SUPABASE_URL}/rest/v1/", headers=headers)

        if response.status_code == 200:
            try:
                openapi_data = response.json()
                definitions = openapi_data.get("definitions", {})
                if table_name in definitions:
                    # Extract column names from the table definition
                    table_properties = definitions[table_name].get("properties", {})
                    return list(table_properties.keys())
                else:
                    logger.error(f"Table '{table_name}' not found in OpenAPI schema definitions.")
                    return []
            except Exception as e:
                logger.error(f"Error parsing OpenAPI response: {e}")
                return []
        else:
            logger.error(f"Failed to fetch OpenAPI schema: {response.status_code}, {response.text}")
            return []
    
def clean_row(row, table_columns):
    """Remove keys not in the Supabase table schema."""
    cleaned_row = {}
    for key, value in row.items():
        # Only include keys that exist in the table schema
        if key in table_columns:
            # Ensure value compatibility (e.g., replace NaN or None with default)
            cleaned_row[key] = value if pd.notnull(value) else None
    return cleaned_row


async def get_data(table: str, filters: str = ""):
    """Get data from a Supabase table with optional filters."""
    async with httpx.AsyncClient() as client:
        url = f"{SUPABASE_URL}/rest/v1/{table}?{filters}"
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

async def update_data(table: str, filters: str, data: dict):
    """Update data in a Supabase table."""
    async with httpx.AsyncClient() as client:
        url = f"{SUPABASE_URL}/rest/v1/{table}?{filters}"
        response = await client.patch(url, json=data, headers=HEADERS)
        response.raise_for_status()
        return response.json()

async def delete_data(table: str, filters: str):
    """Delete data from a Supabase table."""
    async with httpx.AsyncClient() as client:
        url = f"{SUPABASE_URL}/rest/v1/{table}?{filters}"
        response = await client.delete(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
