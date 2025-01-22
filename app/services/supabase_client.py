import httpx
import logging

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

    # Clean rows to remove unsupported fields
    cleaned_rows = [clean_row(row, table_columns) for row in rows]

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
    """Retrieve the list of columns for a given table from Supabase."""
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{table_name}?select=*&limit=1",
            headers=headers,
        )
        if response.status_code != 200:
            logger.error(f"Failed to fetch table columns: {response.text}")
            raise ValueError("Failed to fetch table columns.")
        # Extract column names from the response keys
        return list(response.json()[0].keys()) if response.json() else []
    
def clean_row(row, table_columns):
    """Remove keys not in the Supabase table schema and rename keys if needed."""
    # Map 'desc' to 'description'
    key_map = {'desc': 'description'}
    cleaned_row = {}
    for key, value in row.items():
        # Rename or drop keys not in the table schema
        mapped_key = key_map.get(key, key)
        if mapped_key in table_columns:
            cleaned_row[mapped_key] = value
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
