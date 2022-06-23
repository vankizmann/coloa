from typing import List, Union
from fastapi import FastAPI, Query
from lib.router import Router

app = FastAPI()

@app.get('/get')
def route_get(url: Union[str], detect: Union[bool] = False, focus: Union[str, None] = None, size: Union[List[str], None] = Query(default=None)):
    return Router.get(url, focus, size, detect)

@app.get('/size')
def route_size(url: Union[str], size: Union[str, None] = None):
    return Router.size(url, size)

@app.get('/crop')
def route_crop(url: Union[str], size: Union[str, None] = None, focus: Union[str, None] = None):
    return Router.crop(url, size, focus)