import asyncio
import llm
import database

async def ask_question():
    question = input("Qual informação voce deseja saber ?")
    llm_response = llm.create_sql(user_request=question)

    pool = await database.open_pool()
    database_response = await database.execuete_command(pool, llm_response)

    format_result = llm.format_result(question, database_response)
    print(format_result)

asyncio.run(ask_question())