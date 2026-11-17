from fastapi import FastAPI, Path, HTTPException, status, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI(
    title = "Patient Management System",
    version="1.0.1"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Model
class Patient(BaseModel):

    id : Annotated[str, Field(..., description='Id of the patient', examples=['P001'])]
    name : Annotated[str, Field(..., description='Name of the Patient')]
    city : Annotated[str, Field(..., description='City where the patient is living')]
    age : Annotated[int, Field(gt=0, lt=120)]
    gender : Annotated[Literal['Male', 'Female', 'Others'], Field(..., description="Gender of the patient")]
    height : Annotated[float, Field(..., gt=0, description='Height of the patient')]
    weight : Annotated[float, Field(..., description='weight of the patient')]

    # bmi calculator
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round((self.weight)/(self.height**2), 2)
        return bmi
    
    #verdict  
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'obese'


# Pydantic model for Patient updation
class PatientUpdate(BaseModel):

    name : Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt=0)]
    gender : Annotated[Optional[Literal['Male', 'Female', 'Others']], Field(default=None)]
    height : Annotated[Optional[float], Field(default=None, gt=0)]
    weight : Annotated[Optional[float], Field(default=None, gt=0)]
    

# Function for loading jason data
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# home page
@app.get("/")
def hello():
    return {"message" : "Patient Management System API"}

# about page
@app.get("/about")
def hello():
    return {"message" : "A fully functional API to manage your patient records."}

#view page
@app.get('/view')
def view():
    data = load_data()
    return data

# patientspage
@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description='ID of the patient in DB', example='P001')):
    # load all the functions:
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail='Patient data not found.')

# sort accordingly
@app.get('/sort')
def sort_patients(sort_by : str = Query(...,  description='Sort on the basis of height, weight, or bmi'), order : str = Query('asc', description='sort in ascending or descending order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail = f'invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail = 'invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by, 0), reverse = sort_order)

    return sorted_data


# endpoint to create new patient
@app.post('/create')
def create_patient(patient : Patient):

    # load existing data
    data = load_data()

    # check if the patient already exist
    if patient.id in data :
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # add new patient to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save in json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message' : 'Patient created successfully'})




# Update endpoint
@app.put('/edit/{patient_id}')
def update_patient(patient_id : str, patient_update : PatientUpdate):

    data = load_data()

    if patient_id not in data :
        raise HTTPException(status_code = 404, detail = 'patient not found')

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, val in updated_patient_info.items():
        existing_patient_info[key] = val

    existing_patient_info['id'] = patient_id
    patient_pydantic_model = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_model.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    # save data
    save_data(data)


    return JSONResponse(status_code=200, content = {'message' : 'Patient updated'})


# Delete Endpoint
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):

    data = load_data()

    if patient_id not in data :
        raise HTTPException(status_code = 404, detail = 'patient not found')

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message' : 'Patient Deleted'})





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)