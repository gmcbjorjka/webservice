from flask import request
from bson import ObjectId
from datetime import datetime
from app import mongo, response

def is_valid_objectid(id_str):
    try:
        ObjectId(id_str)
        return True
    except:
        return False

def create_post():
    try:
        data = request.get_json()
        print("POST DATA:", data)

        konten = data.get("konten")
        user_id = data.get("user_id")

        if not konten or not user_id:
            return response.error([], "User ID dan konten harus diisi")

        if not is_valid_objectid(user_id):
            return response.error([], "User ID tidak valid")

        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        if not user:
            return response.error([], "User tidak ditemukan")

        post_data = {
            "user_id": user_id,
            "nama": user["nama"],
            "foto_profil": user.get("foto_profil", ""),
            "konten": konten,
            "created_at": datetime.utcnow(),
            "komentar": []
        }

        mongo.db.posts.insert_one(post_data)
        return response.success(post_data, "Post berhasil dibuat")

    except Exception as e:
        print("Error create_post:", e)
        return response.error([], "Gagal membuat post")

def get_posts():
    try:
        posts = list(mongo.db.posts.find().sort("created_at", -1))
        for post in posts:
            post["_id"] = str(post["_id"])
            post["created_at"] = post["created_at"].isoformat()
            for komentar in post.get("komentar", []):
                komentar["created_at"] = komentar["created_at"].isoformat()
        return response.success(posts, "List postingan")
    except Exception as e:
        print("Error get_posts:", e)
        return response.error([], "Gagal mengambil postingan")

def add_comment(post_id):
    try:
        data = request.get_json()
        komentar_text = data.get("komentar")
        user_id = data.get("user_id")

        if not komentar_text or not user_id:
            return response.error([], "User ID dan komentar wajib diisi")

        if not is_valid_objectid(user_id) or not is_valid_objectid(post_id):
            return response.error([], "ID tidak valid")

        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        if not user:
            return response.error([], "User tidak ditemukan")

        komentar = {
            "user_id": user_id,
            "nama": user["nama"],
            "foto_profil": user.get("foto_profil", ""),
            "komentar": komentar_text,
            "created_at": datetime.utcnow()
        }

        result = mongo.db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$push": {"komentar": komentar}}
        )

        if result.modified_count == 0:
            return response.error([], "Post tidak ditemukan")

        return response.success(komentar, "Komentar ditambahkan")

    except Exception as e:
        print("Error add_comment:", e)
        return response.error([], "Gagal menambahkan komentar")
