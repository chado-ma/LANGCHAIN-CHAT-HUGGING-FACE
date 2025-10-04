from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# LangChain imports para Hugging Face
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

app = FastAPI(title="LangChain Chat com Hugging Face", version="1.0.0")

# Inicializar modelo Hugging Face (gratuito)
model_loaded = False
chat_chain = None

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

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    model: str = "Hugging Face DialoGPT"
    status: str = "success"

@app.on_event("startup")
async def startup_event():
    """Carrega o modelo na inicialização da API"""
    initialize_model()

@app.get("/")
async def root():
    return {
        "message": "LangChain Chat com Hugging Face funcionando!",
        "model_loaded": model_loaded,
        "model": "microsoft/DialoGPT-small" if model_loaded else "None"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if model_loaded else "model_not_loaded",
        "model_loaded": model_loaded
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)