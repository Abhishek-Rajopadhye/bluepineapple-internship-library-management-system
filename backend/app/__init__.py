from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import books, members, allocations, history

app = FastAPI(title="Library Management System")

origins = [
    "http://localhost",
    "http://localhost:5173"
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/books")
app.include_router(members.router, prefix="/members")
app.include_router(allocations.router, prefix="/allocations")
app.include_router(history.router, prefix="/history")