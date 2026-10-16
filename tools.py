from langchain.tools import tool
from retrival import answer_handler, get_faq
import logging as log
from tavily import TavilyClient
import os

TAVILY_SEARCH_API = os.getenv("TAVILY_SEARCH_API")

tavily_client = TavilyClient(api_key=TAVILY_SEARCH_API)

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

@tool
def tavilySearch(query:str, max_result:int) -> str:
    """Uses Tavily to search the web for latest and acurate inforation for a given query.
     Args:
          query: search query to execute
          max_result: Maximum number of results to be returned (default: 1)
     Returns:
        Formatted search results with full webpage content
    """
    log.info('=============== CALLING tavilySearch TOOL ============\n\n')
#     results = tavily_client.search(query,
#         max_results=max_result)
    results = {'query': '2026 best investment options beginner diversified portfolio current interest rates bonds stocks ETFs retirement accounts', 'follow_up_questions': None, 'answer': None, 'images': [], 'results': [{'url': 'https://useorigin.com/resources/blog/10-best-investments-for-beginners-in-2026-with-tools-tips', 'title': '10 Best Investments for Beginners in 2026 (With Tools & Tips)', 'content': '### Index Funds\n\nIndex funds are a staple for beginner investors because they’re diversified, low-cost, and built for long-term growth. They remove the pressure to pick winners and instead track the broader market. The risk isn’t the fund itself—it’s duplication. Beginners often end up holding similar index exposure across multiple accounts without realizing it. [...] In 2026, beginner-friendly investments tend to share a few traits. They’re relatively transparent, diversified by default, cost-efficient, and designed for long-term participation rather than short-term trading. They also integrate well with automation, which matters more than most people realize. [...] ETFs offer flexibility and accessibility, often appealing to beginners who want diversification with more control. They cover everything from broad markets to specific sectors. Because ETFs are easy to buy, it’s also easy to overdo it. Multiple ETFs can overlap significantly, creating complexity without adding diversification.\n\nA consolidated view of holdings helps beginners understand what they actually own beneath the ticker symbols.', 'score': 0.7274535, 'raw_content': None, 'id': '5224bc-00'}, {'url': 'https://finance.yahoo.com/news/top-3-bond-etfs-buy-065300387.html', 'title': 'The Top 3 Bond ETFs to Buy With Interest Rates Falling', 'content': "Currently, 58% of the portfolio is in securitized bonds, while 24% is in investment-grade credit and 13% is in U.S. government bonds. Around 54% have maturities of 5 to 10 years, while 17% mature in 3 to 5 years, and 15% have maturities of 1 to 3 years.\n\nThe ETF has a one-year return of 8.5%, which beats the Bloomberg U.S. Aggregate Index one-year return of 7.3%. It has a 10-year average annualized return of 2.01%, beating the benchmark's return of 1.64%.\n\n## 2. Vanguard Long-Term Bond Fund", 'score': 0.6922474, 'raw_content': None, 'id': '6517b3-01'}, {'url': 'https://www.fidelity.com/learning-center/smart-money/what-to-invest-in', 'title': '11 top investments in 2026 | Fidelity', 'content': 'Investing for beginners\n           Trading for beginners\n           Crypto basics\n           Crypto: Beyond the basics\n           Alternative investing\n           Stocks and sectors\n           Initial public offerings\n           Income investing\n           Fundamental analysis\n           Technical analysis\n\n        Investment products\n\n           ETFs\n           Mutual funds\n           Stocks\n           Fixed income, bonds, CDs\n           Annuities\n           Closed-end funds [...] Potentially good for people who: are more risk-averse, are building a diversified portfolio, and/or want to support particular bond issuers.\n\nHow to buy: in investment accounts from a brokerage firm, like brokerage and retirement accounts. However, workplace retirement accounts may limit available options. In addition to individual bonds, investors can buy bond exchange-traded funds (ETFs) and mutual funds. Treasurys can be purchased from the US Treasury or through Fidelity. [...] Real talk and helpful tips about money, investing, and careers.\n\n- [x] \n\n Educational Webinars and Events \n\n \n\nFree financial education from Fidelity and other leading industry professionals.\n\nDone \n\nAdd subscriptions \n\nNo, thanks. \n\nLoading\n\n   Finding stock and sector ideas\n   Investing for beginners\n   Crypto\n   Managing taxes\n   Investing for income\n   Fixed income, bonds, CDs\n   Stocks\n   Using technical analysis\n   ETFs\n   Mutual funds\n   Trading options\n\n1.', 'score': 0.67988104, 'raw_content': None, 'id': '6c04ff-02'}], 'response_time': 2.5, 'request_id': '3fb64d46-c26c-4e10-b21e-0882bd26f00b'} 
    print(results, '<<<<<<<<<<<<<<')
    content = '';
    for res in results['results']:
        content += f"\n\n{res['title']} \n\n {res['url']} \n\n"
    return content