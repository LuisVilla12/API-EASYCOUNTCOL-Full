from pydantic import BaseModel
from datetime import date
from datetime import datetime
from passlib.context import CryptContext
from db import get_db
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class FollowCreate(BaseModel):
    followName: str
    followDescription: str
    idUser: int

    @classmethod
    def save(cls, followName: str, followDescription: str, idUser: int):
        try:
            ahoraActual = datetime.now()
            creation_time = ahoraActual.strftime("%H:%M:%S")
            
            conn = get_db()
            cursor = conn.cursor()

            sql = """
                INSERT INTO follows (
                    name, idUser, description, creationDate, creationTime, state
                ) 
                VALUES (%s, %s, %s, %s, %s,1)
            """
            cursor.execute(sql, (
                followName,
                idUser,
                followDescription,
                date.today(),
                creation_time
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
    