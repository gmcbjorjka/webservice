from flask import request
from app import mongo, response

from app.model.dosen import Dosen
from bson import ObjectId

# --- READ All
def index():
    try:
        dosens = mongo.db.dosen.find()
        data = formatarray(dosens)
        return response.success(data, "Success mengambil data dosen")
    except Exception as e:
        print(e)
        return response.error([], "Error mengambil data dosen")

# --- CREATE
def save():
    data = request.get_json()
    try:
        nidn = data.get('nidn')
        nama = data.get('nama')
        phone = data.get('phone')
        alamat = data.get('alamat')

        if not nidn or not nama or not phone or not alamat:
            return response.error([], "Semua field harus diisi")

        dosen = Dosen(nidn, nama, phone, alamat)
        inserted = mongo.db.dosen.insert_one(dosen.to_dict())

        return response.success({"id": str(inserted.inserted_id)}, "Berhasil menambah dosen")
    except Exception as e:
        print(e)
        return response.error([], "Gagal menambah dosen")

# --- FORMAT Helpers
def formatarray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array

def singleObject(data):
    return {
        "id": str(data['_id']),
        "nidn": data['nidn'],
        "nama": data['nama'],
        "phone": data['phone'],
        "alamat": data['alamat']
    }
