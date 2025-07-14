

from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64


load_dotenv()
my_api_key = os.getenv("OPENAI_API_KEY")
print('My api key', my_api_key)


client = OpenAI(api_key = my_api_key)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins: restrict in production
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods
    allow_headers=["*"] # Allows all http headers
)

@app.post("/")
def ai_prompt(request: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": request.prompt
            }
        ]
    )

    gtp_response = completion.choices[0].message.content
    return ChatResponse(response = gtp_response)

@app.post("/uploadfile/")
async def create_upload_file(
    prompt: str = Form(...),
    file: UploadFile = File(None)
):
    base64_image = None
    completion = None
    if file:
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode("utf-8")

        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": prompt },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
        )
    else:
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    if (completion):
        gtp_response = completion.choices[0].message.content
        return ChatResponse(response=gtp_response)
    return {"message": "No response from OpenAI API."}
