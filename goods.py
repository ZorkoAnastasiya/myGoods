import my_function
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
filename = 'my_goods.csv'


class GoodsArgs(BaseModel):
    name: str
    price: float
    quantity: int
    
    
@app.post('/add')
async def add_goods(args: GoodsArgs):
    list_args = [args.name, args.price, args.quantity]
    return my_function.csv_writer(filename, list_args)


@app.get('/add/{name}/{price}/{quantity}')
async def add_goods(name: str, price: float, quantity: int):
    list_args = [name, price, quantity]
    return my_function.csv_writer(filename, list_args)


@app.get('/read')
async def read_file():
    return my_function.csv_reader(filename)


@app.get('/delete/{name}')
async def del_goods(name: str):
    return my_function.deletion_goods(filename, name)


@app.get('/sum')
async def sum_price():
    result = my_function.sum_goods(filename)
    return {"Сумма стоимости товаров": result}


@app.get('/max')
async def max_price_goods():
    return my_function.max_price(filename)


@app.get('/min')
async def min_price_goods():
    return my_function.min_price(filename)


@app.get('/quantity/{name}/{quantity}/{effect}')
async def change(name: str, quantity: int, effect: str):
    return my_function.change_quantity(filename, name, quantity, effect)
