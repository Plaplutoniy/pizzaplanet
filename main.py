from fastapi import FastAPI
import asyncpg

from db import host, user, password, db_name
from models import Restaraunt, pizza, chef, review

app = FastAPI()

async def get_db():
    conn = await asyncpg.connect(
        host = host, user = user, password = password, database = db_name
    )
    return conn


@app.get("/rest", response_model=list[Restaraunt], tags=["rest"])
async def get_rest():
    conn = await get_db()
    rows = await conn.fetch("SELECT id, name, adress FROM restaraunts")
    await conn.close()
    return [Restaraunt(**dict(row)) for row in rows]

@app.post("/rest/post", response_model=Restaraunt, tags=["rest"])
async def post_rest(rest_: Restaraunt):
    conn = await get_db()
    row = await conn.fetchrow(
        """
        INSERT INTO restaraunts (id, name, adress)
        VALUES ($1, $2, $3)
        RETURNING id, name, adress;
        """,
        rest_.id, rest_.name, rest_.adress
    )
    await conn.close()
    return Restaraunt(**dict(row))

@app.get("/restaurants/{id}/menu/", tags=["rest"])
async def get_menu(id_: int):
    conn = await get_db()
    row_rest = await conn.fetchrow("SELECT name FROM restaraunts WHERE id = $1;", id_)
    row_chef = await conn.fetch("SELECT name FROM chefs WHERE restaraunt_id = $1;", id_)
    row_pizza = await conn.fetch("SELECT id, name, cheese, height, ingr, secret, restaraunt_id FROM pizzas WHERE restaraunt_id = $1;", id_)
    await conn.close()
    return [row_rest, row_chef, row_pizza]

@app.get("/chef", response_model=list[chef], tags=["chef"])
async def get_chef():
    conn = await get_db()
    rows = await conn.fetch("SELECT id, name, restaraunt_id FROM chefs")
    await conn.close()
    return [chef(**dict(row)) for row in rows]

@app.post("/chef/post", response_model=chef, tags=["chef"])
async def post_chef(chef_: chef):
    conn = await get_db()
    row = await conn.fetchrow(
        """
        INSERT INTO chefs (id, name, restaraunt_id)
        VALUES ($1, $2, $3)
        RETURNING id, name, restaraunt_id;
        """,
        chef_.id, chef_.name, chef_.restaraunt_id
    )
    await conn.close()
    return chef(**dict(row))


@app.get("/pizza", response_model=list[pizza], tags=["pizza"])
async def get_pizza():
    conn = await get_db()
    rows = await conn.fetch("SELECT id, name, cheese, height, ingr, secret, restaraunt_id FROM pizzas")
    await conn.close()
    return [pizza(**dict(row)) for row in rows]

@app.get("/ingredients/{id_}", tags=["pizza"])
async def get_ingr(id_: int):
    conn = await get_db()
    row = await conn.fetch("SELECT name, ingr FROM pizzas WHERE id = $1", id_)
    await conn.close()
    return (row)

@app.post("/pizza/post", response_model=pizza, tags=["pizza"])
async def post_pizza(pizza_: pizza):
    conn = await get_db()
    row = await conn.fetchrow(
        """
        INSERT INTO pizzas (id, name, cheese, height, ingr, secret, restaraunt_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, name, cheese, height, ingr, secret, restaraunt_id;
        """,
        pizza_.id, pizza_.name, pizza_.cheese, pizza_.height, pizza_.ingr, pizza_.secret, pizza_.restaraunt_id
    )
    await conn.close()
    return pizza(**dict(row))

@app.put("/pizza/put/{id}", response_model=pizza, tags=["pizza"])
async def put_pizza(pizza_: pizza, id_: int):
    conn = await get_db()
    row = await conn.fetchrow(
        """
        UPDATE pizzas
        SET 
            name = COALESCE($2, name),
            cheese = COALESCE($3, cheese),
            height = COALESCE($4, height),
            ingr = COALESCE($5, ingr),
            secret = COALESCE($6, secret),
            restaraunt_id = COALESCE($7, restaraunt_id)
        WHERE id = $1
        RETURNING id, name, cheese, height, ingr, secret, restaraunt_id;
        """,
        id_, pizza_.name, pizza_.cheese, pizza_.height, pizza_.ingr, pizza_.secret, pizza_.restaraunt_id
    )
    await conn.close()
    return pizza(**dict(row))


@app.delete("/pizza/delete/{id_}", response_model=list[pizza], tags=["pizza"])
async def del_pizza(id_: int):
    conn = await get_db()
    rows = await conn.fetch("DELETE FROM pizzas WHERE id = $1", id_)
    await conn.close()
    return [pizza(**dict(row)) for row in rows]


@app.get("/review", response_model=list[review], tags=["reviews"])
async def get_review():
    conn = await get_db()
    rows = await conn.fetch("SELECT id, restaraunt_id, rate, text FROM reviews")
    await conn.close()
    return [review(**dict(row)) for row in rows]

@app.post("/review/post", response_model=review, tags=["reviews"])
async def post_review(review_: review):
    conn = await get_db()
    row = await conn.fetchrow(
        """
        INSERT INTO reviews (id, restaraunt_id, rate, text)
        VALUES ($1, $2, $3, $4)
        RETURNING id, restaraunt_id, rate, text;
        """,
        review_.id, review_.restaraunt_id, review_.rate, review_.text
    )
    await conn.close()
    return review(**dict(row))

