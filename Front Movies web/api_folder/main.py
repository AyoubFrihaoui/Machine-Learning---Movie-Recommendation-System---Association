from fastapi import FastAPI,Body,Request
from model_import import recommendations_name 

app=FastAPI()


@app.post("/")
async def get_recommendation(request:Request,movie : str= Body(...,embed=True) ):
    requestBody=await request.body()
    content= requestBody.decode()
    print(content)
    recommendations = recommendations_name(movie)
    return {"recommendations":recommendations}



