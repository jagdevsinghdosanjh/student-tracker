# app/utils/image_handler.py

from gridfs import GridFS
from bson.objectid import ObjectId
from flask import current_app

def save_image(file):
    fs = GridFS(current_app.mongo.db)
    return fs.put(file, filename=file.filename)

def get_image(photo_id):
    fs = GridFS(current_app.mongo.db)
    try:
        image = fs.get(ObjectId(photo_id))
        return image.read(), image.content_type, image.filename
    except:
        return None, None, None

def delete_image(photo_id):
    fs = GridFS(current_app.mongo.db)
    try:
        fs.delete(ObjectId(photo_id))
        return True
    except:
        return False
