import reflex as rx
from typing import TypedDict, Literal, Optional, ClassVar
import csv
import io
import os
import uuid
import logging
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions


class Product(TypedDict):
    id: int
    name: str
    brand: str
    price: float
    image: str
    description: str
    colors: list[str]
    category: str
    discount_price: Optional[float]


class CartItem(TypedDict):
    product_id: int
    quantity: int
    color: str


from datetime import datetime

OrderStatus = Literal[
    "Pendiente",
    "Procesando",
    "Enviado",
    "Entregado",
    "Cancelado",
    "Revisión Solicitada",
]


class Order(TypedDict):
    id: int
    customer_email: str
    items: list[CartItem]
    total: float
    status: OrderStatus
    created_at: str


class DetailedCartItem(TypedDict):
    product: Product
    quantity: int
    subtotal: float
    color: str


class Transaction(TypedDict):
    id: str
    order_id: int
    type: Literal["Ingreso", "Egreso"]
    amount: float
    date: str
    description: str


class Transaction(TypedDict):
    id: str
    order_id: int
    type: Literal["Ingreso", "Egreso"]
    amount: float
    date: str
    description: str


class Notification(TypedDict):
    id: str
    message: str
    read: bool
    created_at: str


class AuthState(rx.State):
    ADMIN_EMAIL: ClassVar[str] = "gallardoclaudio98@gmail.com"
    USERS: ClassVar[dict[str, dict]] = {
        "user@example.com": {"password": "password123"},
        ADMIN_EMAIL: {"password": "admin"},
    }
    in_session: bool = False
    error_message: str = ""
    current_user_email: Optional[str] = None

    @rx.var
    def is_admin(self) -> bool:
        return self.current_user_email == self.ADMIN_EMAIL

    @rx.event
    def sign_up(self, form_data: dict):
        email = form_data["email"]
        password = form_data["password"]
        if email in self.USERS:
            self.error_message = "El correo ya está en uso."
            yield rx.toast.error(self.error_message)
            return
        self.USERS[email] = {"password": password}
        self.in_session = True
        self.current_user_email = email
        self.error_message = ""
        return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data["email"]
        password = form_data["password"]
        user_data = self.USERS.get(email)
        if user_data and user_data["password"] == password:
            self.in_session = True
            self.current_user_email = email
            self.error_message = ""
            return rx.redirect("/")
        else:
            self.error_message = "Correo o contraseña inválidos."
            yield rx.toast.error(self.error_message)

    @rx.event
    def sign_out(self):
        self.in_session = False
        self.current_user_email = None
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        if not self.in_session:
            return rx.redirect("/sign-in")

    @rx.event
    def check_admin(self):
        if not self.in_session:
            return rx.redirect("/sign-in")
        if not self.is_admin:
            yield rx.toast.error(
                "Acceso denegado. Se requieren privilegios de administrador."
            )
            return rx.redirect("/")

    def _get_google_flow(self) -> Flow | None:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        if not all([client_id, client_secret, redirect_uri]):
            return None
        client_config = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
            }
        }
        scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ]
        return Flow.from_client_config(
            client_config=client_config, scopes=scopes, redirect_uri=redirect_uri
        )

    @rx.event
    def initiate_google_oauth(self):
        flow = self._get_google_flow()
        if flow is None:
            return rx.toast.error(
                "Autenticación de Google no configurada. Por favor, configure las variables de entorno."
            )
        authorization_url, _ = flow.authorization_url(
            access_type="offline", prompt="consent"
        )
        return rx.redirect(authorization_url)

    @rx.event
    def handle_google_callback(self):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        flow = self._get_google_flow()
        if not client_id or flow is None:
            yield rx.toast.error(
                "Error en la configuración de autenticación de Google."
            )
            return rx.redirect("/sign-in")
        try:
            flow.fetch_token(authorization_response=str(self.router.page.raw_url))
            credentials = flow.credentials
            id_info = id_token.verify_oauth2_token(
                credentials.id_token, Request(), client_id
            )
            email = id_info.get("email")
            if not email:
                self.error_message = "No se pudo obtener el correo de Google."
                yield rx.toast.error(self.error_message)
                return rx.redirect("/sign-in")
            if email not in self.USERS:
                self.USERS[email] = {"password": None}
            self.in_session = True
            self.current_user_email = email
            self.error_message = ""
            yield rx.toast.success(f"¡Bienvenido {email}!")
            return rx.redirect("/")
        except Exception as e:
            logging.exception(f"Error de Google OAuth: {e}")
            self.error_message = "Ocurrió un error durante la autenticación con Google."
            yield rx.toast.error(self.error_message)
            return rx.redirect("/sign-in")


