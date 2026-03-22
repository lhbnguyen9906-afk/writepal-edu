from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import chat, users, conversations

# 🔥 CREATE TABLE
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 ROUTES
app.include_router(chat.router)
app.include_router(users.router)
app.include_router(conversations.router)


# 🔥 HEALTH CHECK (khuyên thêm)
@app.get("/")
def root():
    return {"status": "WritePal-Edu backend running"}