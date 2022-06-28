from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:
    
    def __init__(self):
        self.pool: Union[Pool, None] = None
        
    
    async def create(self):
        self.pool = await asyncpg.create_pool(
            user = config.DB_USER,
            password = config.DB_PASS,
            host = config.DB_HOST,
            name = config.DB_NAME
        )
        
    
    async def execute(
        self, command, *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result
      
        
    async def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            username varchar(255) NULL,
            lang varchar(3) NOT NULL,
            telegram_id BIGINT NOT NULL UNIQUE
            );
            """
        await self.execute(sql, execute=True)
        
        
    async def create_table_channels(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Channels (
            id SERIAL PRIMARY KEY,
            
            channel_id BIGINT NOT NULL UNIQUE,
            channel_link varchar(20) not null,
            
            admin_id BIGINT NOT NULL UNIQUE,
            admin_link varchar(20)
            );
            """
        await self.execute(sql, execute=True)