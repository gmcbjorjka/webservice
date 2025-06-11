from flask import request
from app import mongo, response
from app.model.pelabuhan import Pelabuhan
from bson import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
import os

# --- READ All
def index():
    try:
        pelabuhans = mongo.db.pelabuhan.find()
        data = formatarray(pelabuhans)
        return response.success(data, "Berhasil mengambil data pelabuhan")
    except Exception as e:
        print(e)
        return response.error([], "Gagal mengambil data pelabuhan")

# --- CREATE
def save():
    try:
        nama_pelabuhan = request.form.get('nama_pelabuhan')
        description = request.form.get('description')
        location = request.form.get('location')
        rating = request.form.get('rating')
        facilities = request.form.getlist('facilities')  # list dari form-data
        article = request.form.get('article')
        file = request.files.get('image')  # key: image

        if not all([nama_pelabuhan, description, location, rating, facilities, article, file]):
            return response.error([], "Semua field harus diisi")

        filename = secure_filename(nama_pelabuhan.lower().replace(" ", "_") + os.path.splitext(file.filename)[1])
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
        file.save(filepath)

        pelabuhan = Pelabuhan(
            nama_pelabuhan,
            filename,
            description,
            location,
            float(rating),
            facilities,
            article
        )

        inserted = mongo.db.pelabuhan.insert_one(pelabuhan.to_dict())
        return response.success({"id": str(inserted.inserted_id)}, "Berhasil menambah pelabuhan")
    except Exception as e:
        print(e)
        return response.error([], "Gagal menambah pelabuhan")

# --- UPDATE
def update(id):
    try:
        data = request.get_json()
        required_fields = ['nama_pelabuhan', 'image', 'description', 'location', 'rating', 'facilities', 'article']

        if not all(data.get(field) for field in required_fields):
            return response.error([], "Semua field harus diisi")

        update_data = {
            "nama_pelabuhan": data['nama_pelabuhan'],
            "image": data['image'],
            "description": data['description'],
            "location": data['location'],
            "rating": float(data['rating']),
            "facilities": data['facilities'],
            "article": data['article'],
            "updated_at": datetime.utcnow()
        }

        mongo.db.pelabuhan.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return response.success({"id": id}, "Berhasil mengupdate pelabuhan")
    except Exception as e:
        print(e)
        return response.error([], "Gagal mengupdate pelabuhan")

# --- DELETE
def delete(id):
    try:
        pelabuhan = mongo.db.pelabuhan.find_one({"_id": ObjectId(id)})
        if not pelabuhan:
            return response.error([], "Pelabuhan tidak ditemukan")

        # Hapus file gambar
        gambar_path = os.path.join(os.getenv("UPLOAD_FOLDER"), pelabuhan["image"])
        if os.path.exists(gambar_path):
            os.remove(gambar_path)

        mongo.db.pelabuhan.delete_one({"_id": ObjectId(id)})
        return response.success([], "Berhasil menghapus pelabuhan")
    except Exception as e:
        print(e)
        return response.error([], "Gagal menghapus pelabuhan")

# --- FORMAT Helpers
def formatarray(datas):
    return [singleObject(data) for data in datas]

def singleObject(data):
    return {
        "id": str(data['_id']),
        "nama_pelabuhan": data['nama_pelabuhan'],
        "image": data['image'],
        "description": data['description'],
        "location": data['location'],
        "rating": data['rating'],
        "facilities": data['facilities'],
        "article": data['article'],
        "created_at": data['created_at'],
        "updated_at": data['updated_at']
    }
