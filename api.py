from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import analysis_func as af
import json

api = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/")
async def root():
    return {"messgae": "you've reached the math alliance data webpage"}

@api.get("/query")
async def query(degree: str, start_year: int, end_year: int, citizenship: str, cip: str, min_awards:int, uni_type:str, geo_region:str, obreg: str, states: str):
    print(degree, start_year, end_year, citizenship, cip, min_awards, uni_type, geo_region, obreg, states)
    data_out = af.history_best_unis_2019(af.setup(), method='percentage', min_awards=5e4)
    print(data_out)
    return {'data': data_out}

@api.get("/query/major_universities")
async def major_univeristies(year: int, min_awards: int):
    df = af.find_major_universities(af.setup(), year, min_awards=min_awards)
    print(df)
    return df.to_json()

@api.get("/query/top_10_urm")
async def top_10_urm(year: int, degree: str, method: str):
    return af.top_10_num_urm_students(af.setup(), year, degree, method)

@api.get("/query/urm_students_large_inst")
async def urm_students_large_inst(year: int, method: str, min_awards: int):
    return af.urm_students_large_inst(af.setup(), year, method, min_awards)