class MainState(rx.State):
    products: list[Product] = [
        {
            "id": 1,
            "name": "Pixel 8 Pro",
            "brand": "Google",
            "price": 999.0,
            "image": "/pixel8pro.png",
            "description": "El Pixel más potente hasta la fecha, con un sistema de cámara de nivel profesional.",
            "colors": ["Obsidian", "Porcelain", "Bay"],
            "category": "smartphone",
            "discount_price": 949.0,
        },
        {
            "id": 2,
            "name": "iPhone 15 Pro",
            "brand": "Apple",
            "price": 1099.0,
            "image": "/iphone15pro.png",
            "description": "Una bestia. Un nuevo diseño de titanio, más ligero y resistente.",
            "colors": [
                "Natural Titanium",
                "Blue Titanium",
                "White Titanium",
                "Black Titanium",
            ],
            "category": "smartphone",
            "discount_price": None,
        },
        {
            "id": 3,
            "name": "Galaxy S24 Ultra",
            "brand": "Samsung",
            "price": 1299.0,
            "image": "/s24ultra.png",
            "description": "Libera nuevos niveles de creatividad, productividad y posibilidades con Galaxy AI.",
            "colors": ["Titanium Gray", "Titanium Black", "Titanium Violet"],
            "category": "smartphone",
            "discount_price": 1199.0,
        },
        {
            "id": 4,
            "name": "OnePlus 12",
            "brand": "OnePlus",
            "price": 799.0,
            "image": "/oneplus12.png",
            "description": "Rendimiento de élite, de adentro hacia afuera. Una experiencia insignia de varias capas.",
            "colors": ["Silky Black", "Flowy Emerald"],
            "category": "smartphone",
            "discount_price": None,
        },
        {
            "id": 5,
            "name": "Xperia 1 V",
            "brand": "Sony",
            "price": 1399.0,
            "image": "/xperia1v.png",
            "description": "Sensor de última generación y procesamiento computacional para una calidad de imagen asombrosa.",
            "colors": ["Black", "Platinum Silver"],
            "category": "smartphone",
            "discount_price": None,
        },
        {
            "id": 6,
            "name": "Nothing Phone (2)",
            "brand": "Nothing",
            "price": 599.0,
            "image": "/nothingphone2.png",
            "description": "Una nueva forma de interactuar con un smartphone a través de una Interfaz Glyph rediseñada.",
            "colors": ["White", "Dark Gray"],
            "category": "smartphone",
            "discount_price": 549.0,
        },
        {
            "id": 7,
            "name": "MacBook Air M3",
            "brand": "Apple",
            "price": 1099.0,
            "image": "/macbookairm3.png",
            "description": "Potenciada por el chip M3, la MacBook Air de 13 pulgadas es una laptop sumamente portátil.",
            "colors": ["Space Gray", "Silver", "Starlight", "Midnight"],
            "category": "notebook",
            "discount_price": None,
        },
        {
            "id": 8,
            "name": "Dell XPS 15",
            "brand": "Dell",
            "price": 1499.0,
            "image": "/dellxps15.png",
            "description": "Pantalla impresionante, sonido envolvente y un diseño sofisticado.",
            "colors": ["Platinum", "Graphite"],
            "category": "notebook",
            "discount_price": 1399.0,
        },
        {
            "id": 9,
            "name": "Lenovo ThinkPad X1",
            "brand": "Lenovo",
            "price": 1599.0,
            "image": "/thinkpadx1.png",
            "description": "Ultraligero. ultrapotente. Ultra-evidente. Para el portátil de negocios definitivo.",
            "colors": ["Black"],
            "category": "notebook",
            "discount_price": None,
        },
        {
            "id": 10,
            "name": "AirPods Pro 2",
            "brand": "Apple",
            "price": 249.0,
            "image": "/airpodspro2.png",
            "description": "Reconstruido desde cero para un audio aún más rico.",
            "colors": ["White"],
            "category": "accessory",
            "discount_price": 229.0,
        },
        {
            "id": 11,
            "name": "Sony WH-1000XM5",
            "brand": "Sony",
            "price": 399.0,
            "image": "/sonyxm5.png",
            "description": "Los mejores audífonos con cancelación de ruido del mercado, ahora aún mejores.",
            "colors": ["Black", "Silver"],
            "category": "accessory",
            "discount_price": None,
        },
        {
            "id": 12,
            "name": "Anker PowerCore 24K",
            "brand": "Anker",
            "price": 149.99,
            "image": "/ankerpowercore.png",
            "description": "Carga bidireccional ultrapotente: equipado con lo último en Power Delivery 3.1.",
            "colors": ["Black"],
            "category": "accessory",
            "discount_price": None,
        },
        {
            "id": 13,
            "name": "JBL Charge 5",
            "brand": "JBL",
            "price": 179.95,
            "image": "/jblcharge5.png",
            "description": "Lleva la fiesta contigo sin importar el clima.",
            "colors": ["Black", "Blue", "Red", "Teal"],
            "category": "accessory",
            "discount_price": 149.95,
        },
    ]
    cart: list[CartItem] = []
    orders: list[Order] = [
        {
            "id": 1,
            "customer_email": "comprador1@example.com",
            "items": [{"product_id": 2, "quantity": 1, "color": "Natural Titanium"}],
            "total": 1099.0,
            "status": "Entregado",
            "created_at": "2024-05-20T10:00:00",
        },
        {
            "id": 2,
            "customer_email": "comprador2@example.com",
            "items": [
                {"product_id": 1, "quantity": 1, "color": "Obsidian"},
                {"product_id": 4, "quantity": 1, "color": "Silky Black"},
            ],
            "total": 1798.0,
            "status": "Enviado",
            "created_at": "2024-05-21T11:30:00",
        },
        {
            "id": 3,
            "customer_email": "comprador1@example.com",
            "items": [{"product_id": 10, "quantity": 2, "color": "White"}],
            "total": 458.0,
            "status": "Pendiente",
            "created_at": "2024-05-22T09:00:00",
        },
    ]
    search_query: str = ""
    filter_brand: str = ""
    filter_category: str = ""
    filter_min_price: int = 0
    filter_max_price: int = 2000
    filter_sort: str = "price_asc"
    selected_product: Optional[Product] = None
    selected_quantity: int = 1
    selected_color: str = ""
    buy_now_item: Optional[CartItem] = None

    @rx.event
    def load_product_details(self):
        product_id = self.router.page.params.get("product_id")
        if product_id:
            product = next(
                (p for p in self.products if p["id"] == int(product_id)), None
            )
            if product:
                self.selected_product = product
                self.selected_quantity = 1
                if product["colors"]:
                    self.selected_color = product["colors"][0]

    @rx.event
    def set_selected_quantity(self, quantity: int):
        self.selected_quantity = int(quantity)

    @rx.event
    def set_selected_color(self, color: str):
        self.selected_color = color

    @rx.var
    def filtered_and_sorted_products(self) -> list[Product]:
        products = self.products
        if self.filter_category:
            products = [p for p in products if p["category"] == self.filter_category]
        if self.search_query:
            sq_lower = self.search_query.lower()
            products = [
                p
                for p in products
                if sq_lower in p["name"].lower() or sq_lower in p["brand"].lower()
            ]
        if self.filter_brand:
            products = [p for p in products if p["brand"] == self.filter_brand]
        products = [
            p
            for p in products
            if (p.get("discount_price") or p["price"]) >= self.filter_min_price
            and (p.get("discount_price") or p["price"]) <= self.filter_max_price
        ]
        if self.filter_sort == "price_asc":
            products.sort(key=lambda p: p.get("discount_price") or p["price"])
        elif self.filter_sort == "price_desc":
            products.sort(
                key=lambda p: p.get("discount_price") or p["price"], reverse=True
            )
        elif self.filter_sort == "name_asc":
            products.sort(key=lambda p: p["name"])
        elif self.filter_sort == "name_desc":
            products.sort(key=lambda p: p["name"], reverse=True)
        return products

    @rx.var
    def discounted_products(self) -> list[Product]:
        return [
            p
            for p in self.products
            if p["discount_price"] is not None and p != self.selected_product
        ][:3]

    @rx.var
    def brands(self) -> list[str]:
        products = self.products
        if self.filter_category:
            products = [p for p in products if p["category"] == self.filter_category]
        return sorted(list(set((p["brand"] for p in products))))

    @rx.var
    def cart_items_detailed(self) -> list[DetailedCartItem]:
        detailed_cart = []
        for item in self.cart:
            product = next(
                (p for p in self.products if p["id"] == item["product_id"]), None
            )
            if product:
                price = product.get("discount_price") or product["price"]
                detailed_cart.append(
                    {
                        "product": product,
                        "quantity": item["quantity"],
                        "subtotal": price * item["quantity"],
                        "color": item["color"],
                    }
                )
        return detailed_cart

    @rx.var
    def cart_total(self) -> float:
        return sum((item["subtotal"] for item in self.cart_items_detailed))

    @rx.var
    def buy_now_item_detailed(self) -> list[DetailedCartItem]:
        if not self.buy_now_item:
            return []
        product = next(
            (p for p in self.products if p["id"] == self.buy_now_item["product_id"]),
            None,
        )
        if product:
            price = product.get("discount_price") or product["price"]
            return [
                {
                    "product": product,
                    "quantity": self.buy_now_item["quantity"],
                    "subtotal": price * self.buy_now_item["quantity"],
                    "color": self.buy_now_item["color"],
                }
            ]
        return []

    @rx.var
    def buy_now_total(self) -> float:
        if not self.buy_now_item_detailed:
            return 0.0
        return self.buy_now_item_detailed[0]["subtotal"]

    @rx.event
    def add_to_cart(self, product_id: int, quantity: int, color: str):
        for item in self.cart:
            if item["product_id"] == product_id and item["color"] == color:
                item["quantity"] += quantity
                yield rx.toast.success(f"¡Producto {color} actualizado en el carrito!")
                return
        self.cart.append(
            {"product_id": product_id, "quantity": quantity, "color": color}
        )
        yield rx.toast.success("¡Añadido al carrito!")

    @rx.event
    def remove_from_cart(self, product_id: int):
        self.cart = [item for item in self.cart if item["product_id"] != product_id]

    @rx.event
    def update_quantity(self, product_id: int, quantity: str):
        quantity_int = int(quantity)
        for i, item in enumerate(self.cart):
            if item["product_id"] == product_id:
                if quantity_int > 0:
                    self.cart[i]["quantity"] = quantity_int
                else:
                    self.cart.pop(i)
                return

    @rx.event
    def checkout(self):
        if not self.cart and (not self.buy_now_item):
            return rx.toast.error("Tu carrito está vacío.")
        return rx.redirect("/checkout")

    @rx.event
    def buy_now(self, product_id: int, quantity: int, color: str):
        self.buy_now_item = {
            "product_id": product_id,
            "quantity": quantity,
            "color": color,
        }
        return rx.redirect("/checkout")

    @rx.event
    def clear_buy_now_item(self):
        self.buy_now_item = None

    @rx.event
    def clear_buy_now_item_if_not_checkout(self):
        if self.router.page.path != "/checkout":
            self.buy_now_item = None

    @rx.event
    async def request_revision(self, order_id: int):
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user_email:
            yield rx.toast.error("Debes iniciar sesión.")
            return
        for order in self.orders:
            if (
                order["id"] == order_id
                and order["customer_email"] == auth_state.current_user_email
            ):
                if order["status"] == "Entregado":
                    order["status"] = "Revisión Solicitada"
                    admin_state = await self.get_state(AdminState)
                    yield admin_state.add_notification(
                        f"El cliente {auth_state.current_user_email} solicitó revisión para la orden #{order_id}."
                    )
                    yield rx.toast.info("Revisión solicitada para tu orden.")
                else:
                    yield rx.toast.warning(
                        "Solo puedes solicitar revisión de órdenes entregadas."
                    )
                return

    @rx.var
    def order_stats(self) -> dict[str, int]:
        stats = {
            "Procesando": 0,
            "Enviado": 0,
            "Entregado": 0,
            "Revisión Solicitada": 0,
        }
        for order in self.orders:
            if order["status"] in stats:
                stats[order["status"]] += 1
        return stats

    @rx.event
    def export_orders(self):
        if not self.orders:
            return rx.toast.warning("No hay órdenes para exportar.")
        output = io.StringIO()
        writer = csv.writer(output)
        headers = [
            "ID Orden",
            "Total",
            "Estado",
            "Nombre Producto",
            "Cantidad",
            "Color",
        ]
        writer.writerow(headers)
        for order in self.orders:
            for item in order["items"]:
                product = next(
                    (p for p in self.products if p["id"] == item["product_id"]), None
                )
                product_name = product["name"] if product else "Desconocido"
                writer.writerow(
                    [
                        order["id"],
                        order["total"],
                        order["status"],
                        product_name,
                        item["quantity"],
                        item["color"],
                    ]
                )
        csv_data = output.getvalue()
        return rx.download(data=csv_data, filename="ordenes.csv")


