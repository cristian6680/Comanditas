from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.usuario import Usuario
from app.schemas.token import Token
from app.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Login estándar OAuth2.
    El campo 'username' del formulario recibe el email del usuario.
    """
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not verify_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ingresado está inactivo"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=usuario.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra un usuario encriptando su clave con Bcrypt.
    """
    usuario_existe = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if usuario_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo '{usuario_in.email}'"
        )
    
    nuevo_usuario = Usuario(
        nombre=usuario_in.nombre,
        email=usuario_in.email,
        password_hash=get_password_hash(usuario_in.password),
        rol=usuario_in.rol,
        activo=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario