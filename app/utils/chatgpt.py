import httpx
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def generate_summary(statistics, prompt):
    """Generate a summary using ChatGPT based on the provided statistics and prompt."""
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-3.5-turbo",  # Use the recommended model
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt.format(statistics=statistics)},
                    ],
                    "max_tokens": 150,
                },
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except httpx.HTTPStatusError as http_err:
            error_details = http_err.response.json()
            raise ValueError(
                f"HTTP error: {http_err.response.status_code}. Details: {error_details}"
            )
        except Exception as e:
            raise ValueError(f"Failed to generate summary: {str(e)}")
