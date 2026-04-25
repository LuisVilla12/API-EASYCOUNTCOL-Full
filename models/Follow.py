from pydantic import BaseModel
from datetime import date
from datetime import datetime
from passlib.context import CryptContext
from db import get_db
from fastapi import HTTPException



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Follow(BaseModel):
    followName: str
    followDescription: str
    idUser: int
    creationDate: date
    creationTime: str

    @classmethod
    def save(cls, followName: str, followDescription: str, idUser: int):
        try:
            ahoraActual = datetime.now()
            creation_time = ahoraActual.strftime("%H:%M:%S")
            muestra = cls(
                followName=followName,
                idUser=idUser,
                followDescription=followDescription,
                creationDate=date.today(),
                creationTime=creation_time,
            )

            # 4. Guardar en la base de datos
            conn = get_db()
            cursor = conn.cursor()

            sql = """
                INSERT INTO follows (
                    name, idUser, description, creationDate, creationTime, state
                ) 
                VALUES (%s, %s, %s, %s, %s,1)
            """
            cursor.execute(sql, (
                muestra.followName,
                muestra.idUser,
                muestra.followDescription,
                muestra.creationDate,
                muestra.creationTime
            ))
            follow_id = cursor.lastrowid

            conn.commit()
            cursor.close()
            conn.close()

            # Regresar el id de la muestra y mensaje
            return {
                "success": True,
                "idFollow": follow_id,
                "message": "Seguimiento registrado correctamente."
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al registrar seguimiento: {e}")
    
    @classmethod
    def update(cls, followID: int, followName: str, followDescription: str):
        try:
            conn = get_db()
            cursor = conn.cursor()

            sql = """
                UPDATE follows
                SET 
                    name = %s,
                    description = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                followName,
                followDescription,
                followID
            ))

            conn.commit()
            cursor.close()
            conn.close()

            return {
                "success": True,
                "id": followID,
                "message": "Seguimiento actualizado correctamente."
            }

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al actualizar seguimiento: {e}")   
        
        
        
        
        
