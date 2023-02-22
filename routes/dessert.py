from fastapi import APIRouter
from fastapi.responses import JSONResponse

# schemas
from schemas.Dessert import Dessert, DessertGeneral

# models
from models.dessert import dessert
from models.ingredients import ingredients
from models.ingredients_dessert import ingredients_dessert

# db
from config.db import session

router = APIRouter(
        prefix= '/dessert',
        tags= ['dessert'],
        responses= {404 : {'description' : 'Not found'}}
    )

# this function will show all desserts of one user 
# but i will show all desserts for now
@router.get('/')
async def get_all_desserts():
    try:
        desserts = session.execute(dessert.select()).fetchall()
        list_desserts = [{'id' : dessert[0], 'name' : dessert[1], 'id_category' : dessert[2]} for dessert in desserts]
        if desserts:
            return JSONResponse(content= {'Desserts' : list_desserts, 'lenght' : len(desserts)})
    except Exception as e:
        return JSONResponse(content= {'Error' : str(e)})

# This function will show just one dessert
@router.get('/getDessert/{id}')
async def get_desert(id:int):
    try:
        list_ingredints = []
        dessert_found =  session.execute(dessert.select().where(dessert.c.id == id)).first()

        if dessert_found:
            ingredients_dessert_found = session.execute(ingredients_dessert.select().where(ingredients_dessert.c.id_dessert == id)).fetchall()
            
            for ingredient_dessert in ingredients_dessert_found:
                ingredient_found = session.execute(ingredients.select().where(ingredients.c.id == ingredient_dessert[1])).first()
                list_ingredints.append({'id' : ingredient_found[0], 'name' : ingredient_found[1], 'price' : ingredient_found[2]})
            
    
            dessert_to_show = {'id' : dessert_found[0], 'name' : dessert_found[1], 'ingredients' : list_ingredints, 'id_category' : dessert_found[2]}
            return JSONResponse(content= {'dessert' : dessert_to_show})

        else:
            return JSONResponse(content= {'message' : 'Dessert not found'})

    except Exception as e:
        return JSONResponse(content= {'Error' : str(e)})

@router.post('/createDessert')
async def create_dessert(dessert_to_add:DessertGeneral):
    
    try:
        dessert_add = Dessert(name = dessert_to_add.name, id_category= dessert_to_add.id_category)
        ingredients_add = dessert_to_add.ingredients
        portion = dessert_to_add.portion

        exist_dessert= session.execute(dessert.select().where(dessert.c.name == dessert_add.name)).first()

        if not exist_dessert:
            session.execute(dessert.insert(), dessert_add.dict())
            session.commit()

            dessert_found = session.execute(dessert.select().where(dessert.c.name == dessert_add.name)).first()
            id_dessert = dessert_found[0]

            for ingredient_to_add in ingredients_add:
                ingredient_found = session.execute(ingredients.select().where(ingredients.c.name == ingredient_to_add.name)).first()
                
                if not ingredient_found:
                    session.execute(ingredients.insert(), {'name' : ingredient_to_add.name, 'price' : ingredient_to_add.price})
                    session.commit()
            
            for ingredient_to_add in ingredients_add:
                ingredient_found = session.execute(ingredients.select().where(ingredients.c.name == ingredient_to_add.name)).first()

                session.execute(ingredients_dessert.insert(), {'id_dessert': id_dessert, 'id_ingredients': ingredient_found[0], 'portion': portion})
                session.commit()

            return JSONResponse(content= {'success' : 'Dessert Created'})
        else:
            return JSONResponse(content= {'message' : 'Existing Dessert'})

    except Exception as e:
        return JSONResponse(content= {'Error' : str(e)})
    

@router.put('/editDessert/{id}')
async def update_dessert(id:int ,dessert_to_update:Dessert):
    try:
        dessert_found = session.execute(dessert.select().where(dessert.c.id == id)).first()
        if dessert_found:
            session.execute(dessert.update().where(dessert.c.id == id), dessert_to_update.dict())
            session.commit()
            return JSONResponse(content={'Success' : 'Dessert updated'})
        else:
            return JSONResponse(content= {'message' : 'Dessert not found'})
    except Exception as e:
        return JSONResponse(content= {'Error' : str(e)})

@router.delete('/deleteDessert')
async def delete_dessert(id:int):
    try:
        
        if session.execute(dessert.select().where(dessert.c.id == id)).first():            

            ingredients_dessert_found = session.execute(ingredients_dessert.select().where(ingredients_dessert.c.id_dessert == id)).fetchall()
            for ingredient_dessert in ingredients_dessert_found:
                session.execute(ingredients_dessert.delete().where(ingredients_dessert.c.id_dessert == ingredient_dessert[0]))

            session.execute(dessert.delete().where(dessert.c.id == id))
            session.commit()

            return JSONResponse(content= {'Success' : 'Dessert deleted'})
        else: 
            return JSONResponse(content= {'Message' : 'Dessert not found'})

    except Exception as e:
        return JSONResponse(content= {'Error': str(e)})



