import asyncio
import llm
import database

async def ask_question():
    pool = await database.open_pool()
    general_context = []

    while True:
        question = input("Qual informação voce deseja saber ?\n Informe (1) para finalizar o chat\n")
        if question == "1":
            break
    
        llm_response = llm.create_sql(user_request=question, general_context = general_context)
        database_response = await database.execuete_command(pool, llm_response)

        format_result = llm.format_result(question, database_response)
        x = {question: format_result}
        general_context.append(x)
        print(f"\n{format_result} \n")

    await database.close_pool(pool)

asyncio.run(ask_question())