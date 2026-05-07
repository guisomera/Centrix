import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()                       #Pega as variaveis do ambiente ev 
dsn = os.getenv("DSN")

async def open_pool():
    pool = await asyncpg.create_pool(dsn, min_size=2, max_size=3)   #Cria pool de conexões
    return pool     #Retorna pool de conexoes

async def execuete_command(pool, command):
    async with pool.acquire() as conn:            #With garante que vai abir e fechar / pool.acquire() pega as conexões e atribui a conn
        response = await conn.fetch(command)    #Roda o comando que vai receber 
        return response     #Retorna comando

async def main():
    pool = await open_pool()

    response = await execuete_command(pool, command="SELECT * FROM condominios")
    for c in response:
       print(c["nome_cond"], c["id_sindico"])
    await pool.close()      #Abre pool, executa comando e fecha 
