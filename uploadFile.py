from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO
import csv
import models
from database import SessionLocal, engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital CSV API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Generic CSV Upload ----------------
@app.post("/upload-csv/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    csv_str = content.decode("utf-8")
    reader = csv.DictReader(StringIO(csv_str))
    
    model_map = {
        "unit": models.Unit,
        "bed": models.Bed,
        "patient": models.Patient,
        "admission": models.Admission,
        "user": models.User,
    }

    model_class = model_map.get(table_name.lower())
    if not model_class:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    rows_added = 0
    for row in reader:
        obj = model_class(**row)
        db.add(obj)
        rows_added += 1

    db.commit()
    return {"message": f"{rows_added} rows added to {table_name}"}


# ---------------- Generic CSV Download ----------------
@app.get("/download-csv/{table_name}")
def download_csv(table_name: str, db: Session = Depends(get_db)):
    model_map = {
        "unit": models.Unit,
        "bed": models.Bed,
        "patient": models.Patient,
        "admission": models.Admission,
        "user": models.User,
    }

    model_class = model_map.get(table_name.lower())
    if not model_class:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    records = db.query(model_class).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No records found in {table_name}")
    
    # CSV in memory
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    
    # Write header dynamically from SQLAlchemy model
    header = [col.name for col in model_class.__table__.columns]
    writer.writerow(header)
    
    # Write data rows
    for record in records:
        row = [getattr(record, col) for col in header]
        writer.writerow(row)
    
    csv_file.seek(0)
    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}
    )
