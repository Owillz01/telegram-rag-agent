import csv
import json
import os

# from langchain_huggingface import HuggingFaceEmbeddings
import openai
# from openai import OpenAI
import psycopg2
from dotenv import load_dotenv

load_dotenv()


# Postgres connection info
POSTGRES_HOST = os.getenv("SUPABASE_DB_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("SUPABASE_DB_PORT", 5432))
POSTGRES_DB = os.getenv("SUPABASE_DB_NAME", "postgres")
POSTGRES_USER = os.getenv("SUPABASE_DB_USER", "postgres")
POSTGRES_PASS = os.getenv("SUPABASE_DB_PASSWORD", "")

# from langchain_huggingface import HuggingFaceEmbeddings

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}

openai.api_key = os.getenv("OPENAI_API_KEY")
# openai = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),                       # was: OPENAI_API_KEY
#     base_url="https://api.llmgateway.io/v1",   
# )


FILE_PATH = 'data/mhfaq.csv'

EMBED_DIMENSION = 1536


def connect_to_postgres():
    """Connects and returns a postgress connection"""

    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASS,
    )

    return conn


def create_table_if_not_existing(conn):
    """
        create the faq_embeddings table if it does nt exisit.
        install and activate pgvector extension for this to work
    """

    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS faq_embeddings (
            id            SERIAL PRIMARY KEY,
            source_id     TEXT,
            chunk_index   INT,
            text_content  TEXT,
            metadata      JSONB,
            embedding     VECTOR({EMBED_DIMENSION})
        );
    """

    create_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_faq_embeddings_embedding
            ON faq_embeddings
            USING ivfflat (embedding vector_l2_ops)
            WITH (lists = 100);
    """

    with conn.cursor() as cur:
        cur.execute(create_table_sql)
        cur.execute(create_index_sql)
        conn.commit()

def chunk_text(text, max_chars=2000):
    chunks = []
    start = 0
    while start < len(text):
        end = start+max_chars
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
        return chunks

def get_embedding(text):
    response = openai.Embedding.create(model="text-embedding-3-small", input=text)
    # Extract embeddings (returns a list of floats)
    vector = response["data"][0]["embedding"]
    return vector

def insert_embedding_row( conn, source_id, chunk_idx, text_content, metadata_dict, embedding_vector ):
    insert_query = """
        INSERT INTO faq_embeddings (source_id, chunk_index, text_content, metadata, embedding)
        VALUES (%s, %s, %s, %s, %s);
    """

    with conn.cursor() as cur:
        cur.execute(
            insert_query,
            (
                source_id,
                chunk_idx,
                text_content,
                json.dumps(metadata_dict),
                embedding_vector,
            ),
        )


def process_csv_and_store_embeddings(csv_file_path):
    """
    Read CSV with headers, embed text from each row, chunk if needed,
    and store results in my_embeddings table.
    """
    conn = connect_to_postgres()
    create_table_if_not_existing(conn)
    csv_file_path = FILE_PATH

    with open(csv_file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")  # Use semicolon as delimiter
        for idx, row in enumerate(reader):
            # Use row index as the source_id
            source_id = str(idx)

            # Build a structured text string with clear labels matching the English CSV columns
            structured_text = (
                f"Question ID: {row.get('Question_ID', '').strip()}\n"
                f"Questions: {row.get('Questions', '').strip()}\n"
                f"Answers: {row.get('Answers', '').strip()}\n"
            )

            metadata_dict = dict(row)

            # If the text is very large, chunk it into manageable pieces
            text_chunks = chunk_text(structured_text, max_chars=2000)

            # For each text chunk, generate an embedding and insert it into the database
            for i, chunk in enumerate(text_chunks):
                client = openai.OpenAI()
                response = client.embeddings.create(
                    model="text-embedding-3-small", input=chunk
                )
                embedding_vector = response.data[0].embedding
                insert_embedding_row(
                    conn,
                    source_id=source_id,
                    chunk_idx=i,
                    text_content=chunk,
                    metadata_dict=metadata_dict,
                    embedding_vector=embedding_vector,
                )
        conn.commit()

    conn.close()        


if __name__ == "__main__":
    process_csv_and_store_embeddings(FILE_PATH)
    print("CSV data successfully processed and embeddings stored.")