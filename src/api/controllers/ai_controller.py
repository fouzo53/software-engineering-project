from flask import Blueprint, request, jsonify, g
import os
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
from src.infrastructure.services.ai_service import AIService
from src.api.middleware import token_required, staff_required

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@ai_bp.route('/parse-order', methods=['POST'])
@staff_required
def parse_order(ai_service: AIService):
    """
    Phân tích câu lệnh bán hàng bằng AI
    ---
    tags:
      - AI
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              description: Câu lệnh bán hàng bằng tiếng Việt tự nhiên
              example: "Bán 5 bao xi măng cho anh Nam nợ nhé"
    responses:
      200:
        description: Phân tích thành công, trả về đơn hàng nháp
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            draft_id:
              type: integer
              description: ID đơn hàng nháp (dùng để confirm sau)
              example: 1
            items:
              type: array
              description: Danh sách sản phẩm đã phân tích
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                    description: ID sản phẩm (null nếu không tìm thấy)
                    example: 1
                  product_name:
                    type: string
                    example: "Xi măng Hoàng Thạch"
                  quantity:
                    type: integer
                    example: 5
                  price:
                    type: number
                    example: 120000
                  subtotal:
                    type: number
                    example: 600000
                  error:
                    type: string
                    description: Thông báo lỗi nếu không tìm thấy sản phẩm
            customer:
              type: object
              description: Thông tin khách hàng (nếu tìm thấy)
              properties:
                customer_id:
                  type: integer
                  example: 1
                customer_name:
                  type: string
                  example: "Anh Nam"
                phone:
                  type: string
                  example: "0123456789"
                debt_amount:
                  type: number
                  example: 500000
                found:
                  type: boolean
                  description: true nếu tìm thấy trong hệ thống
                message:
                  type: string
                  description: Thông báo nếu chưa có trong hệ thống
            payment_method:
              type: string
              enum: [CASH, DEBT]
              description: Phương thức thanh toán (DEBT nếu có từ "nợ", "trả sau")
              example: "DEBT"
            total_amount:
              type: number
              description: Tổng tiền đơn hàng
              example: 600000
            message:
              type: string
              example: "Đã phân tích thành công. Kiểm tra và xác nhận đơn hàng."
      400:
        description: Lỗi khi phân tích
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "Vui lòng nhập câu lệnh bán hàng"}), 400
        
        result = ai_service.parse_order_text(text)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify({"message": result.get('message', 'Lỗi khi phân tích')}), 400
            
    except Exception as e:
        return jsonify({"error": f"Lỗi: {str(e)}"}), 500


@ai_bp.route('/confirm-draft/<int:draft_id>', methods=['POST'])
@staff_required
def confirm_draft(draft_id: int, ai_service: AIService):
    """
    Xác nhận chuyển đơn nháp thành đơn hàng thật
    ---
    tags:
      - AI
    security:
      - Bearer: []
    parameters:
      - in: path
        name: draft_id
        type: integer
        required: true
        description: ID đơn hàng nháp (lấy từ API /api/ai/parse-order)
        example: 1
    responses:
      200:
        description: Tạo đơn hàng thành công
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            order_id:
              type: integer
              description: ID đơn hàng thật đã được tạo
              example: 10
            total:
              type: number
              description: Tổng tiền đơn hàng
              example: 600000
            payment_method:
              type: string
              enum: [CASH, DEBT]
              example: "DEBT"
            message:
              type: string
              example: "Đã tạo đơn hàng thành công!"
      400:
        description: Lỗi khi tạo đơn hàng
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Không tìm thấy đơn nháp"
      404:
        description: Không tìm thấy đơn nháp
    """
    try:
        user_id = request.current_user.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        result = ai_service.confirm_draft_order(draft_id, user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify({"message": result.get('message', 'Lỗi khi tạo đơn hàng')}), 400
            
    except Exception as e:
        return jsonify({"error": f"Lỗi: {str(e)}"}), 500


@ai_bp.route('/parse-voice-order', methods=['POST'])
@staff_required
def parse_voice_order(ai_service: AIService):
    """
    Phân tích đơn hàng qua giọng nói
    """
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "Không tìm thấy file âm thanh"}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({"error": "File âm thanh không hợp lệ"}), 400
        
        # Lưu tạm file để xử lý
        upload_folder = 'src/uploads/temp'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Gọi service để xử lý
        result = ai_service.parse_audio_order(filepath)
        
        # Xóa file sau khi xử lý xong (tùy chọn)
        # os.remove(filepath)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify({"message": result.get('message', 'Lỗi khi phân tích giọng nói')}), 400
            
    except Exception as e:
        return jsonify({"error": f"Lỗi: {str(e)}"}), 500

