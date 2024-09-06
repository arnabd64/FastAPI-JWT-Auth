from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import auth

app = FastAPI(
    title = "FastAPI JWT Authentication"
)

app.include_router(auth.router)

@app.get('/', response_class=PlainTextResponse)
async def root():
    return "Server is Running"
