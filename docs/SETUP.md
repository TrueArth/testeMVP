# Guia de Instalação e Execução

Este guia contém os passos detalhados para configurar e executar os ambientes de desenvolvimento do backend e do frontend.

## Pré-requisitos

- Python 3.10 ou superior
- Node.js 18 ou superior (recomendado via NVM)
- Git

### Dependências do Sistema (Ubuntu/Debian)
O projeto utiliza bibliotecas modernas que minimizam a necessidade de pacotes do sistema. No entanto, o `build-essential` e o `git` são recomendados:
```bash
sudo apt update && sudo apt install -y build-essential git
```

## 1. Configuração do Backend

Siga estes passos a partir da raiz do repositório. O projeto utiliza o **uv** para gerenciamento ultra-rápido de pacotes e ambientes.

```bash
# 1. Instale o uv (caso não possua)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Sincronize o ambiente e dependências
uv sync

# 3. Configure as variáveis de ambiente
cp .env.example .env

# Edite o arquivo .env com suas configurações
# Dica: Para desenvolvimento offline, use PACIENTE_PROVIDER_TYPE=CSV
nano .env
```

## 2. Configuração do Frontend

Estes passos devem ser executados em um novo terminal.

```bash
# 1. Navegue até a pasta do frontend
cd frontend

# 2. Instale as dependências e execute
npm install
npm run dev
```

## 3. Executando a Aplicação

### Servidor de Backend

Você pode iniciar o servidor de três formas:

**A. Usando o script automatizado (Recomendado):**
```bash
./start.sh
```

**B. Usando o uv run (Desenvolvimento):**
```bash
uv run uvicorn src.main:app --reload
```

**C. Executando como módulo:**
```bash
uv run python -m src.main
```

- O backend estará disponível em `http://127.0.0.1:8000`.
- O Swagger UI estará em `http://127.0.0.1:8000/docs`.

### Servidor de Frontend

Na pasta `frontend/`, execute o servidor de desenvolvimento do Vite.

```bash
npm run dev
```

- O frontend estará disponível em `http://127.0.0.1:5173` (ou outra porta indicada pelo Vite). O servidor de desenvolvimento do Vite já vem configurado com um proxy para o backend, então todas as chamadas de API para `/api` serão redirecionadas automaticamente para `http://127.0.0.1:8000`.

## 4. Build de Produção do Frontend

Para gerar a versão de produção do frontend, que é servida diretamente pelo FastAPI:

```bash
# Na pasta frontend/
npm run build
```

Os arquivos gerados em `frontend/dist/` serão servidos pela aplicação FastAPI quando ela não estiver em modo de desenvolvimento, na rota raiz (`/`).
