# 🤖 LangChain Chat com Hugging Face

Sistema de chat inteligente usando LangChain + Hugging Face para indexação de documentos e comunicação com modelos de IA gratuitos.

## ⚡ Execução Rápida

**Depois de configurar o ambiente virtual e instalar dependências:**

```bash
python -m services.api.main
```

**Pronto!** Acesse: http://localhost:8000/docs 🚀

---

## 📋 Pré-requisitos

- **Python 3.9+** instalado
- **Git** (opcional)
- **4GB+ RAM** (para modelos Hugging Face)

## 🚀 Instalação e Configuração

### 1. **Clone ou Download do Projeto**
```bash
# Se usar Git
git clone <seu-repositorio>
cd "LangChain Chat"

# Ou simplesmente navegue até a pasta do projeto
cd "C:\Projetos\Estudos\LangChain Chat"
```

### 2. **Criar Ambiente Virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows (PowerShell):
venv\Scripts\activate

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate
```

**✅ Verificar se ativou:** O prompt deve mostrar `(.venv)` no início

### 3. **Instalar Dependências**
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar todas as dependências
pip install -r requirements.txt
```

### 4. **Configurar Variáveis de Ambiente (Opcional)**
```bash
# Criar arquivo .env na raiz do projeto
echo "HF_MODEL_ID=microsoft/DialoGPT-small" > .env
echo "CACHE_DIR=./models_cache" >> .env
```

## 🏃‍♂️ Executando a Aplicação

### **Comando Principal (Recomendado)**
```bash
# Da raiz do projeto - comando único!
python -m services.api.main
```

### **Métodos Alternativos:**

**Método 1: Navegar e executar**
```bash
cd services\api
python main.py
```

**Método 2: Uvicorn diretamente**
```bash
uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Acessando a API

Após iniciar o servidor, acesse:

- 🏠 **API Principal**: http://localhost:8000
- 📚 **Documentação (Swagger)**: http://localhost:8000/docs
- 📖 **Redoc**: http://localhost:8000/redoc
- ❤️ **Health Check**: http://localhost:8000/health

## 🤖 Modelos Disponíveis

### **Modelo Padrão: microsoft/DialoGPT-small**
- ✅ **Gratuito e local**
- ✅ **Conversação em inglês**
- ✅ **Tamanho: ~120MB**
- ✅ **Rápido para testes**

### **Outros Modelos Recomendados:**
```python
# Para chat em português
"neuralmind/bert-base-portuguese-cased"

# Para perguntas e respostas
"google/flan-t5-small"

# Para conversação mais avançada
"microsoft/DialoGPT-medium"
```

## 🧪 Testando a API

### **1. Teste Básico (Health Check)**
```bash
curl http://localhost:8000/health
```

### **2. Teste de Chat**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Olá, como você está?"}'
```

### **3. Via Swagger UI**
1. Acesse http://localhost:8000/docs
2. Clique em **POST /chat**
3. Clique em **Try it out**
4. Digite sua mensagem no campo `message`
5. Clique em **Execute**

## 📁 Estrutura do Projeto

```
LangChain Chat/
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências do Python
├── .env                     # Variáveis de ambiente (opcional)
├── services/
│   └── api/
│       └── main.py          # API FastAPI principal
├── models/                  # Cache dos modelos (criado automaticamente)
├── agent/                   # Agentes LangChain (futuro)
├── utils/                   # Utilitários (futuro)
└── venv/                    # Ambiente virtual
```

## ⚙️ Configurações Avançadas

### **Alterar Modelo**
Edite o arquivo `services/api/main.py`:
```python
# Linha ~25
model_id = "seu-modelo-preferido"
```

### **Ajustar Parâmetros do Modelo**
```python
model_kwargs={
    "temperature": 0.7,      # Criatividade (0.0-1.0)
    "max_length": 200,       # Tamanho máximo da resposta
    "do_sample": True,       # Usar amostragem
    "pad_token_id": 50256    # Token de padding
}
```

### **Cache de Modelos**
Os modelos são baixados automaticamente na primeira execução e salvos em:
- Windows: `%USERPROFILE%\.cache\huggingface`
- Linux/Mac: `~/.cache/huggingface`

## 🛠️ Solução de Problemas

### **Erro: "Import could not be resolved"**
```bash
# Verificar se o ambiente virtual está ativo
# Deve mostrar (.venv) no prompt
venv\Scripts\activate

# Reinstalar dependências
pip install -r requirements.txt
```

### **Erro: "Model not found"**
```bash
# Limpar cache e baixar novamente
pip install --upgrade transformers huggingface-hub
```

### **Erro: "CUDA out of memory"**
```python
# Usar modelo menor
model_id = "microsoft/DialoGPT-small"  # Em vez de "medium" ou "large"
```

### **Porta já em uso**
```bash
# Usar porta diferente
uvicorn services.api.main:app --host 0.0.0.0 --port 8001 --reload
```

## � Comandos Essenciais

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar aplicação
python -m services.api.main

# 4. Acessar: http://localhost:8000/docs
```

## �📈 Próximos Passos

- [ ] **Indexação de Documentos** (PDF, DOCX, TXT)
- [ ] **Banco Vetorial** (Chroma, FAISS)
- [ ] **Chat com Histórico**
- [ ] **Interface Web** (Streamlit/Gradio)
- [ ] **Deploy na Nuvem** (Azure, AWS, GCP)

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/langchain-chat/issues)
- **Documentação LangChain**: https://python.langchain.com/docs/
- **Hugging Face**: https://huggingface.co/docs

---

**Desenvolvido com ❤️ usando LangChain + Hugging Face**