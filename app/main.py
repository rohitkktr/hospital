from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import Base, engine
from routers.patients import router as patients_router
from routers.admissions import router as admissions_router
from routers.beds import router as beds_router
from routers.units import router as units_router
from routers.restriants import router as restraints_router
from routers.user import router as users_router

# -------------------- CREATE TABLES --------------------
Base.metadata.create_all(bind=engine)

# -------------------- INITIALIZE APP --------------------
app = FastAPI(
    title="Hospital Management API",
    description="API for managing patients, admissions, beds, units, restraints, and users",
    version="1.0.0"
)

# -------------------- CORS --------------------
origins = ["*"]  # allow all origins (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# -------------------- INCLUDE ROUTERS --------------------
app.include_router(patients_router)
app.include_router(admissions_router)
app.include_router(beds_router)
app.include_router(units_router)
app.include_router(restraints_router)
app.include_router(users_router)

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Hospital Management API!"}
