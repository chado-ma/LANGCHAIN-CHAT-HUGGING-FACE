from services.db.vector_store import VectorDBService

def initialize_database():
    """Inicializa o banco de dados e cria as tabelas necessárias"""
    print("🏗️ Inicializando banco de dados vetorial...")
    vector_db = VectorDBService(collection_name="documents")
    
    # Criar extensão pgvector
    if vector_db.create_table_if_not_exists():
        print("✅ Banco de dados vetorial inicializado com sucesso!")
    else:
        print("❌ Falha ao inicializar banco de dados vetorial")
    
    return vector_db

if __name__ == "__main__":
    # Execute este script para inicializar o banco de dados
    initialize_database()