from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routes.chat import router as chat_router
from routes.conversations import router as convo_router
from routes.users import router as user_router
from routes.survey import router as survey_router

app = FastAPI(title="WritePal-Edu API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(convo_router)
app.include_router(user_router)
app.include_router(survey_router)

Base.metadata.create_all(bind=engine)