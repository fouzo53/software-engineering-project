
from flask import Blueprint, request, jsonify
from src.api.middleware import token_required, owner_required
from src.services.subscription_service import SubscriptionService
from src.infrastructure.databases.database import db

subscription_bp = Blueprint('subscription', __name__, url_prefix='/api/subscription')
subscription_service = SubscriptionService()

@subscription_bp.route('/plans', methods=['GET'])
def get_plans():
    """
    Get all subscription plans
    """
    return jsonify(subscription_service.get_plans()), 200

@subscription_bp.route('/current', methods=['GET'])
@token_required
def get_current_subscription():
    """
    Get current user's subscription details
    """
    from src.infrastructure.models.user_model import UserModel
    user_id = request.current_user['user_id']
    user = UserModel.query.get(user_id)
    
    plan_key = user.subscription or "basic"
    plan = subscription_service.get_plans().get(plan_key, subscription_service.get_plans()["basic"])
    
    return jsonify({
        "plan": plan_key,
        "details": plan
    }), 200

@subscription_bp.route('/upgrade', methods=['POST'])
@owner_required
def upgrade_subscription():
    """
    Upgrade subscription plan
    """
    from src.infrastructure.models.user_model import UserModel
    data = request.get_json()
    plan_key = data.get('plan')
    
    try:
        user_id = request.current_user['user_id']
        user = UserModel.query.get(user_id)
        
        subscription_service.upgrade_subscription(user, plan_key)
        db.session.commit()
        return jsonify({"success": True, "message": f"Upgraded to {plan_key}"}), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
