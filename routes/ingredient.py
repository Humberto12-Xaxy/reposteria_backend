from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Schemas
from schemas.Ingredient import Ingredient

# models
from models.ingredients import ingredients

# db
from config.db import session

router = APIRouter(
    prefix= '/ingredients',
    tags= ['ingredients'],
    responses= {404 : {'description' : 'Not found'}}
)

@router.get('/')
async def get_ingredients():
    try:
        ingredients_found = session.execute(ingredients.select().order_by(ingredients.c.id)).fetchall()
        if ingredients_found:
            list_ingredients = [{'id': ingredient[0], 'name' : ingredient[1], 'price' : ingredient[2]} for ingredient in ingredients_found]
            return JSONResponse(content= {'Success' : list_ingredients})
        
        else:
            return JSONResponse(content= {'Message' : 'Ingredients not found'})
    except Exception as e:
        return JSONResponse(content= {'Error' : str(e)})

@router.put('/editIngredient/{id}')
async def update_ingredient(id: int, ingredient_to_update: Ingredient):
    try:
        ingredient_found = session.execute(ingredients.select().where(ingredients.c.id == id)).first()
        
        if ingredient_found:
            session.execute(ingredients.update().where(ingredients.c.id == id), ingredient_to_update.dict())
            session.commit()
            return JSONResponse(content= {'Success': 'Ingredient updated'})
        else:
            return JSONResponse(content= {'Message' : 'Ingredient not found'}) 
    except Exception as e:
        return JSONResponse(content= {'Error' : str(e)})


@router.delete('/deleteIngredient/{id}')
async def delete_ingredient(id:int):
    try:
        ingredient_to_delete = session.execute(ingredients.select().where(ingredients.c.id == id)).first()
        if ingredient_to_delete:
            session.execute(ingredients.delete().where(ingredients.c.id == id))
            session.commit()
            return JSONResponse(content= {'Success' : 'Ingredient Deleted'})

        else:
            return JSONResponse(content= {'message' : 'Ingredient not found'})
    except Exception as e :
        return JSONResponse(content= {'Error' : str(e)})