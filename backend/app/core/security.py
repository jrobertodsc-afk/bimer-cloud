import os
import time
import json
import base64
import hmac
import hashlib
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "bimer-cloud-secret-master-key-2026-roberto")
security_bearer = HTTPBearer(auto_error=False)

def gerar_hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, 100000)
    return f"{salt.hex()}:{key.hex()}"

def verificar_senha(senha: str, hash_salvo: str) -> bool:
    try:
        if not hash_salvo or ":" not in hash_salvo:
            return False
        salt_hex, key_hex = hash_salvo.split(":", 1)
        salt = bytes.fromhex(salt_hex)
        key = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, 100000)
        return hmac.compare_digest(key.hex(), key_hex)
    except Exception:
        return False

def _b64_url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _b64_url_decode(data: str) -> bytes:
    pad = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)

def criar_token_jwt(payload: dict, exp_segundos: int = 86400 * 30) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload_copy = payload.copy()
    payload_copy["exp"] = int(time.time()) + exp_segundos
    payload_copy["iat"] = int(time.time())
    
    h_b64 = _b64_url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    p_b64 = _b64_url_encode(json.dumps(payload_copy, separators=(',', ':')).encode('utf-8'))
    signing_input = f"{h_b64}.{p_b64}"
    
    signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input.encode('utf-8'), hashlib.sha256).digest()
    sig_b64 = _b64_url_encode(signature)
    return f"{signing_input}.{sig_b64}"

def decodificar_token_jwt(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        h_b64, p_b64, sig_b64 = parts
        signing_input = f"{h_b64}.{p_b64}"
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), signing_input.encode('utf-8'), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64_url_encode(expected_sig), sig_b64):
            return None
        
        payload = json.loads(_b64_url_decode(p_b64).decode('utf-8'))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None

def obter_usuario_logado(credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer)) -> dict:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado. Faça login para continuar.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    payload = decodificar_token_jwt(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão expirada ou token inválido. Faça login novamente.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return payload
