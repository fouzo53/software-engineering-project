from flask import Blueprint, jsonify
from src.infrastructure.databases.database import db
from src.infrastructure.models.category_model import CategoryModel

category_bp = Blueprint('category', __name__, url_prefix='/api')


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Lấy danh sách danh mục
    ---
    tags:
      - Categories
    responses:
      200:
        description: Danh sách danh mục
    """
    categories = CategoryModel.query.all()
    return jsonify({
        "data": [
            {"id": cat.id, "name": cat.name}
            for cat in categories
        ]
    }), 200
