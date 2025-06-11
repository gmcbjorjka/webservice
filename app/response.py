from flask import jsonify, make_response

def success(values, message="Berhasil"):
    res = {
        'success': True,
        'data': values,
        'message': message
    }
    return make_response(jsonify(res)), 200

def error(values=None, message="Terjadi kesalahan pada server", status_code=500):
    res = {
        'success': False,
        'data': values or [],
        'message': message
    }
    return make_response(jsonify(res)), status_code


def unauthorized(values=None, message="Tidak diizinkan"):
    res = {
        'data': values or [],
        'message': message
    }
    return make_response(jsonify(res)), 401

def forbidden(values=None, message="Akses ditolak"):
    res = {
        'data': values or [],
        'message': message
    }
    return make_response(jsonify(res)), 403

def notFound(values=None, message="Data tidak ditemukan"):
    res = {
        'data': values or [],
        'message': message
    }
    return make_response(jsonify(res)), 404

def error(values=None, message="Terjadi kesalahan pada server", status_code=500):
    res = {
        'data': values or [],
        'message': message
    }
    return make_response(jsonify(res)), status_code
