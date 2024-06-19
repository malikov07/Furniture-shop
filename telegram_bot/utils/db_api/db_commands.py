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
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
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

    # async def create_table_users(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS users_telegramuser (
    #     id SERIAL PRIMARY KEY,
    #     full_name VARCHAR(255) NOT NULL,
    #     username varchar(255) NULL,
    #     telegram_id BIGINT NOT NULL UNIQUE
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id,created_date):
        sql = "INSERT INTO users_telegramuser (full_name, username, telegram_id, created_date) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, full_name, username, telegram_id, created_date, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users_telegramuser"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users_telegramuser WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users_telegramuser"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE users_telegramuser SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users_telegramuser WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users_telegramuser", execute=True)

    ### Mahsulotlar uchun jadval (table) yaratamiz
    # async def create_table_products(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS shop_product (
    #     id SERIAL PRIMARY KEY,
    #
    #     -- Mahsulot kategoriyasi
    #     category_code VARCHAR(20) NOT NULL,
    #     category_name VARCHAR(50) NOT NULL,
    #
    #     -- Mahsulot kategoriya ichida ketgoriyasi ("Go'sht"->"Mol go'shti")
    #     subcategory_code VARCHAR(20) NOT NULL,
    #     subcategory_name VARCHAR(50) NOT NULL,
    #
    #     -- Mahsulot haqida malumot
    #     productname VARCHAR(50) NOT NULL,
    #     photo varchar(255) NULL,
    #     price INT NOT NULL,
    #     description VARCHAR(3000) NULL
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    async def add_product(
        self,
        category_code,
        category_name,
        subcategory_code,
        subcategory_name,
        productname,
        photo=None,
        price=None,
        description="",
    ):
        sql = "INSERT INTO shop_product (name, description, price, image, width, height, deep, color, material, style, company_name, country, warranty_duration, slug,) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14) returning *"
        return await self.execute(
            sql,
            category_code,
            category_name,
            subcategory_code,
            subcategory_name,
            productname,
            photo,
            price,
            description,
            fetchrow=True,
        )

    async def add_category(self, name, created_date):
        sql = "INSERT INTO shop_category (name, created_date) VALUES ($1, $2) RETURNING *"
        return await self.execute(sql, name, created_date, fetchrow=True)

    async def get_category(self, category_id):
        sql = "SELECT * FROM shop_category WHERE id=$1"
        return await self.execute(sql, category_id, fetchrow=True)

    async def get_categories(self):
        sql = "SELECT * FROM shop_category"
        return await self.execute(sql, fetch=True)

    async def update_category(self, category_id, name):
        sql = "UPDATE shop_category SET name=$1 WHERE id=$2 RETURNING *"
        return await self.execute(sql, name, category_id, fetchrow=True)

    async def delete_category(self, category_id):
        sql = "DELETE FROM shop_category WHERE id=$1 RETURNING *"
        return await self.execute(sql, category_id, fetchrow=True)

    ### Product Methods ###
    async def add_product(self, name, description, price, image, width, height, deep, color, material, style, company_name, country, warranty_duration, slug, created_date, updated_date):
        sql = """
        INSERT INTO shop_product (name, description, price, image, width, height, deep, color, material, style, company_name, country, warranty_duration, slug, created_date, updated_date) 
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16) 
        RETURNING *
        """
        return await self.execute(sql, name, description, price, image, width, height, deep, color, material, style, company_name, country, warranty_duration, slug, created_date, updated_date, fetchrow=True)

    async def get_product(self, product_id):
        sql = "SELECT * FROM shop_product WHERE id=$1"
        return await self.execute(sql, product_id, fetchrow=True)

    async def get_products(self):
        sql = "SELECT * FROM shop_product"
        return await self.execute(sql, fetch=True)

    async def update_product(self, product_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${idx + 2}" for idx, key in enumerate(kwargs.keys())])
        sql = f"UPDATE shop_product SET {set_clause} WHERE id = $1 RETURNING *"
        return await self.execute(sql, product_id, *kwargs.values(), fetchrow=True)

    async def delete_product(self, product_id):
        sql = "DELETE FROM shop_product WHERE id=$1 RETURNING *"
        return await self.execute(sql, product_id, fetchrow=True)