class AdminState(rx.State):
    orders: list[Order] = []
    filter_date_from: str = ""
    filter_date_to: str = ""
    filter_customer: str = ""
    filter_order_status: str = ""
    current_page: int = 1
    items_per_page: int = 10
    show_order_detail: bool = False
    selected_order: Optional[Order] = None
    notifications: list[Notification] = []

    @rx.var
    def unique_customers(self) -> list[str]:
        return sorted(list(set((order["customer_email"] for order in self.orders))))

    @rx.var
    def filtered_orders(self) -> list[Order]:
        orders_to_filter = self.orders
        if self.filter_order_status:
            orders_to_filter = [
                o for o in orders_to_filter if o["status"] == self.filter_order_status
            ]
        if self.filter_customer:
            orders_to_filter = [
                o
                for o in orders_to_filter
                if o["customer_email"] == self.filter_customer
            ]
        if self.filter_date_from:
            orders_to_filter = [
                o for o in orders_to_filter if o["created_at"] >= self.filter_date_from
            ]
        if self.filter_date_to:
            orders_to_filter = [
                o for o in orders_to_filter if o["created_at"] <= self.filter_date_to
            ]
        return sorted(orders_to_filter, key=lambda o: o["created_at"], reverse=True)

    @rx.var
    def total_pages(self) -> int:
        return -(-len(self.filtered_orders) // self.items_per_page)

    @rx.var
    def paginated_orders(self) -> list[Order]:
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_orders[start:end]

    @rx.event
    def clear_filters(self):
        self.filter_date_from = ""
        self.filter_date_to = ""
        self.filter_customer = ""
        self.filter_order_status = ""
        self.current_page = 1

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    async def load_all_orders(self):
        main_state = await self.get_state(MainState)
        self.orders = main_state.orders

    @rx.event
    async def change_order_status(self, order_id: int, status: str):
        main_state = await self.get_state(MainState)
        for i, order in enumerate(main_state.orders):
            if order["id"] == order_id:
                main_state.orders[i]["status"] = status
                self.orders = main_state.orders
                yield rx.toast.success(f"Orden #{order_id} actualizada a {status}")
                return

    @rx.event
    def accept_order(self, order_id: int):
        yield AdminState.change_order_status(order_id, "Procesando")

    @rx.event
    def cancel_order(self, order_id: int):
        yield AdminState.change_order_status(order_id, "Cancelado")

    @rx.event
    def view_order_details(self, order: Order):
        self.selected_order = order
        self.show_order_detail = True

    @rx.event
    def close_order_detail_modal(self):
        self.show_order_detail = False
        self.selected_order = None

    @rx.var
    def unread_notifications_count(self) -> int:
        return sum((1 for n in self.notifications if not n["read"]))

    @rx.event
    def add_notification(self, message: str):
        self.notifications.insert(
            0,
            {
                "id": str(uuid.uuid4()),
                "message": message,
                "read": False,
                "created_at": datetime.now().isoformat(),
            },
        )
        yield rx.toast.info(message)

    @rx.event
    def mark_notification_as_read(self, notification_id: str):
        for i, n in enumerate(self.notifications):
            if n["id"] == notification_id:
                self.notifications[i]["read"] = True
                return

    @rx.event
    def mark_all_as_read(self):
        for i in range(len(self.notifications)):
            self.notifications[i]["read"] = True

    transactions: list[Transaction] = []

    @rx.event
    def add_transaction(
        self, order_id: int, type: str, amount: float, description: str
    ):
        self.transactions.append(
            {
                "id": str(uuid.uuid4()),
                "order_id": order_id,
                "type": type,
                "amount": amount,
                "date": datetime.now().isoformat(),
                "description": description,
            }
        )

    @rx.var
    def monthly_income(self) -> dict[str, float]:
        income_by_month: dict[str, float] = {}
        for tx in self.transactions:
            if tx["type"] == "Ingreso":
                month = datetime.fromisoformat(tx["date"]).strftime("%Y-%m")
                income_by_month[month] = income_by_month.get(month, 0) + tx["amount"]
        return income_by_month

    @rx.var
    def monthly_income_chart_data(self) -> list[dict]:
        return [
            {"month": month, "ingresos": amount}
            for month, amount in sorted(self.monthly_income.items())
        ]

    @rx.var
    def total_sales(self) -> float:
        return sum((o["total"] for o in self.orders))

    @rx.var
    def average_order_value(self) -> float:
        if not self.orders:
            return 0.0
        return self.total_sales / len(self.orders)

    transactions: list[Transaction] = []

    @rx.event
    def add_transaction(
        self, order_id: int, type: str, amount: float, description: str
    ):
        self.transactions.append(
            {
                "id": str(uuid.uuid4()),
                "order_id": order_id,
                "type": type,
                "amount": amount,
                "date": datetime.now().isoformat(),
                "description": description,
            }
        )

    @rx.var
    def monthly_income(self) -> dict[str, float]:
        income_by_month: dict[str, float] = {}
        for tx in self.transactions:
            if tx["type"] == "Ingreso":
                month = datetime.fromisoformat(tx["date"]).strftime("%Y-%m")
                income_by_month[month] = income_by_month.get(month, 0) + tx["amount"]
        return income_by_month

    @rx.var
    def monthly_income_chart_data(self) -> list[dict]:
        return [
            {"month": month, "ingresos": amount}
            for month, amount in sorted(self.monthly_income.items())
        ]

    @rx.var
    def total_sales(self) -> float:
        return sum((o["total"] for o in self.orders))

    @rx.var
    def average_order_value(self) -> float:
        if not self.orders:
            return 0.0
        return self.total_sales / len(self.orders)


class PaymentState(rx.State):
    webpay_token: str = ""
    webpay_url: str = ""
    pending_order_id: str = ""
    payment_amount: float = 0.0
    payment_status: str = ""

    def _get_tx(self) -> Transaction:
        COMMERCE_CODE = os.getenv("WEBPAY_COMMERCE_CODE", "597055555532")
        API_KEY = os.getenv(
            "WEBPAY_API_KEY",
            "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        )
        options = WebpayOptions(COMMERCE_CODE, API_KEY, IntegrationType.TEST)
        return Transaction(options)

    def _generate_short_order_id(self) -> str:
        """Generates a unique order ID with a maximum of 26 characters."""
        return uuid.uuid4().hex[:26]

    @rx.event
    async def initiate_webpay_transaction(self):
        main_state = await self.get_state(MainState)
        items_to_purchase = []
        total_amount = 0.0
        is_buy_now = False
        if main_state.buy_now_item:
            items_to_purchase = main_state.buy_now_item_detailed
            total_amount = main_state.buy_now_total
            is_buy_now = True
        elif main_state.cart:
            items_to_purchase = main_state.cart_items_detailed
            total_amount = main_state.cart_total
        else:
            yield rx.toast.error("No hay nada para comprar.")
            return
        self.payment_amount = total_amount
        self.pending_order_id = self._generate_short_order_id()
        return_url = f"{self.router.page.full_raw_path.replace('/checkout', '')}/payment/callback"
        try:
            tx = self._get_tx()
            response = tx.create(
                buy_order=self.pending_order_id,
                session_id=self.pending_order_id,
                amount=int(self.payment_amount),
                return_url=return_url,
            )
            self.webpay_token = response["token"]
            self.webpay_url = response["url"]
            yield rx.redirect(self.webpay_url)
            return
        except Exception as e:
            logging.exception(f"Error de WebPay: {e}")
            yield rx.toast.error(f"Error de WebPay: {str(e)}")

    @rx.event
    async def confirm_payment(self):
        token = self.router.page.params.get("token_ws")
        tbk_token = self.router.page.params.get("TBK_TOKEN")
        tbk_id_session = self.router.page.params.get("TBK_ID_SESION")
        tbk_orden_compra = self.router.page.params.get("TBK_ORDEN_COMPRA")
        if tbk_token and tbk_orden_compra:
            self.payment_status = "Cancelado"
            yield rx.toast.warning("Pago cancelado.")
            yield rx.redirect("/cart")
            return
        if not token:
            self.payment_status = "Fallido"
            yield rx.toast.error("Token de pago inválido.")
            return
        try:
            tx = self._get_tx()
            response = tx.commit(token)
            if response.status == "AUTHORIZED":
                self.payment_status = "Éxito"
                main_state = await self.get_state(MainState)
                new_order_id = max([o["id"] for o in main_state.orders] + [0]) + 1
                items_for_order = []
                order_total = 0.0
                if main_state.buy_now_item:
                    items_for_order = [main_state.buy_now_item]
                    order_total = main_state.buy_now_total
                    main_state.buy_now_item = None
                else:
                    items_for_order = main_state.cart.copy()
                    order_total = main_state.cart_total
                    main_state.cart = []
                auth_state = await self.get_state(AuthState)
                new_order: Order = {
                    "id": new_order_id,
                    "customer_email": auth_state.current_user_email
                    or "anonimo@example.com",
                    "items": items_for_order,
                    "total": order_total,
                    "status": "Pendiente",
                    "created_at": datetime.now().isoformat(),
                }
                main_state.orders.append(new_order)
                admin_state = await self.get_state(AdminState)
                main_state.orders.append(new_order)
                yield AdminState.add_transaction(
                    order_id=new_order_id,
                    type="Ingreso",
                    amount=order_total,
                    description=f"Venta de orden #{new_order_id}",
                )
                yield admin_state.add_notification(
                    f"Nueva orden #{new_order_id} recibida por ${order_total:.2f}."
                )
                yield rx.toast.success(
                    "¡Pago exitoso! Orden creada y pendiente de aprobación."
                )
                yield rx.redirect("/profile")
                return
            else:
                self.payment_status = "Fallido"
                yield rx.toast.error(f"Pago fallido: {response.response_code}")
        except Exception as e:
            logging.exception(f"Error de confirmación de WebPay: {e}")
            self.payment_status = "Fallido"
            yield rx.toast.error(f"Error de confirmación de WebPay: {str(e)}")