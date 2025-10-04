from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List, Optional

# LangChain imports para Hugging Face
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# Importações do banco de dados vetorial
from services.db.vector_store import VectorDBService

load_dotenv()

app = FastAPI(title="LangChain Chat com Hugging Face", version="1.0.0")

# Inicializar modelo Hugging Face (gratuito)
model_loaded = False
chat_chain = None
vector_db = None

def initialize_model():
    global chat_chain, model_loaded
    try:
        print("🤖 Carregando modelo Hugging Face...")
        
        # Modelo pequeno e rápido para chat em português
        model_id = "microsoft/DialoGPT-small"
        
        llm = HuggingFacePipeline.from_model_id(
            model_id=model_id,
            task="text-generation",
            model_kwargs={
                "temperature": 0.7, 
                "max_length": 100,
                "do_sample": True,
                "pad_token_id": 50256
            }
        )
        
        prompt = PromptTemplate(
            input_variables=["question"],
            template="Usuário: {question}\nAssistente:"
        )
        
        chat_chain = LLMChain(llm=llm, prompt=prompt)
        model_loaded = True
        print("✅ Modelo carregado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        model_loaded = False
        chat_chain = None

def initialize_vector_db():
    global vector_db
    try:
        print("🔍 Inicializando banco de dados vetorial...")
        vector_db = VectorDBService(collection_name="documents")
        vector_db.create_table_if_not_exists()
        vector_db.initialize()
        print("✅ Banco de dados vetorial inicializado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados vetorial: {e}")
        return False

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    model: str = "Hugging Face DialoGPT"
    status: str = "success"

class DocumentRequest(BaseModel):
    texts: List[str]
    metadatas: Optional[List[dict]] = None

class DocumentResponse(BaseModel):
    ids: List[str]
    status: str = "success"

class SearchRequest(BaseModel):
    query: str
    k: int = 3

class SearchResult(BaseModel):
    content: str
    metadata: dict
    score: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    status: str = "success"

@app.on_event("startup")
async def startup_event():
    """Carrega o modelo e banco de dados na inicialização da API"""
    initialize_model()
    initialize_vector_db()

@app.get("/")
async def root():
    return {
        "message": "LangChain Chat com Hugging Face funcionando!",
        "model_loaded": model_loaded,
        "vector_db_loaded": vector_db is not None,
        "model": "microsoft/DialoGPT-small" if model_loaded else "None"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if model_loaded else "model_not_loaded",
        "model_loaded": model_loaded,
        "vector_db_loaded": vector_db is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not model_loaded or chat_chain is None:
        return ChatResponse(
            response="🔄 Modelo ainda está carregando. Tente novamente em alguns segundos.",
            model="Loading",
            status="loading"
        )
    
    try:
        # Gerar resposta usando LangChain + Hugging Face
        print(f"💬 Processando: {request.message}")
        response = chat_chain.run(question=request.message)
        
        # Limpar resposta (remover texto extra)
        if "Assistente:" in response:
            response = response.split("Assistente:")[-1].strip()
        
        return ChatResponse(
            response=response,
            model="microsoft/DialoGPT-small",
            status="success"
        )
        
    except Exception as e:
        print(f"❌ Erro ao processar: {str(e)}")
        return ChatResponse(
            response=f"Desculpe, ocorreu um erro: {str(e)}",
            model="Error",
            status="error"
        )

@app.post("/documents", response_model=DocumentResponse)
async def add_documents(request: DocumentRequest):
    """Adiciona documentos ao banco de dados vetorial"""
    if vector_db is None:
        if not initialize_vector_db():
            raise HTTPException(status_code=500, detail="Banco de dados vetorial não disponível")
    
    try:
        ids = vector_db.add_texts(
            texts=request.texts,
            metadatas=request.metadatas
        )
        
        if not ids:
            raise HTTPException(status_code=500, detail="Falha ao adicionar documentos")
        
        return DocumentResponse(ids=ids, status="success")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar documentos: {str(e)}")

@app.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Realiza busca por similaridade no banco de dados vetorial"""
    if vector_db is None:
        if not initialize_vector_db():
            raise HTTPException(status_code=500, detail="Banco de dados vetorial não disponível")
    
    try:
        documents = vector_db.similarity_search(query=request.query, k=request.k)
        
        results = []
        for doc in documents:
            results.append(SearchResult(
                content=doc.page_content,
                metadata=doc.metadata,
                score=None  # A implementação atual não retorna scores
            ))
        
        return SearchResponse(results=results, status="success")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)