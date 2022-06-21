from typing import List, Union
from fastapi import FastAPI, Query
from lib.router import Router

app = FastAPI()

@app.get('/get')
def route_get(url: Union[str], detect: Union[bool] = False, focus: Union[str, None] = None, size: Union[List[str], None] = Query(default=None)):
    return Router.get(url, focus, size, detect)

@app.get('/run')
def route_run(url: Union[str], size: Union[str, None] = None):
    return Router.run(url, size)