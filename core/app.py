from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title = "FastAPI JWT Authentication"
)

@app.get('/', response_class=PlainTextResponse)
async def root():
    return "Server is Running"
