from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import auth.routes

app = FastAPI(
    title = "FastAPI JWT Authentication"
)

app.include_router(auth.routes.router)

@app.get('/', response_class=PlainTextResponse)
async def root():
    return "Server is Running"
