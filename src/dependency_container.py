from injector import Binder, singleton

from src.domain.interfaces.user_repository import IUserRepository
from src.domain.interfaces.product_repository import IProductRepository
from src.domain.interfaces.category_repository import ICategoryRepository
from src.domain.interfaces.customer_repository import ICustomerRepository

from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from src.infrastructure.repositories.category_repository_impl import CategoryRepositoryImpl
from src.infrastructure.repositories.customer_repository_impl import CustomerRepositoryImpl

from src.services.auth_service import AuthService
from src.services.product_service import ProductService
from src.services.order_service import OrderService
from src.services.report_service import ReportService
from src.services.customer_service import CustomerService
from src.services.employee_service import EmployeeService
from src.services.admin_service import AdminService
from src.infrastructure.services.ai_service import AIService


def configure(binder: Binder) -> None:
    # Bind repositories - Interface to Implementation
    binder.bind(IUserRepository, to=UserRepositoryImpl, scope=singleton)
    binder.bind(IProductRepository, to=ProductRepositoryImpl, scope=singleton)
    binder.bind(ICategoryRepository, to=CategoryRepositoryImpl, scope=singleton)
    binder.bind(ICustomerRepository, to=CustomerRepositoryImpl, scope=singleton)

    # Services don't need explicit binding - injector will create them automatically
    # Just ensure they are in singleton scope
    binder.bind(AuthService, scope=singleton)
    binder.bind(ProductService, scope=singleton)
    binder.bind(OrderService, scope=singleton)
    binder.bind(ReportService, scope=singleton)
    binder.bind(CustomerService, scope=singleton)
    binder.bind(EmployeeService, scope=singleton)
    binder.bind(AdminService, scope=singleton)
    binder.bind(AIService, scope=singleton)
