from app import app
from app.controller import DosenController,ArtikelController,PelabuhanController, UserController,OAuthController,PostController
from flask import Flask, request, jsonify, send_from_directory
import os
from config import Config
from flask_jwt_extended import jwt_required
from app.api_service import require_api_key





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




