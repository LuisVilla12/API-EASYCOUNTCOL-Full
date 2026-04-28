#Importa la clase FastAPI para crear la aplicación.
from fastapi import FastAPI, HTTPException,Form,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# Importa los modelos a utilizar
from models.User import usuario, registrar_usuario
from models.Login import LoginUsuario, login_usuario 
from models.Sample import RegistarMuestra 
from models.RecordCreate import RecordCreate
from models.Follow import Follow
from models.FollowCreate import FollowCreate
from fastapi.responses import FileResponse
import shutil
import os
from db import get_db


#Crea una instancia de la aplicación FastAPI.
app = FastAPI()
# ✅ Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Define una ruta raíz
@app.get("/")
def home():
    print("➡ Working directory (os.getcwd()):", os.getcwd())

    return {"mensaje": "Bienvenido a la API"}

#Ruta para el registro de un usuario
@app.post("/registrar-usuario")
def registrarUsuario(data: usuario):
    try:
        registrar_usuario(data)
        return {"mensaje": "Usuario registrado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Ruta para inicio de sesión
@app.post("/login")
def login(usuario: LoginUsuario):
    return login_usuario(usuario)

#Ruta para registro de una muestra
@app.post("/registrar-muestra-file")
async def registrar_muestra_file(
    sampleName: str = Form(...),
    idUser: int = Form(...),
    typeSample: str = Form(...),
    volumenSample: str = Form(...),
    factorSample: str = Form(...),
    medioSample: str = Form(...),
    sample_file: UploadFile = File(...)):
    try:
        return RegistarMuestra.save_with_file(
        sampleName=sampleName,
        idUser=idUser,
        typeSample=typeSample,
        volumenSample=volumenSample,
        factorSample=factorSample,
        medioSample=medioSample,
        sample_file=sample_file
    )
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

#Ruta para mostar la imagen procesada
@app.get("/imagen-procesada/{id_muestra}")
def get_processed_image(id_muestra: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = "SELECT sampleRoute FROM samples WHERE id = %s"
        cursor.execute(sql, (id_muestra,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")

        filename = result[0]
        processed_path = f"ia/resultados/clustering_img/{filename}"

        if not os.path.exists(processed_path):
            raise HTTPException(status_code=404, detail="Imagen procesada no encontrada")

        return FileResponse(processed_path, media_type="image/png")

    except Exception as e:
        print(f"ERROR AL CARGAR IMAGEN procesada: {e}") 
        raise HTTPException(status_code=400, detail=f"Error al cargar imagen procesada: {e}")

#Ruta para mostar la imagen original
@app.get("/imagen-original/{id_muestra}")
def get_original_image(id_muestra: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = "SELECT sampleRoute FROM samples WHERE id = %s"
        cursor.execute(sql, (id_muestra,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")

        filename = result[0]
        original_path = f"ia/resultados/img/{filename}"  # Asegúrate de que el archivo está en esta ruta

        if not os.path.exists(original_path):
            raise HTTPException(status_code=404, detail="Imagen original no encontrada")

        return FileResponse(original_path, media_type="image/png")

    except Exception as e:
        print(f"ERROR AL CARGAR IMAGEN ORIGINAL: {e}")  # <-- log
        raise HTTPException(status_code=400, detail=f"Error al cargar imagen original: {e}")

#Ruta para mostar la informacion de la muestra
@app.get("/muestra-info/{id_muestra}")
def getSample(id_muestra: int):
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM samples WHERE id = %s"
    cursor.execute(sql, (id_muestra,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Muestra no encontrada")
    
    return {"sample": result[0]}

#Ruta para mostar todas las muestras
@app.get("/samples")
def getSamples():
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM samples WHERE state = 1"  # Solo muestras activas
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Muestras no encontradas")
    
    return {"samples": result}

#Ruta para mostar las muestras de un usuario
@app.get("/samples/{idUser}")
def getSamplesUser(idUser: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = "SELECT * FROM samples WHERE idUser = %s AND state = 1"
        cursor.execute(sql, (idUser,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        # if not result:
        #     raise HTTPException(status_code=404, detail="No cuenta con muestras")
        
        return {"samples": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eror: {e}") 

# Ruta para cambiar el estado de una muestra
@app.put("/sample/{sample_id}")
def update_state_sample(sample_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        sql = "UPDATE samples SET state = 0 WHERE id = %s"
        cursor.execute(sql, (sample_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")

        return {"message": "Estado de la muestra actualizado a 0"}
    finally:
        cursor.close()
        conn.close()


# Ruta para editar una muestra
@app.put("/sample/state/{sample_id}")
def update_sample(sample_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        sql = "UPDATE samples SET state = 0 WHERE id = %s"
        cursor.execute(sql, (sample_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")

        return {"message": "Estado de la muestra actualizado a 0"}
    finally:
        cursor.close()
        conn.close()
        
#Ruta para editar  una muestra
@app.put("/sample/update/{sampleID}")
async def update_sample(
    sampleID: int,
    sampleName: str = Form(...),
    typeSample: str = Form(...),
    volumenSample: str = Form(...),
    factorSample: str = Form(...),
    medioSample: str = Form(...),
    
):
    try:
        return RegistarMuestra.update_sample(
            sampleID=sampleID,
            sampleName=sampleName,
            typeSample=typeSample,
            volumenSample=volumenSample,
            factorSample=factorSample,
            medioSample=medioSample,
        )
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok"})

# Registrar un seguimiento
@app.post("/registrar-follow")
def registrarFollow(data: FollowCreate):
    try:
        return FollowCreate.save(
            followName=data.followName,
            followDescription=data.followDescription,
            idUser=data.idUser,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ver todos los seguimientos de un usuario
@app.get("/follows/{idUser}")
def getFollowsUser(idUser: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = "SELECT * FROM follows WHERE idUser = %s AND state = 1"
        cursor.execute(sql, (idUser,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"follows": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eror: {e}") 

# Ver todo el listado de seguimientos
@app.get("/follows")
def getFollows():
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = "SELECT * FROM follows WHERE state = 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"follows": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eror: {e}") 


# Ruta para actualizar un seguimiento
@app.put("/follows/update/{followID}")
async def update_follow(
    followID: int,
    followName: str = Form(...),
    followDescription: str = Form(...),
):
    return Follow.update(
        followID=followID,
        followName=followName,
        followDescription=followDescription
    )

# Ruta para cambiar el estado de un seguimiento
@app.put("/follow/state/{follow_id}")
def update_follow(follow_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        sql = "UPDATE follows SET state = 0 WHERE id = %s"
        cursor.execute(sql, (follow_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Seguimiento no encontrado")

        return {"message": "Estado del seguimiento actualizado a 0"}
    finally:
        cursor.close()
        conn.close()


#Ruta para mostar la informacion del follow
@app.get("/follows/info/{id_follow}")
def getFollow(id_follow: int):
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM follows WHERE id = %s"
    cursor.execute(sql, (id_follow,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    
    return {"follow": result[0]}

# Ver todos los records
@app.get("/records")
def getRecords():
    try:
        conn = get_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM records WHERE state = 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"records": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eror: {e}") 

# Ver todos los records de un seguimiento
@app.get("/records/{followID}")
def getRecords(followID: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM records WHERE followID = %s AND state = 1"
        cursor.execute(sql, (followID,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"records": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eror: {e}") 

# Registrar un record a un seguimiento
@app.post("/registrar-record-file")

async def registrar_record_file(
    followID: int = Form(...),
    dayNumber: str = Form(...),
    sampleRoute: UploadFile = File(...)):
    try:
        return RecordCreate.save_with_file(
        followID=followID,
        dayNumber=dayNumber,
        sampleRoute=sampleRoute
        )
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

#Ruta para mostar la informacion de la muestra
@app.get("/record-info/{id_muestra}")
def getSample(id_muestra: int):
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM records WHERE id = %s"
    cursor.execute(sql, (id_muestra,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Muestra no encontrada")
    
    return {"record": result[0]}


#Ruta para mostar la imagen original
@app.get("/record/imagen-original/{id_muestra}")
def get_original_image(id_muestra: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = "SELECT sampleRoute FROM records WHERE id = %s"
        cursor.execute(sql, (id_muestra,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")

        filename = result[0]
        original_path = f"ia/resultados/img/{filename}"  # Asegúrate de que el archivo está en esta ruta

        if not os.path.exists(original_path):
            raise HTTPException(status_code=404, detail="Imagen original no encontrada")

        return FileResponse(original_path, media_type="image/png")

    except Exception as e:
        print(f"ERROR AL CARGAR IMAGEN ORIGINAL: {e}")  # <-- log
        raise HTTPException(status_code=400, detail=f"Error al cargar imagen original: {e}")

#Ruta para mostar la imagen original
@app.get("/record/imagen-inferencia/{id_muestra}")
def get_inference_image(id_muestra: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = "SELECT sampleRoute FROM records WHERE id = %s"
        cursor.execute(sql, (id_muestra,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")

        filename = result[0]
        inference_path = f"ia/resultados/clustering_img/{filename}"  # Asegúrate de que el archivo está en esta ruta

        if not os.path.exists(inference_path):
            raise HTTPException(status_code=404, detail="Imagen de inferencia no encontrada")

        return FileResponse(inference_path, media_type="image/png")

    except Exception as e:
        print(f"ERROR AL CARGAR IMAGEN DE INFERENCIA: {e}")  # <-- log
        raise HTTPException(status_code=400, detail=f"Error al cargar imagen de inferencia: {e}")

# Actualizar estado de un record
@app.put("/records/state/{record_id}")
def update_record(record_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        sql = "UPDATE records SET state = 0 WHERE id = %s"
        cursor.execute(sql, (record_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Record no encontrado")

        return {"message": "Estado del record actualizado a 0"}
    finally:
        cursor.close()
        conn.close()

@app.put("/record/update/{recordID}")
async def updateRecord(
    recordID: int,
    dayNumber: str = Form(...),
):
    try:
        return RecordCreate.update_record(
            recordID=recordID,
            dayNumber=dayNumber,
        )
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/record-show/{idRecord}")
def show_record(idRecord: int):
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT id,countCol,dayNumber,creationDate FROM records WHERE id = %s"
    cursor.execute(sql, (idRecord,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Muestra no encontrada")
    
    return {"record": result}