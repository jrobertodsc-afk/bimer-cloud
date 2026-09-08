# ?? Bimer Cloud - Central de Documentos & Contas a Pagar

Sistema moderno de gestão financeira, contas a pagar, desmembramento de retenções tributárias federais e municipais, agenda de vencimentos e prestação de contas de adiantamentos corporativos no padrão de alta densidade visual **Alterdata Bimer**.

---

## ??? Arquitetura do Projeto

O projeto segue a arquitetura de **Monólito Modular Desacoplado**:
- **rontend/**: Interface SPA de alta densidade com viewport desktop (85%-100%), decodificador inteligente de boletos Febraban (47 e 48 dígitos) e régua de vencimentos. Pronta para deploy estático na **Vercel** ou **Cloudflare Pages**.
- **ackend/**: API RESTful em **FastAPI** modularizada por domínio (	itulos, previsoes, diantamentos), com suporte a CORS total e conteinerizada via **Docker**. Pronta para deploy no **Railway** ou **Render**.
- **database/**: Banco de dados SQLite persistente (imer.db), com suporte a migração simples para PostgreSQL / Turso no cloud.

---

## ?? Como Rodar Localmente

### 1. Iniciar o Backend (FastAPI):
\\\ash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
\\\
A documentação interativa estará disponível em: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Iniciar o Frontend:
\\\ash
cd frontend
python -m http.server 3000
\\\
Acesse no navegador: [http://localhost:3000](http://localhost:3000)

---

## ?? Como Fazer Deploy na Nuvem

### 1. Backend (Railway ou Render):
- Crie um novo projeto no **[Railway.app](https://railway.app)** ou **[Render.com](https://render.com)**.
- Conecte o repositório do GitHub e aponte a pasta raiz como ackend/ (ele detectará o Dockerfile automaticamente).
- Defina a variável de ambiente: \PORT=8000\.
- O Railway/Render gerará uma URL segura (ex: \https://bimer-api.up.railway.app\).

### 2. Frontend (Vercel):
- Crie um novo projeto no **[Vercel.com](https://vercel.com)**.
- Importe o repositório do GitHub e selecione a pasta raiz como rontend/.
- Clique em **Deploy**. A Vercel gerará o link global (ex: \https://bimer-cloud.vercel.app\).
