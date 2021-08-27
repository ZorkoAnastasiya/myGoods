import my_function
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel


app = FastAPI()

filename = 'my_goods.csv'


class GoodsArgs(BaseModel):
    name: str
    price: float
    quantity: int
    
    
@app.post('/add')
async def add_goods(
        args: GoodsArgs,
        request: Request,
        response: Response
):
    list_args = [args.name, args.price, args.quantity]
    user = my_function.get_user(request) or my_function.get_random_name()
    response.set_cookie("user", user)

    return my_function.csv_writer(filename, list_args, user)


@app.get('/add/{name}/{price}/{quantity}')
async def add_goods(
        name: str,
        price: float,
        quantity: int,
        request: Request,
        response: Response
):
    list_args = [name, price, quantity]
    user = my_function.get_user(request) or my_function.get_random_name()
    response.set_cookie("user", user)

    return my_function.csv_writer(filename, list_args, user)


@app.get('/read')
async def read_file(request: Request):
    user = my_function.get_user(request)

    return my_function.csv_reader(filename, user)


@app.get('/delete/{name}')
async def del_goods(name: str, request: Request):
    user = my_function.get_user(request)

    return my_function.deletion_goods(filename, name, user)


@app.get('/sum')
async def sum_price(request: Request):
    user = my_function.get_user(request)

    return my_function.sum_goods(filename, user)


@app.get('/max')
async def max_price_goods(request: Request):
    user = my_function.get_user(request)

    return my_function.max_price(filename, user)


@app.get('/min')
async def min_price_goods(request: Request):
    user = my_function.get_user(request)

    return my_function.min_price(filename, user)


@app.get('/quantity/{name}/{quantity}/{effect}')
async def change(
        name: str,
        quantity: int,
        effect: str,
        request: Request
):
    user = my_function.get_user(request)

    return my_function.change_quantity(filename, name, quantity, effect, user)
