import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from . import models
from .database import engine


from .routers import post, user, auth,vote


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

'''original_openapi = app.openapi

def custom_get_openapi():
    # Get the default OpenAPI schema
    openapi_schema = original_openapi()

    # Add the Bearer Authentication schema to the securitySchemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",  # Optional, but you can specify "JWT"
            "description": "Enter JWT Bearer token **_only_**",
        }
    }
    # Add the security requirement to all endpoints if needed
    #openapi_schema["security"] = [{"bearerAuth": []}]  # Applies globally

    return openapi_schema

app.openapi = custom_get_openapi
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# my_posts = []


# path operation
@app.get("/")
def start():
    return {"message": "Helloworld"}

