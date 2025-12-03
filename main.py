from fastapi import FastAPI ,Path , HTTPException , Query 
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal, Optional

app = FastAPI()

#Building Pydantic model for Data Validation
class Patient(BaseModel):

    id : Annotated[str , Field(...,description="ID of the patient",examples=['P001'])]
    name : Annotated[str , Field(...,description="Name of the Patient")]
    city : Annotated[str , Field(...,description="City of the patient")]
    age : Annotated[int , Field(...,description="Age of the person", gt=0 , lt=120)]
    gender : Annotated[Literal['male','female','other'], Field(...,description="Gender of the person")]
    height : Annotated[float , Field(...,description="Height of the person", gt=0)]
    weight : Annotated[float , Field(...,description="Weight of the person",gt = 0)]


    @computed_field
    @property
    def bmi(self)->float:

        bmi = self.weight / (self.height**2) 

        return bmi 
    
    @computed_field
    @property
    def verdict(self)->str:

        if self.bmi < 18.5:
            return "Underweight"
    
        elif self.bmi < 25:
            return "Normal"
        
        elif self.bmi < 30:
            return "Overweight"
        
        else:   
            return "Obese"

# Pydantic Model for Updating Patient (all fields optional)

class Patient_update(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]



# === Helper Functions === 

def load_file():

    with open("patients.json", "r") as f:
        data = json.load(f)

    return data


def save_data(data):

    with open("patients.json", "w") as f:
        json.dump(data, f , indent=2)

    
# === API Endpoints ===

@app.get("/")
def hello():

    return {'message':"API for Patient Management System"}

@app.get("/about")
def information():

    return {'information': "A Fully functional API for Patients Record System"}

@app.get("/view")
def view_patient():

    data = load_file()

    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient in DB", example='P001')):

    data = load_file()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404 , detail="Patient Data Not Found")

@app.get("/sort")
def sort_patient(sort_by : str = Query(...,description="Sort patient by height, weight and bmi"), order : str = Query('asc',description="sort in asc or desc order")):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field selected from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400 , detail=f"Invalid order selected between asc and desc")
    
    data = load_file()

    sort_order = True if order== 'desc' else False 

    sorted_data = sorted(data.values(), key= lambda x : x.get(sort_by,0),reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient : Patient):

    data = load_file()

    # Check whether the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400 , detail="Patient already exists")
    
    # Adding the patient 
    data[patient.id] = patient.model_dump(exclude=["id"])


    save_data(data)

    return JSONResponse(status_code=201 , content={'message' : 'Patient created Successfully'})


@app.put("/update/{patient_id}")
def update_patient(patient_id : str , patient_update : Patient_update):

   
    data = load_file() 

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient not found")


    existing_patient_info = data[patient_id]

    # Get only the fields that were provided in the request
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    # Update the existing patient with new values
    for key, value in updated_patient_info.items():

        existing_patient_info[key] = value 

    # Recalculate BMI and verdict using Patient model's computed fields
    # We need to add 'id' temporarily as Patient model requires it
    existing_patient_info['id']  = patient_id

    patient_pydantic_object = Patient(**existing_patient_info)


     # Convert back to dict without id and save
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')

    # Add the dict to data

    data[patient_id] = existing_patient_info

    # save data

    save_data(data)

    return JSONResponse(status_code=201 , content={'message': 'patient updated'})


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):

    # load data

    data = load_file()

    if patient_id not in data:
        raise HTTPException(status_code=404 ,detail="Patient data not found")

    del data[patient_id] 

    # save data

    save_data(data)

    return JSONResponse(status_code=200 , content={'message': 'patient deleted'})






    
                                      


