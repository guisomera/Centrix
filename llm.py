import asyncio, asyncpg
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY_ANTHROPIC")

def create_sql(user_request, general_context):
    client = Anthropic(api_key=api_key)
    schema_bd = read_schema()
    prompt = read_prompt_sql()

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=f"Schema banco de dados: {schema_bd}. Prompt: {prompt}",
        messages=[{
            "role": "user",
            "content": f"Pergunta do usuário: {user_request}. Contexto da conversa{general_context}"
        }]
    )   

    result = message.content[0].text
    return result   

def format_result(context, result_to_format):
    client = Anthropic(api_key=api_key)
    format_prompt = read_format_prompt()
    result_to_format = str(result_to_format)

    message = client.messages.create(
        model= "claude-sonnet-4-6",
        max_tokens=1024,
        system=format_prompt,
        messages=[{
            "role": "user",
            "content": f"Pergunta original: {context}.\n \nDados: {result_to_format}"
        }]
    )

    format_result = message.content[0].text
    return format_result

def read_schema():
    with open("Schema_BD.md") as f:
        schema_bd = f.read()
        return schema_bd
    
def read_prompt_sql():
    with open("prompt_sql.md") as f:
        prompt= f.read()
        return prompt

def read_format_prompt():
    with open("format_prompt.md") as f:
        format_promp = f.read()
        return format_promp
