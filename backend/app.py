# from fastapi import FastAPI
# from backend.models import ChatRequest, ChatResponse
# from backend.chatbot import chatbot_reply


# app = FastAPI(title="Vormirex Chatbot")

# @app.post("/chat", response_model=ChatResponse)
# def chat(req: ChatRequest):
#     reply = chatbot_reply(req.message)
#     return ChatResponse(reply=reply)

# @app.get("/")
# def home():
#     return {"status": "Vormirex chatbot is running"}

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from backend.chatbot import chatbot_reply
# import uuid

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str
#     user_id: str | None = None   # ✅ optional

# class ChatResponse(BaseModel):
#     reply: str
#     buttons: list | None = None

# @app.get("/")
# def root():
#     return {"status": "Vormirex backend running"}

# @app.post("/chat", response_model=ChatResponse)
# def chat(req: ChatRequest):
#     user_id = req.user_id or str(uuid.uuid4())  # ✅ auto-generate
#     response = chatbot_reply(
#         user_id=user_id,
#         user_message=req.message
#     )
#     return response


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from backend.chatbot import chatbot_reply
# import uuid

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str
#     user_id: str | None = None

# class ChatResponse(BaseModel):
#     reply: str
#     buttons: list | None = None


# # ✅ API ROUTES FIRST
# @app.post("/chat", response_model=ChatResponse)
# def chat(req: ChatRequest):
#     user_id = req.user_id or str(uuid.uuid4())
#     return chatbot_reply(
#         user_id=user_id,
#         user_message=req.message
#     )


# @app.get("/health")
# def health():
#     return {"status": "Vormirex backend running"}


# # ✅ STATIC FILES LAST (IMPORTANT)
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")



# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from backend.chatbot import chatbot_reply
# import uuid

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str
#     user_id: str | None = None

# @app.post("/chat")
# def chat(req: ChatRequest):
#     return chatbot_reply(req.user_id or str(uuid.uuid4()), req.message)

# # STATIC
# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from backend.chatbot import chatbot_reply
# import uuid

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str
#     user_id: str | None = None
#     language: str | None = "en"

# @app.post("/chat")
# def chat(req: ChatRequest):
#     return chatbot_reply(req.user_id or str(uuid.uuid4()), req.message, language=req.language)

# # STATIC FILES
# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from backend.chatbot import chatbot_reply
# import uuid

# app = FastAPI()

# # -------------------------
# # CORS Middleware
# # -------------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------------
# # Request Model
# # -------------------------
# class ChatRequest(BaseModel):
#     message: str
#     user_id: str | None = None
#     # language: str | None = "en"   # optional, only if you want future multi-language support

# # -------------------------
# # Chat Endpoint
# # -------------------------
# @app.post("/chat")
# def chat(req: ChatRequest):
#     # Generate user_id if not provided
#     user_id = req.user_id or str(uuid.uuid4())
#     # Call chatbot_reply (no language argument for now)
#     return chatbot_reply(user_id, req.message)

# # -------------------------
# # Static Files
# # -------------------------
# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.chatbot import chatbot_reply
from backend.google_sheets import save_lead
import uuid

app = FastAPI()

# -------------------------
# CORS Middleware
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Models
# -------------------------
class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None


class LeadRequest(BaseModel):
    name: str
    phone: str
    course: str
    source: str = "chatbot"


# -------------------------
# Chat Endpoint
# -------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    # Generate user_id if not provided
    user_id = req.user_id or str(uuid.uuid4())
    return chatbot_reply(user_id, req.message)


# -------------------------
# Save Lead Endpoint (Google Sheets)
# -------------------------
@app.post("/save-lead")
def save_lead_api(req: LeadRequest):
    save_lead(
        name=req.name,
        phone=req.phone,
        source=req.source,
        course=req.course
    )
    return {"status": "success", "message": "Lead saved successfully"}


# -------------------------
# Static Files
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
