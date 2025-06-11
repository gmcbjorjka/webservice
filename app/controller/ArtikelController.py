from flask import request
from app import mongo, response
from app.model.artikel import Artikel
from bson import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
import os

# --- READ All
def index():
    try:
        artikels = mongo.db.artikel.find()
        data = formatarray(artikels)
        return response.success(data, "Berhasil mengambil data artikel")
    except Exception as e:
        print(e)
        return response.error([], "Gagal mengambil data artikel")

# --- CREATE
def save():
    try:
        judul = request.form.get('judul')
        isi = request.form.get('isi')
        penulis = request.form.get('penulis')
        file = request.files.get('gambar')

        if not judul or not isi or not penulis or not file:
            return response.error([], "Semua field harus diisi")

        filename = secure_filename(judul.lower().replace(" ", "_") + os.path.splitext(file.filename)[1])
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
        file.save(filepath)

        artikel = Artikel(judul, isi, filename, penulis)
        inserted = mongo.db.artikel.insert_one(artikel.to_dict())

        return response.success({"id": str(inserted.inserted_id)}, "Berhasil menambah artikel")
    except Exception as e:
        print(e)
        return response.error([], "Gagal menambah artikel")

# --- UPDATE
def update(id):
    try:
        if request.is_json:
            data = request.get_json()
            judul = data.get('judul')
            isi = data.get('isi')
            gambar = data.get('gambar')
            penulis = data.get('penulis')
        else:
            judul = request.form.get('judul')
            isi = request.form.get('isi')
            penulis = request.form.get('penulis')
            gambar = request.form.get('gambar') or (
                request.files.get('gambar').filename if request.files.get('gambar') else None
            )

        if not gambar:
            old = mongo.db.artikel.find_one({"_id": ObjectId(id)})
            if old:
                gambar = old.get('gambar')

        if not judul or not isi or not gambar or not penulis:
            return response.error([], "Semua field harus diisi")

        update_data = {
            "judul": judul,
            "isi": isi,
            "gambar": gambar,
            "penulis": penulis,
            "updated_at": datetime.utcnow()
        }

        mongo.db.artikel.update_one({"_id": ObjectId(id)}, {"$set": update_data})

        return response.success({"id": id}, "Berhasil mengupdate artikel")
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return response.error([], "Gagal mengupdate artikel")

# --- DELETE
def delete(id):
    try:
        artikel = mongo.db.artikel.find_one({"_id": ObjectId(id)})
        if not artikel:
            return response.error([], "Artikel tidak ditemukan")

        gambar_path = os.path.join(os.getenv("UPLOAD_FOLDER"), artikel["gambar"])
        if os.path.exists(gambar_path):
            os.remove(gambar_path)

        mongo.db.artikel.delete_one({"_id": ObjectId(id)})
        return response.success([], "Berhasil menghapus artikel")
    except Exception as e:
        print(e)
        return response.error([], "Gagal menghapus artikel")

# --- FORMAT Helpers
def formatarray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array

def singleObject(data):
    return {
        "id": str(data['_id']),
        "judul": data['judul'],
        "isi": data['isi'],
        "gambar": data['gambar'],
        "penulis": data.get('penulis', '-'),
        "created_at": data['created_at'],
        "updated_at": data['updated_at']
    }
