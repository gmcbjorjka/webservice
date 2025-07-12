from app import app
from app.controller import DosenController,ArtikelController,PelabuhanController, UserController,OAuthController,PostController
from flask import Flask, request, jsonify, send_from_directory
import os
from config import Config
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.api_service import require_api_key
from app import mongo
from bson import ObjectId
from app import response 
from datetime import datetime
from werkzeug.utils import secure_filename






@app.route('/')
def index():
    return 'hello flask app'

@app.route('/post', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'GET':
        return PostController.get_posts()
    elif request.method == 'POST':
        return PostController.create_post()

@app.route('/posts/<post_id>/komentar', methods=['POST'])
def handle_comment(post_id):
    return PostController.add_comment(post_id)


@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    elif request.method == 'POST':
        return DosenController.save()

# --- Artikel Routes
@app.route('/artikel', methods=['GET', 'POST'])
def artikels():
    if request.method == 'GET':
        return ArtikelController.index()
    elif request.method == 'POST':
        return ArtikelController.save()

@app.route('/artikel/<id>', methods=['PUT', 'DELETE'])
def artikel_detail(id):
    if request.method == 'PUT':
        return ArtikelController.update(id)
    elif request.method == 'DELETE':
        return ArtikelController.delete(id)

@app.route('/pelabuhan', methods=['GET', 'POST'])
#@jwt_required()
#@require_api_key
def pelabuhans():
    if request.method == 'GET':
        return PelabuhanController.index()
    elif request.method == 'POST':
        return PelabuhanController.save()

@app.route('/pelabuhan/<id>', methods=['PUT', 'DELETE'])
def pelabuhan_detail(id):
    if request.method == 'PUT':
        return PelabuhanController.update(id)
    elif request.method == 'DELETE':
        return PelabuhanController.delete(id)

@app.route('/user/register', methods=['POST'])
def register_user():
    return UserController.register()

@app.route('/user/login', methods=['POST'])
def login_user():
    return UserController.login()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Looking for: {full_path}")  # Debug log
    if not os.path.exists(full_path):
        print("File not found")
        return jsonify({'error': 'File not found'}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Google OAuth Routes
@app.route('/login/google')
def login_google():
    return OAuthController.login_google()

@app.route('/auth/google')
def auth_google():
    return OAuthController.auth_google()

@app.route('/auth/google/flutter', methods=['POST'])
def auth_google_flutter_route():
    from app.controller.OAuthController import auth_google_flutter
    return auth_google_flutter()

@app.route('/user/forgot-password', methods=['POST'])
def forgot_password_route():
    return UserController.forgot_password()

@app.route('/user/reset-password', methods=['POST'])
def reset_password_route():
    return UserController.reset_password()


@app.route('/verify-email', methods=['GET'])
def verify_email_route():
    return UserController.verify_email()

@app.route('/user/login-history', methods=['GET'])
@jwt_required()
def get_login_history():
    try:
        user_id = get_jwt_identity()
        print(f"🔒 Get history for user_id: {user_id}")

        history = list(
            mongo.db.login_history.find({"user_id": ObjectId(user_id)}).sort("login_time", -1)
        )

        for h in history:
            h["_id"] = str(h["_id"])
            h["user_id"] = str(h["user_id"])
            h["login_time"] = h["login_time"].isoformat()
            h["device"] = h.get("device", "unknown")
            h["ip_address"] = h.get("ip_address", "-")

        return response.success(history, "Riwayat login ditemukan")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return response.badRequest([], f"Error: {str(e)}")

@app.route('/penimbangan', methods=['POST'])
@jwt_required()
def simpan_penimbangan():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validasi dasar
        weight = data.get("weight")
        count = data.get("count")
        fish_type = data.get("fish_type", "Tidak Diketahui")
        lokasi = data.get("lokasi", "Tidak Diketahui")
        created_at = data.get("created_at")

        if not weight or not count:
            return response.error([], "Weight dan count wajib diisi")

        mongo.db.penimbangan.insert_one({
            "user_id": ObjectId(user_id),
            "weight": weight,
            "count": count,
            "fish_type": fish_type,
            "lokasi": lokasi,
            "created_at": datetime.fromisoformat(created_at),
            "tanggal": datetime.fromisoformat(created_at).date().isoformat()
        })

        return response.success({}, "Penimbangan disimpan")
    except Exception as e:
        print(e)
        return response.error([], "Gagal menyimpan penimbangan")

@app.route("/penimbangan", methods=["GET"])
@jwt_required()
def get_penimbangan():
    try:
        user_id = get_jwt_identity()
        data = mongo.db.penimbangan.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)

        result = []
        for item in data:
            result.append({
                "id": str(item["_id"]),
                "weight": item.get("weight", 0),
                "count": item.get("count", 0),
                "fish_type": item.get("fish_type", ""),
                "lokasi": item.get("lokasi", ""),
                "tanggal": item.get("tanggal", ""),
                "created_at": item.get("created_at", "").isoformat() if item.get("created_at") else ""
            })

        return response.success(result, "Histori penimbangan berhasil diambil")
    except Exception as e:
        print(e)
        return response.error([], "Gagal mengambil histori penimbangan")

@app.route('/user/change-password', methods=['POST'])
def change_password_route():
    from app.controller.UserController import change_password
    return change_password()

@app.route('/user/upload-profile-picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    try:
        user_id = get_jwt_identity()
        print("✅ JWT user_id:", user_id)

        if not user_id:
            return response.error([], "User tidak ditemukan di JWT", 401)

        print("✅ Request form:", request.form)
        print("✅ Request files:", request.files)

        file = request.files.get('file')
        if not file or file.filename == '':
            return response.error([], "File tidak ditemukan atau kosong", 400)

        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()
        new_filename = f"{user_id}{ext}"

        upload_path = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_path, exist_ok=True)
        save_path = os.path.join(upload_path, new_filename)

        file.save(save_path)
        print(f"✅ File disimpan di: {save_path}")

        mongo.db.user.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"foto_profil": new_filename}}
        )

        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        user['id'] = str(user['_id'])
        user.pop('_id', None)
        user.pop('password', None)

        return response.success(user, "Foto profil berhasil diperbarui")
    except Exception as e:
        print("❌ Upload error:", e)
        return response.error([], f"Upload gagal: {str(e)}", 500)
    

@app.route('/user/update-name', methods=['POST'])
@jwt_required()
def update_name():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_name = data.get('nama', '').strip()

    print(f"🟢 user_id: {user_id}")
    print(f"🟢 request data: {data}")
    print(f"🟢 new_name: {new_name}")

    if not new_name:
        return jsonify(success=False, message="Nama tidak boleh kosong"), 400

    # ✅ PASTIKAN SAMA DENGAN UPLOAD!
    users = mongo.db.user

    try:
        filter_query = {'_id': ObjectId(user_id)}
    except:
        filter_query = {'_id': user_id}

    result = users.update_one(filter_query, {'$set': {'nama': new_name}})
    if result.matched_count == 0:
        filter_query = {'_id': user_id}
        result = users.update_one(filter_query, {'$set': {'nama': new_name}})

    print(f"🟢 matched_count: {result.matched_count}")
    print(f"🟢 modified_count: {result.modified_count}")

    if result.matched_count >= 1:
        updated_user = users.find_one(filter_query)
        return jsonify(success=True, data={'nama': updated_user['nama']}, message="Nama berhasil diperbarui"), 200
    else:
        return jsonify(success=False, message="User tidak ditemukan"), 400
