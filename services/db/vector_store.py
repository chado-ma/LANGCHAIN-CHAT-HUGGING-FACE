from sqlalchemy import create_engine
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração de conexão com o banco de dados
CONNECTION_STRING = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://user:user@localhost:5555/VECTORDB"
)

class VectorDBService:
    def __init__(self, collection_name="documents"):
        self.collection_name = collection_name
        self.connection_string = CONNECTION_STRING
        self._embeddings = None
        self.store = None

    @property
    def embeddings(self):
        """Inicializa o modelo de embeddings sob demanda"""
        if self._embeddings is None:
            # Usando modelo de embeddings em português
            model_name = "neuralmind/bert-base-portuguese-cased"
            self._embeddings = HuggingFaceEmbeddings(model_name=model_name)
        return self._embeddings

    def initialize(self):
        """Inicializa a conexão com o banco de dados vetorial"""
        try:
            self.store = PGVector(
                connection_string=self.connection_string,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados vetorial: {e}")
            return False

    def add_texts(self, texts, metadatas=None):
        """Adiciona textos ao banco de dados vetorial"""
        if not self.store:
            if not self.initialize():
                return False
        
        try:
            ids = self.store.add_texts(texts=texts, metadatas=metadatas)
            return ids
        except Exception as e:
            print(f"Erro ao adicionar textos: {e}")
            return None

    def similarity_search(self, query, k=3):
        """Realiza uma busca por similaridade"""
        if not self.store:
            if not self.initialize():
                return []
        
        try:
            results = self.store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Erro na busca por similaridade: {e}")
            return []

    def create_table_if_not_exists(self):
        """Cria a tabela se ela não existir (apenas para inicialização)"""
        try:
            engine = create_engine(self.connection_string)
            with engine.connect() as connection:
                connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
                print("✅ Extensão pgvector criada/verificada com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar extensão pgvector: {e}")
            return False