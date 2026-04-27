
from pydantic import BaseModel
from datetime import date
from datetime import datetime
from passlib.context import CryptContext
from db import get_db
from fastapi import HTTPException, UploadFile
from PIL import Image  # <-- ¡IMPORTANTE! necesitas importar PILLOW
import shutil
import os
import uuid
import time
import cv2
# from ia.algoritmo_water import tratamiento_imagen
from ia.infer import tratamiento_imagen


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class RecordCreate(BaseModel):
    followID: int
    dayNumber: int
    sampleRoute: str
    countCol: int
    creationDate: date
    creationTime: str
    processingTime: float
    optimalClusters: int


    @classmethod
    def save_with_file(cls, followID: int, dayNumber: str, sampleRoute: UploadFile):
        try:
            #Verificar existencia de las carpetas donde esta almacenada las imagenes
            os.makedirs("ia/resultados/img", exist_ok=True)
            os.makedirs("ia/resultados/clustering", exist_ok=True)
            
            # Asignar un nombre unico
            filename = f"{uuid.uuid4().hex}_{sampleRoute.filename}"
            file_location = f"ia/resultados/img/{filename}"
            # Reinicia el puntero del archivo al primer
            sampleRoute.file.seek(0) 
        
            # Reiniciar lectura del archivo
            with open(file_location, "wb") as buffer:
                # Guarda el archivo subidoa la carpeta uploads
                shutil.copyfileobj(sampleRoute.file, buffer)
                
            start_time = time.time()  
            # Extreaer los resultados del procesamiento de la imagen
            resultado = tratamiento_imagen(filename)
            
            if resultado["labels"] == 0:
                raise HTTPException(status_code=400, detail="No se detectaron objetos en la imagen.")
            
            end_time = time.time()   
            processing_time = end_time - start_time 
            
            # Asignar variables del resultado
            image_resultado = resultado["image_resultado"]
            labels = resultado["labels"]
            optimal_clusters = int(resultado["optimal_clusters"])
            clusters_detail = resultado["clustersDetail"]
            print("Resultado del tratamiento de imagen:", optimal_clusters, clusters_detail)
            
            # Determinar la hora
            ahoraActual = datetime.now()
            creation_time = ahoraActual.strftime("%H:%M:%S")
            
            
            # Crear la instancia de RegistarMuestra
            record = cls(
                followID=followID,
                sampleRoute=filename,
                countCol=labels,
                dayNumber=dayNumber,
                processingTime=processing_time,
                creationDate=date.today(),
                creationTime=creation_time,
                optimalClusters=optimal_clusters
            )
            creation_date_str = record.creationDate.strftime("%Y-%m-%d")
            # 4. Guardar en la base de datos
            conn = get_db()
            cursor = conn.cursor()

            sql = """
                INSERT INTO records (
                    followID, sampleRoute, countCol, dayNumber, creationTime, creationDate, state, processingTime, optimalClusters,clustersDetail
                )   
                VALUES (%s, %s, %s, %s, %s, %s, 1, %s, %s, %s)
            """
            cursor.execute(sql, (
                record.followID,
                record.sampleRoute,
                record.countCol,
                record.dayNumber,
                record.creationTime,
                creation_date_str,
                record.processingTime,
                record.optimalClusters,
                clusters_detail
            ))  
                        
                        
            record_id = cursor.lastrowid

            conn.commit()
            cursor.close()
            conn.close()

            # Regresar el id de la muestra y mensaje
            return {
                "success": True,
                "idSample": record_id,
                "message": "Muestra registrada correctamente."
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al registrar muestra: {e}")
    
    @classmethod
    # METODO PARA ACTUALIZAR MUESTRA
    def update_record(cls, recordID: int, dayNumber: str):
        try:
            conn = get_db()
            cursor = conn.cursor()

            sql = """
                UPDATE records
                SET 
                    dayNumber = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                dayNumber,
                recordID))

            conn.commit()
            cursor.close()
            conn.close()

            return {
                "success": True,
                "idSample": recordID,
                "message": "Muestra actualizada correctamente."
            }

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al actualizar muestra: {e}")