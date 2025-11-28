from fastapi import FastAPI, Depends,Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import SessionLocal, engine, Base
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company Employee API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()

# Pydantic model for request
class EmpCreate(BaseModel):
    name: str
    role: str
    salary: int

# POST endpoint
@app.post("/employees")
def create_employee(emp: EmpCreate, db: Session = Depends(get_db)):
    new_emp = models.Emp(name=emp.name, role=emp.role, salary=emp.salary)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


@app.get("/employees")
def read_employees(db: Session = Depends(get_db)):
    return db.query(models.Emp).all()



class EmpDelete(BaseModel):
    emp_id: int
# @app.delete("/employees")
# def delete_employee(emp: EmpDelete, db: Session = Depends(get_db)):
#     emp_record = db.query(models.Emp).filter(models.Emp.id == emp.emp_id).first()
#     if not emp_record:
#         raise "Employee not found"
    
#     db.delete(emp_record)
#     db.commit()
#     return {"message": f"Employee with id {emp.emp_id} deleted successfully"}

@app.delete("/employees")
def delete_employee(emp_id: EmpDelete, db: Session = Depends(get_db)):
    emp = db.query(models.Emp.id).filter(models.Emp.id == emp_id).first()
    if emp:
        db.delete(emp)
        db.commit()
        return {"message": "Employee deleted successfully"}
    return {"message": "Employee not found"}

#filter employees by first character of name
class EmpFilter(BaseModel):
    first_char: str
@app.get("/employees/filter")
def filter_employees(emp_filter: EmpFilter, db: Session = Depends(get_db)):
    first_char = emp_filter.first_char
    results = db.query(models.Emp).filter(models.Emp.name.ilike(f"{first_char}%")).all()
    if not results:
        return "No employees found starting with '{first_char}'"
    return results

