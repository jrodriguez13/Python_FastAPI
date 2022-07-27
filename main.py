#--------------------------------------------------------------#
#  Primera prueba de uvicorn                                   #
# - para ejecutar, escribir en terminal uvicorn main:app       #
# - para cambiar el puerto, agregar --port 5000                #
# - para que tome los cambios en el código, agregar --reload   #
#--------------------------------------------------------------#

# Librerías a importar}
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# cliente HTTP
# FastAPI - framework para construir APIs en Python
# Developer, clase custom que importa los modelos de datos
# JSONResponse y jsonable_encoder para parsear las respuestas del servidor
# motor_asyncio para codificar instrucciones asincronas
# ObjectId para conectar con MongoDB

from http import client
from fastapi import FastAPI
from models.Developer import Developer
from fastapi.responses import JSONResponse
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

# Objeto del tipo FastAPI 
app = FastAPI()

# Función para conectar a la BBDD
async def connection():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://127.0.0.1:27017')
    db = client['mydb']
    return db

# Método GET

@app.get('/developers')
async def get_developers():
    try:
        db = await connection()
        developers = await db.developers.find().to_list(1000)
        for developer in developers: developer['_id'] = str(developer['_id'])
        return JSONResponse(status_code=200, content= {"data" : developers})
    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content = {"message" : "Ha ocurrido un error"})


# Método GET por ID

@app.get('/developers/{id}')
async def get_developers(id: str):
    try:
        db = await connection()
        developer = await db.developers.find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(status_code=400, content={'message':'No encontrado'})
        developer['_id'] = str(developer['_id'])
        return JSONResponse(status_code=200, content={'data':developer})
    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={'message': 'Ha ocurrido un error'})

# Método GET devolviendo sólo skills

@app.get('/developers/{id}/skills')
async def get_developers(id: str):
    try:
        db = await connection()
        developer = await db.developers.find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(status_code=400, content={'message':'No encontrado'})
        developer['_id'] = str(developer['_id'])
        return JSONResponse(status_code=200, content={'data':developer['skills']})
    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={'message': 'Ha ocurrido un error'})

# Método GET devolviendo sólo experience

@app.get('/developers/{id}/experience')
async def get_developers(id: str):
    try:
        db = await connection()
        developer = await db.developers.find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(status_code=400, content={'message':'No encontrado'})
        developer['_id'] = str(developer['_id'])
        return JSONResponse(status_code=200, content={'data':developer['experience']})
    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={'message': 'Ha ocurrido un error'})

# Método GET devolviendo sólo languages

@app.get('/developers/{id}/languages')
async def get_developers(id: str):
    try:
        db = await connection()
        developer = await db.developers.find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(status_code=400, content={'message':'No encontrado'})
        developer['_id'] = str(developer['_id'])
        return JSONResponse(status_code=200, content={'data':developer['languages']})
    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={'message': 'Ha ocurrido un error'})

# Método POST para registrar un nuevo Developer

@app.post('/developers')
async def create_developer(developer: Developer):
    try:
        db = await connection()
        await db.developers.insert_one(jsonable_encoder(developer))
        return JSONResponse(status_code=201, content={'message': "Desarrollador registrado"})
    except:
        return JSONResponse(status_code=500, content={'message': "Ha ocurrido un error"})

# Método PUT para actualizar un Developer

@app.put('/developers/{id}')
async def update_developer(data: Developer, id: str):
    try:
        db = await connection()
        developer = await db.developers.find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(status_code=400, content={'message':'No encontrado'})
        await db.developers.update_one({'_id': ObjectId(id)}, {'$set': jsonable_encoder(data)})
        return JSONResponse(status_code=201, content={'message': "Desarrollador modificado"})
    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={'message': "Ha ocurrido un error"})

# Método DELETE para eliminar un Developer por ID

@app.delete('/developers/{id}')
async def delete_developer(id: str):
    try:
        db = await connection()
        developer = await db.developers.find_one({"_id": ObjectId(id)})
        if not developer:
            return JSONResponse(status_code=400, content={'message':'No encontrado'})
        await db.developers.delete_one({'_id': ObjectId(id)})
        return JSONResponse(status_code=200, content={'message': "Desarrollador eliminado"})
    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={'message': "Ha ocurrido un error"})