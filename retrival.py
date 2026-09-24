from pydantic_ai.models.openai import OpenAIResponsesModel
import openai
import os

from pg_vector import SupabaseVectorDB
from pydantic_ai import Agent

from dotenv import load_dotenv
from pydantic_ai.exceptions import UsageLimitExceeded

load_dotenv()

def get_faq(query:str) -> str:
    db = SupabaseVectorDB()

    try:
        client = openai.OpenAI()

        query_res = client.embeddings.create( model="text-embedding-3-small", input=query )
        print("QUERY RES >>>>: ", query_res)
        embedded_query = query_res.data[0].embedding

        docs = db.search_similar_in_faq_embeddings(embedded_query, top_k=2)

        results = []
        count = 0
        for doc in docs:
            print(doc, count+1)
            results.append(doc['text_content'])

        return "\n".join(results)
    except UsageLimitExceeded as e:
        return (
            f'Error retrieving info, tool usage limit exceded: {e}'
        )
    except Exception as e:
        return f'Error occured!!!'


def answer_handler(raw_query, retrieved_info=None) -> str:

    prompt = f'Context: {retrieved_info} \n Question: {raw_query}'
    response = openai.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            # {'role': 'system', 'content': "You are a Mental Health FAQ Assistant. Answer strictly from context when provided. If context doesn't cover the question, say so — don't guess."},
            {'role': 'system', 'content': "You are a Mental Health FAQ Assistant. Answer strictly from context when provided."},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response.choices[0].message.content