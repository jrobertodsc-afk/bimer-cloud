# 🏢 Bimer Cloud - Central de Documentos & Contas a Pagar

Sistema moderno de gestão financeira, contas a pagar, desmembramento de retenções tributárias federais e municipais, agenda de vencimentos e prestação de contas de adiantamentos corporativos no padrão de alta densidade visual **Alterdata Bimer**.

---

## 🏛️ Arquitetura do Projeto

O projeto segue a arquitetura de **Monólito Modular Desacoplado**:
- **rontend/**: Interface SPA de alta densidade com layout desktop nativo, decodificador inteligente de boletos Febraban (47 e 48 dígitos) e régua de vencimentos. Pronta para deploy estático na **Vercel** ou **Cloudflare Pages**.
- **ackend/**: API RESTful em **FastAPI** modularizada por domínio (	itulos, previsoes, diantamentos), com suporte a CORS total, conteinerizada via **Docker**. Pronta para deploy no **Railway** ou **Render**.
- **database/**: Banco de dados SQLite persistente (imer.db com 143+ registros reais), com suporte a migração para PostgreSQL ou LibSQL/Turso.

---

## 🚀 Como Rodar Localmente

### 1. Iniciar o Backend (FastAPI):
`ash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
`
- Documentação OpenAPI (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
- Healthcheck: [http://localhost:8000/health](http://localhost:8000/health)

### 2. Iniciar o Frontend:
`ash
cd frontend
python -m http.server 3000
`
- Acesse no navegador: [http://localhost:3000/index.html](http://localhost:3000/index.html)

---

## ☁️ Guia de Deploy Passo a Passo

### Passo 1: Subir o Projeto para o GitHub
No terminal da pasta imer-cloud:
`ash
# Se ainda não criou o repositório no GitHub, crie em: https://github.com/new
git remote add origin https://github.com/SEU_USUARIO/bimer-cloud.git
git branch -M main
git push -u origin main
`

---

### Passo 2: Deploy do Backend (Render ou Railway)

#### Opção A: Render (Recomendado - Gratuito)
1. Acesse [render.com](https://render.com) e conecte sua conta do GitHub.
2. Clique em **New +** -> **Web Service**.
3. Selecione o repositório imer-cloud.
4. O Render detectará automaticamente o arquivo ender.yaml já configurado na raiz!
   - **Root Directory**: ackend
   - **Build Command**: pip install -r requirements.txt
   - **Start Command**: uvicorn app.main:app --host 0.0.0.0 --port 
5. Clique em **Create Web Service**.
6. Copie a URL pública gerada (exemplo: https://bimer-cloud-api.onrender.com).

#### Opção B: Railway
1. Acesse [railway.app](https://railway.app) e conecte sua conta do GitHub.
2. Clique em **New Project** -> **Deploy from GitHub repo** -> selecione imer-cloud.
3. Em Settings, configure o **Root Directory** como /backend ou deixe o Dockerfile da raiz.
4. O Railway iniciará o build e gerará a URL (exemplo: https://bimer-cloud-production.up.railway.app).

---

### Passo 3: Deploy do Frontend (Vercel)
1. Acesse [vercel.com](https://vercel.com) e faça login.
2. Clique em **Add New...** -> **Project**.
3. Importe o repositório imer-cloud.
4. Em **Root Directory**, selecione a pasta rontend (ou mantenha na raiz, pois o ercel.json já está configurado).
5. Clique em **Deploy**.
6. A Vercel disponibilizará a URL pública instantaneamente (exemplo: https://bimer-cloud.vercel.app).

---

### Passo 4: Conectar Frontend ao Backend em Nuvem
1. Abra seu site na Vercel no navegador.
2. Na barra de ferramentas superior, clique no botão **⚙️ Nuvem**.
3. Cole a URL da API gerada no Render ou Railway (exemplo: https://bimer-cloud-api.onrender.com/api/contas-a-pagar).
4. Clique em **OK**. O sistema salvará a URL e se conectará automaticamente à API de nuvem!
