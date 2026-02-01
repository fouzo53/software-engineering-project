from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    """Tạo response thành công chuẩn"""
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code


def error_response(message="Error", status_code=400):
    """Tạo response lỗi chuẩn"""
    response = {
        "status": "error",
        "message": message
    }
    
    return jsonify(response), status_code
