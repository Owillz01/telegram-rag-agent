from langchain.tools import tool
from retrival import answer_handler, get_faq
import logging as log

@tool
def generateRagResponse(query:str) -> str:
    """Answer Mental Health related Questions. Answer strictly from provided context.
       Args:
            query: Natural language search query.

       Returns:
            well compose response text base on retrieveed context and query. 
    """
    log.info('=============== CALLING generateRagResponse TOOL ============\n\n')
    rag_res = get_faq(query)
    model_res = answer_handler(query, rag_res)
    return model_res

@tool
def chatResponse(query:str) -> str:
    """generate reponse that are NOT Mental Health related
       Args:
            query: Natural language search query.

       Returns:
            befitting response to chat. 
    """
    log.info('=============== CALLING chatResponse TOOL ============\n\n')
    model_res = answer_handler(query)
    return model_res