from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import PROJECT_NAME, VERSION, API_PREFIX, CORS_ORIGINS
from .api import titulos, previsoes, adiantamentos, auth, fornecedores

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="Backend Oficial JR Solutions - Plataforma de Gestao Financeira, Contas a Pagar e Retencoes Tributarias"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{API_PREFIX}/auth")
app.include_router(auth.router, prefix="/api/contas-a-pagar/auth")

app.include_router(titulos.router, prefix=API_PREFIX)
app.include_router(previsoes.router, prefix=API_PREFIX)
app.include_router(adiantamentos.router, prefix=API_PREFIX)
app.include_router(fornecedores.router, prefix=API_PREFIX)

app.include_router(titulos.router, prefix="/api/contas-a-pagar")
app.include_router(previsoes.router, prefix="/api/contas-a-pagar")
app.include_router(adiantamentos.router, prefix="/api/contas-a-pagar")
app.include_router(fornecedores.router, prefix="/api/contas-a-pagar")

@app.get("/")
def root():
    return {
        "app": PROJECT_NAME,
        "version": VERSION,
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "bimer-cloud-api"}