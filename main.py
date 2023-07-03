from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.router.base import api_router
import uvicorn

#Base.metadata.create_all(bind=engine)

app = FastAPI(
    debug=True,
    title="Safesight",
    description="App Reconocimiento Armas",
    version="0.0.1",
    openapi_url="/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs")

app.include_router(api_router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8200)
