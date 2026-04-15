from fastapi import FastAPI
from .database import Base, engine
from .routers import users, issues, comments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Move origins to a list for better management
origins = [
    "https://voice-safe.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500", # Live Server default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://.*\.vercel\.app", # Allow all Vercel subdomains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend is running", "database": "Connecting..."}

# Create tables if they don't exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating tables: {e}")

app.include_router(users.router)
app.include_router(issues.router)
app.include_router(comments.router)