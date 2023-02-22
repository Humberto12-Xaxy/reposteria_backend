from fastapi import APIRouter
from fastapi.responses import JSONResponse

# sqlalchemy
from sqlalchemy import select
from config.db import session

# models
from models.category import category

# schemas
from schemas.Category import Category

router = APIRouter(
    prefix= '/category',
    tags= ['category'],
    responses= {404: {'description' : 'Not found'}}
)

# This function will show all category
@router.get('/')
async def get_category():
    all_category = session.execute(category.select()).fetchall()
    list_categories = [{'id' : category[0], 'name' : category[1] } for category in all_category]

    return JSONResponse(content= {'categories' : list_categories , 'length' : len(list_categories)})

# This function add a category to database
@router.post('/addCategory')
async def add_category(category_to_add:Category):

    try:
        new_category = {
            'name' : category_to_add.name
        }

        categories = session.execute(select(category).where(category.c.name == category_to_add.name)).first()

        if not categories:
            session.execute(category.insert(), new_category)
           
            session.commit()
            return JSONResponse(content= {'Success' : 'Category creacted'})

        else:
            return JSONResponse(content= {'message' : 'Existing categories'})

    except Exception as e: 
        return JSONResponse(content= {'Error' : f'{str(e)}'})

# This function delete one category with all desserts
# But this is a test
@router.delete('/deleteCategory/{id_categoty}')
async def delete_category(id_category:int):
    try:
        session.execute(category.delete().where(category.c.id == id_category))        
        session.commit()

        return JSONResponse(content= {'Success' : 'Category deleted'})

    except Exception as e:
        return JSONResponse(content= {'Error' : f'{str(e)}'})

# This function update the name of category
@router.put('/updateCategory/{id_category}')
async def update_category(id_category: int, category_to_update: Category):
    try:
        category_found = session.execute(category.select().where(category.c.id == id_category)).first()
        
        if category_found:
            session.execute(category.update().where(category.c.id == id_category).values(name= category_to_update.name))
            session.commit()
            return JSONResponse(content= {'Success' : 'Category updated'})
        
        else:
            return JSONResponse(content= {'message' : 'Category not found'})
            
    except Exception as e:
        return JSONResponse(content= {'Error' : f'{str(e)}'})

