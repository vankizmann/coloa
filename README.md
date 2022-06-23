# Coloa Image Resize/Crop/Focuspoint API with Compression and YOLOv5 Object Detection

Start webserver with:

```uvicorn main:app --reload```
<br>
<br>
# How use API:

### *http://127.0.0.1:8000/(crop|size)*
The run command just returns a plain image with given query.
<br>
<br>
```.../size?url=https://source.unsplash.com/random&size=600,auto```
```.../crop?url=https://source.unsplash.com/random&size=600,600```

*Image with 600px width and auto/600 height*
<br>
<br>
```.../size?url=https://source.unsplash.com/random```

*Same dimension but with image compression*
<br>
<br>
### *http://127.0.0.1:8000/get*
The get command returns a application/json with new Imageurls and focus point.
<br>
<br>
```.../get?url=https://source.unsplash.com/random&size=1280,720&size=720,1280```

*Crop/Resize with given sizes and focus on center. Returns json:*

```json
{
  "urls": {
    "1280-720": "http://...(landscape)",
    "720-1280": "http://...(portrait)"
  },
  "focus": {
    "x": 0.5, "y": 0.5
  }
}
```
<br>

```.../get?url=https://source.unsplash.com/random&size=1280,720&size=720,1280&focus=0.75,0.25```

*Crop/Resize with given sizes and focus on Right-Top. Returns json:*

```json
{
  "urls": {
    "1280-720": "http://...(landscape)",
    "720-1280": "http://...(portrait)"
  },
  "focus": {
    "x": 0.75, "y": 0.25
  }
}
```
<br>

```.../get?url=https://source.unsplash.com/random&size=1280,720&size=720,1280&detect=1```

*Crop/Resize with given sizes and focus on Left-Bottom (Detected by YOLOv5 Object Detection). Returns json:*

```json
{
  "urls": {
    "1280-720": "http://...(landscape)",
    "720-1280": "http://...(portrait)"
  },
  "focus": {
    "x": 0.2,
    "y": 0.8
  },
  "tags": [
    { "label": "person","rate": 0.1,"xpos": 0.9,"ypos": 0.5 }
  ],
  "yolo": "http://...(landscape)"
}
```
