from fastapi import FastAPI
from routes import dessert
from routes import category
from routes import ingredient

app = FastAPI()

app.include_router(dessert.router)
app.include_router(category.router)
app.include_router(ingredient.router)

@app.get('/')
async def root():
    return {'message' : 'Hello cake shop'}