from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from ..core.database import get_connection
from ..core.security import gerar_hash_senha, verificar_senha, criar_token_jwt, obter_usuario_logado

router = APIRouter(tags=["Autenticação & Sessão"])

class LoginEntrada(BaseModel):
    email: str
    senha: str

class AlterarSenhaEntrada(BaseModel):
    senha_atual: str
    nova_senha: str

@router.post("/login")
def login(dados: LoginEntrada):
    email_clean = dados.email.strip().lower()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, senha_hash, perfil, ativo FROM usuarios WHERE LOWER(email) = ?", (email_clean,))
    user = cur.fetchone()
    
    if not user or not user["ativo"]:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )
    
    if not verificar_senha(dados.senha, user["senha_hash"]):
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )
    
    hoje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE usuarios SET ultimo_login = ? WHERE id = ?", (hoje, user["id"]))
    conn.commit()
    conn.close()
    
    usuario_info = {
        "id": user["id"],
        "nome": user["nome"],
        "email": user["email"],
        "perfil": user["perfil"]
    }
    
    token = criar_token_jwt(usuario_info)
    return {
        "success": True,
        "access_token": token,
        "token_type": "Bearer",
        "usuario": usuario_info
    }

@router.get("/me")
def obter_me(usuario: dict = Depends(obter_usuario_logado)):
    return {"success": True, "usuario": usuario}

@router.post("/alterar-senha")
def alterar_senha(dados: AlterarSenhaEntrada, usuario: dict = Depends(obter_usuario_logado)):
    if len(dados.nova_senha) < 6:
        raise HTTPException(status_code=400, detail="A nova senha deve ter no mínimo 6 caracteres.")
        
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT senha_hash FROM usuarios WHERE id = ?", (usuario["id"],))
    row = cur.fetchone()
    
    if not row or not verificar_senha(dados.senha_atual, row["senha_hash"]):
        conn.close()
        raise HTTPException(status_code=400, detail="Senha atual incorreta.")
        
    novo_hash = gerar_hash_senha(dados.nova_senha)
    cur.execute("UPDATE usuarios SET senha_hash = ? WHERE id = ?", (novo_hash, usuario["id"]))
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "Senha alterada com sucesso!"}
