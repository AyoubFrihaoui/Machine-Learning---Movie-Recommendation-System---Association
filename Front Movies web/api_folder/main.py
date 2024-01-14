from fastapi import FastAPI,Body,Request
from model_import import recommendations_tmdbIds 

app=FastAPI()


@app.post("/")
async def get_recommendation(request:Request,movie : int= Body(...,embed=True) ):
    requestBody=await request.body()
    content= requestBody.decode()
    print(content)
    recommendations = recommendations_tmdbIds(movie)
    return {"recommendations":recommendations}



