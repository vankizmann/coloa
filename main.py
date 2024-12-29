from typing import List, Union
from fastapi import FastAPI, Query, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from lib.router import Router

app = FastAPI()

# app.add_middleware(GZipMiddleware, minimum_size=100)

@app.post('/get')
def route_get(file: UploadFile, detect: Union[bool] = False, focus: Union[str, None] = None, size: Union[List[str], None] = Query(default=None)):
    return Router.get(file, focus, size, detect)

@app.get('/get')
def route_get(url: Union[str], detect: Union[bool] = False, focus: Union[str, None] = None, size: Union[List[str], None] = Query(default=None)):
    return Router.get(url, focus, size, detect)

@app.post('/size')
def route_size(file: UploadFile, size: Union[str, None] = None):
    return Router.size(file, size)

@app.get('/size')
def route_size(url: Union[str], size: Union[str, None] = None):
    return Router.size(url, size)

@app.post('/crop')
def route_crop(file: UploadFile, size: Union[str, None] = None, focus: Union[str, None] = None):
    return Router.crop(file, size, focus)

@app.get('/crop')
def route_crop(url: Union[str], size: Union[str, None] = None, focus: Union[str, None] = None):
    return Router.crop(url, size, focus)

@app.get('/webp')
def route_crop(url: Union[str], quality: Union[int, None] = 100):
    return Router.webp(url, quality)

@app.post('/webp')
def route_crop(file: UploadFile, quality: Union[int, None] = 100):
    return Router.webp(file, quality)
    
app.mount("/static", StaticFiles(directory="static"), name="static")

