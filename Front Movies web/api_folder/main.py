from fastapi import FastAPI,Body,Request
from model_import import recommendations_tmdbIds 
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

#added by @Ayoub_Frihaoui, CORS so u can fetch data from the same machine 'localhost'
origins = [
    "*",
    "https://localhost:5173",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def get_recommendation(request:Request,movie : int= Body(...,embed=True) ):
    requestBody=await request.body()
    content= requestBody.decode()
    print(content)
    recommendations = recommendations_tmdbIds(movie)
    return {"recommendations":recommendations}



