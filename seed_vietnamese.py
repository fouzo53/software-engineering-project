#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🌱 SCRIPT NẠP DỮ LIỆU TIẾNG VIỆT
================================
Tạo dữ liệu mẫu đầy đủ với tên tiếng Việt và hình ảnh thực tế.

Run: python seed_vietnamese.py
"""

import sys
import io
import random
from datetime import datetime, timedelta
import bcrypt

# Fix UTF-8 encoding on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from faker import Faker
except ImportError:
    print("❌ Cần cài đặt faker: pip install faker")
    sys.exit(1)

from src.create_app import create_app
from src.infrastructure.databases.database import db
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.models.product_model import ProductModel
from src.infrastructure.models.customer_model import CustomerModel, DebtTransactionModel
from src.infrastructure.models.order_model import OrderModel, OrderDetailModel

# Initialize Faker with Vietnamese locale
fake = Faker('vi_VN')

# ============================================================================
# IMAGE MAPPING BY CATEGORY
# ============================================================================
CATEGORY_IMAGES = {
    "Vật liệu xây dựng": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=200",
    "Sơn & Hóa chất": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=200",
    "Điện & Nước": "https://images.unsplash.com/photo-1605619869572-101140306385?w=200",
    "Dụng cụ cầm tay": "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=200",
    "Thiết bị vệ sinh": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=200",
}

# ============================================================================
# VIETNAMESE PRODUCT DATA
# ============================================================================
CATEGORIES_DATA = {
    "Vật liệu xây dựng": [
        ("Xi măng Hà Tiên PCB40", 95000, 85000),
        ("Xi măng Holcim", 98000, 88000),
        ("Xi măng INSEE", 92000, 82000),
        ("Cát xây tô (m³)", 350000, 300000),
        ("Cát san lấp (m³)", 180000, 150000),
        ("Đá 1x2 (m³)", 420000, 380000),
        ("Đá mi (m³)", 250000, 210000),
        ("Gạch ống 4 lỗ", 1200, 1000),
        ("Gạch thẻ 6 lỗ", 1500, 1300),
        ("Gạch block 15x20x40", 8500, 7500),
        ("Gạch men 40x40 Viglacera", 65000, 55000),
        ("Gạch granite 60x60", 125000, 105000),
        ("Thép Pomina phi 10", 185000, 165000),
        ("Thép Pomina phi 12", 220000, 195000),
        ("Thép Việt Nhật phi 14", 250000, 220000),
        ("Lưới B40 cuộn 45m", 850000, 750000),
    ],
    "Sơn & Hóa chất": [
        ("Sơn Dulux ngoài trời 5L", 750000, 650000),
        ("Sơn Dulux trong nhà 5L", 680000, 580000),
        ("Sơn Jotun Essence 5L", 820000, 720000),
        ("Sơn Nippon Matex 5L", 550000, 480000),
        ("Sơn lót chống kiềm 5L", 420000, 360000),
        ("Sơn chống thấm Sika 5kg", 380000, 320000),
        ("Sơn chống thấm Kova 5kg", 340000, 290000),
        ("Bột trét tường Spec", 125000, 105000),
        ("Bột trét Dulux", 180000, 155000),
        ("Keo dán gạch Davco 25kg", 165000, 140000),
    ],
    "Điện & Nước": [
        ("Ống nhựa Bình Minh phi 21", 28000, 24000),
        ("Ống nhựa Bình Minh phi 27", 38000, 32000),
        ("Ống nhựa Bình Minh phi 60", 95000, 82000),
        ("Ống nhựa Tiền Phong phi 27", 35000, 30000),
        ("Dây điện Cadivi 1.5mm (100m)", 450000, 400000),
        ("Dây điện Cadivi 2.5mm (100m)", 720000, 650000),
        ("Dây điện Cadivi 4mm (100m)", 1150000, 1050000),
        ("Công tắc Panasonic", 45000, 38000),
        ("Ổ cắm đôi Panasonic", 95000, 82000),
        ("Bóng đèn Rạng Đông 9W", 35000, 28000),
        ("Bóng đèn Rạng Đông 12W", 45000, 38000),
        ("Đèn LED ốp trần 18W", 125000, 105000),
    ],
    "Thiết bị vệ sinh": [
        ("Bồn cầu TOTO 1 khối", 4500000, 4000000),
        ("Bồn cầu Viglacera", 2200000, 1900000),
        ("Lavabo TOTO chân dài", 1850000, 1650000),
        ("Lavabo Viglacera", 850000, 720000),
        ("Vòi sen tắm Inax", 1250000, 1100000),
        ("Vòi lavabo Inax", 650000, 560000),
        ("Chậu rửa inox 2 hố", 750000, 650000),
        ("Gương phòng tắm 45x60", 280000, 240000),
    ],
    "Dụng cụ cầm tay": [
        ("Máy khoan Bosch GSB 10", 1250000, 1100000),
        ("Máy khoan Makita HP1630", 1450000, 1300000),
        ("Máy mài góc Bosch", 850000, 750000),
        ("Máy cắt gạch Makita", 2850000, 2500000),
        ("Búa đóng đinh 500g", 85000, 72000),
        ("Kìm cắt Stanley", 125000, 105000),
        ("Bộ tuốc nơ vít 6 món", 145000, 120000),
        ("Thước cuộn 5m", 45000, 38000),
        ("Thước thủy 60cm", 125000, 105000),
        ("Bay xây inox", 55000, 45000),
        ("Rulo lăn sơn 7 inch", 65000, 55000),
    ],
}


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def main():
    print("\n" + "=" * 60)
    print("🌱 NẠP DỮ LIỆU TIẾNG VIỆT - BIZFLOW")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        # =============================================
        # RESET DATABASE
        # =============================================
        print("\n🗑️  Reset database...")
        db.drop_all()
        db.create_all()
        print("   ✓ Database đã được reset")
        
        # =============================================
        # CREATE USERS
        # =============================================
        print("\n👤 Tạo tài khoản...")
        
        # Owner (Chủ cửa hàng)
        admin = UserModel(
            username="admin",
            password_hash=hash_password("123456"),
            full_name="Nguyễn Quản Lý",
            role="owner",
            status="active",
            subscription="premium"
        )
        db.session.add(admin)
        print("   ✓ Owner: admin / 123456 (Nguyễn Quản Lý)")
        
        # Employee (Nhân viên)
        staff = UserModel(
            username="staff",
            password_hash=hash_password("123456"),
            full_name="Trần Nhân Viên",
            role="employee",
            status="active",
            subscription="basic"
        )
        db.session.add(staff)
        print("   ✓ Employee: staff / 123456 (Trần Nhân Viên)")
        
        db.session.commit()
        
        # =============================================
        # CREATE CATEGORIES & PRODUCTS
        # =============================================
        print("\n📦 Tạo danh mục và sản phẩm...")
        
        all_products = []
        total_products = 0
        
        for cat_name, products_list in CATEGORIES_DATA.items():
            # Create category
            category = CategoryModel(name=cat_name)
            db.session.add(category)
            db.session.flush()
            
            # Get image for this category
            image_url = CATEGORY_IMAGES.get(cat_name, "https://placehold.co/200x200?text=Product")
            
            # Create products
            for prod_name, price, cost_price in products_list:
                product = ProductModel(
                    name=prod_name,
                    price=float(price),
                    cost_price=float(cost_price),
                    stock=random.randint(50, 500),
                    category_id=category.id,
                    image_url=image_url
                )
                db.session.add(product)
                all_products.append(product)
                total_products += 1
            
            print(f"   ✓ {cat_name}: {len(products_list)} sản phẩm")
        
        db.session.commit()
        print(f"   📊 Tổng: {total_products} sản phẩm")
        
        # =============================================
        # CREATE CUSTOMERS
        # =============================================
        print("\n👥 Tạo khách hàng...")
        
        customers = []
        for i in range(20):
            customer = CustomerModel(
                name=fake.name(),
                phone=fake.phone_number().replace(" ", "")[:11],
                address=fake.address().replace("\n", ", "),
                debt_amount=0.0,
                created_at=datetime.now() - timedelta(days=random.randint(1, 90))
            )
            db.session.add(customer)
            customers.append(customer)
        
        db.session.commit()
        
        # Add debt to 5 random customers
        debt_customers = random.sample(customers, 5)
        for customer in debt_customers:
            debt = random.choice([500000, 1000000, 1500000, 2000000, 3000000])
            customer.debt_amount = float(debt)
            
            transaction = DebtTransactionModel(
                customer_id=customer.id,
                transaction_type="debt",
                amount=float(debt),
                note=f"Công nợ đơn hàng {fake.date_this_month().strftime('%d/%m/%Y')}",
                created_at=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            db.session.add(transaction)
        
        db.session.commit()
        print(f"   ✓ Đã tạo 20 khách hàng (5 có công nợ)")
        
        # =============================================
        # CREATE ORDERS (30 orders in past 30 days)
        # =============================================
        print("\n🧾 Tạo đơn hàng...")
        
        users = [admin, staff]
        orders_count = 0
        details_count = 0
        total_revenue = 0
        
        for i in range(30):
            # Random date in past 30 days
            order_date = datetime.now() - timedelta(
                days=random.randint(0, 29),
                hours=random.randint(8, 18),
                minutes=random.randint(0, 59)
            )
            
            order = OrderModel(
                user_id=random.choice(users).id,
                total_amount=0,
                created_at=order_date
            )
            db.session.add(order)
            db.session.flush()
            
            # Add 1-5 products to order
            num_items = random.randint(1, 5)
            order_products = random.sample(all_products, min(num_items, len(all_products)))
            
            order_total = 0
            for product in order_products:
                quantity = random.randint(1, 10)
                line_total = product.price * quantity
                order_total += line_total
                
                detail = OrderDetailModel(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(detail)
                details_count += 1
            
            order.total_amount = order_total
            total_revenue += order_total
            orders_count += 1
        
        db.session.commit()
        print(f"   ✓ Đã tạo {orders_count} đơn hàng, {details_count} chi tiết")
        print(f"   💰 Tổng doanh thu: {total_revenue:,.0f} VND")
        
        # =============================================
        # SUMMARY
        # =============================================
        print("\n" + "=" * 60)
        print("✅ NẠP DỮ LIỆU THÀNH CÔNG!")
        print("=" * 60)
        print(f"""
📊 THỐNG KÊ:
   • Tài khoản:    2 (admin + staff)
   • Danh mục:     {len(CATEGORIES_DATA)} danh mục
   • Sản phẩm:     {total_products} sản phẩm (có hình ảnh)
   • Khách hàng:   20 khách hàng
   • Đơn hàng:     {orders_count} đơn hàng

🔐 ĐĂNG NHẬP:
   • admin / 123456 → Nguyễn Quản Lý (Chủ cửa hàng)
   • staff / 123456 → Trần Nhân Viên (Nhân viên)

🌐 Truy cập: http://localhost:3000
""")


if __name__ == "__main__":
    main()
