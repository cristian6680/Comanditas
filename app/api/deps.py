from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.token import TokenData

# Le indica a Swagger UI la ruta donde se solicitan los tokens
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de acceso",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settigs.SECRET_KEY, algorithm=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(sub=user_id)
    except JWTError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.id == int(token_data.sub)).first()
    if usuario is None:
        raise credentials_exception
    if not usuario.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Usuario inactivo")
    return usuario

