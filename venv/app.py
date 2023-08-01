from fastapi import FastAPI, HTTPException
import httpx
from langchain import TextGenerator

app = FastAPI()

# Replace this with your actual OpenAI API key
YOUR_OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"


def generate_text_from_openai(prompt: str, max_tokens: int, temperature: float):
    api_endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Authorization": f"Bearer {YOUR_OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["text"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch data from OpenAI API.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.post("/competitor_research/")
async def competitor_research(task_input: str):
    generated_text = await generate_text_from_openai(task_input, max_tokens=1000, temperature=0.7)
    return {"result": generated_text}


@app.post("/generate_personalized_email/")
async def generate_personalized_email(recipient_name: str, email_subject: str, email_body: str):
    prompt = f"Dear {recipient_name},\n\n{email_body}\n\nSincerely,\nYour Name"
    generated_email = await generate_text_from_openai(prompt, max_tokens=1000, temperature=0.7)
    return {"email": generated_email}


@app.post("/generate_social_media_post/")
async def generate_social_media_post(platform: str, post_content: str):
    prompt = f"Platform: {platform}\n\n{post_content}"
    generated_post = await generate_text_from_openai(prompt, max_tokens=500, temperature=0.7)
    return {"post": generated_post}


@app.post("/generate_text_langchain/")
async def generate_text_langchain(prompt: str):
    # Use the Langchain library for text generation
    generator = TextGenerator()
    generated_text = generator.generate_text(prompt)
    return {"text": generated_text}
