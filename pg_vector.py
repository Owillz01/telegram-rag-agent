import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("SUPABASE_DB_HOST", "")
DB_NAME = os.getenv("SUPABASE_DB_NAME", "postgres")
DB_USER = os.getenv("SUPABASE_DB_USER", "postgres")
DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD", "")
DB_PORT = os.getenv("SUPABASE_DB_PORT", "5432")

class SupabaseVectorDB:

    _instance = None
    _connection = None

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(SupabaseVectorDB, cls).__new__(cls)
    #         cls._instance._connect()
    #     return cls._instance


    def _connect(self):
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT,
            )
            self._connection.autocommit = True

    # def __del__(self):
    #     if self._connection and not self._connection.closed:
    #         self._connection.close()

    '''
    # embedding <-> {embedding_str}: Uses the pgvector Euclidean distance operator (<->) 
    to calculate the spatial distance between the stored vector (embedding) 
    and an incoming query vector ({embedding_str}). 
    Smaller values indicate higher semantic similarity. 

    # AS distance: Exposes the computed Euclidean distance in the result set so you can inspect 
    how close each match is.

    # ORDER BY embedding <-> {embedding_str}: Sorts the results from closest (most relevant) to furthest.

    # LIMIT {top_k}: Caps the results to the top $k$ closest matches.

    '''

    def search_similar_in_faq_embeddings(self, query_embedding: list[float], top_k: int =4):
        """
            Search for similar documents in documents_code using the <-> operator.
        """

        self._connect()
        # dims=1536 #based on OpenAi
        # embedding_str = (
        #     f"'[{','.join(str(v) for v in query_embedding)}]'::vector({dims})"
        # )
        # with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
        #     sql = f"""
        #             SELECT id, text_content, metadata, embedding <-> {embedding_str} AS distance
        #             FROM faq_embeddings 
        #             ORDER BY embedding <-> {embedding_str}
        #             LIMIT {top_k};
        #             """
        #     cursor.execute(sql)
        #     results = cursor.fetchall()

        # Format the float dimension array safely as a standard string representation
        vector_param = f"[{','.join(str(v) for v in query_embedding)}]"
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                        SELECT id, text_content, metadata, embedding <-> %s::vector AS distance
                        FROM faq_embeddings 
                        ORDER BY embedding <-> %s::vector
                        LIMIT %s;
                    """
            cursor.execute(query, (vector_param, vector_param, top_k))
            results = cursor.fetchall()
            return results