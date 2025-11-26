from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import products, cart


def create_app() -> FastAPI:
    app = FastAPI(title="App", version="1.0.0")

    # Allow Next.js dev server on 3001 to call this API from the browser
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3001",
            "http://127.0.0.1:3001",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount our products API
    app.include_router(products.router)
    app.include_router(cart.router)

    @app.get("/health")
    def health():
        return {"ok": True}

    return app


app = create_app()
