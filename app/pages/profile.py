import reflex as rx
from app.state import AuthState, MainState, Order
from app.components.navbar import navbar
from app.components.footer import footer


def order_card(order: Order) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(f"Order #{order['id']}", class_name="font-semibold text-lg"),
            rx.el.span(
                order["status"],
                class_name=rx.cond(
                    order["status"] == "Delivered",
                    "bg-green-100 text-green-800",
                    rx.cond(
                        order["status"] == "Shipped",
                        "bg-blue-100 text-blue-800",
                        rx.cond(
                            order["status"] == "Processing",
                            "bg-yellow-100 text-yellow-800",
                            "bg-orange-100 text-orange-800",
                        ),
                    ),
                )
                + " text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(f"Total: ${order['total']:.2f}", class_name="text-gray-600 my-2"),
        rx.el.button(
            "Request Revision",
            on_click=lambda: MainState.request_revision(order["id"]),
            disabled=order["status"] != "Delivered",
            class_name="w-full text-sm py-2 rounded-lg bg-gray-200 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        class_name="p-4 bg-white border rounded-lg shadow-sm",
    )


def profile() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("My Profile", class_name="text-3xl font-bold"),
                    rx.el.button(
                        "Sign Out",
                        on_click=AuthState.sign_out,
                        class_name="bg-red-500 text-white px-4 py-2 rounded-lg",
                    ),
                    class_name="flex justify-between items-center mb-8",
                ),
                rx.el.h2("My Orders", class_name="text-2xl font-semibold mb-4"),
                rx.el.div(
                    rx.foreach(MainState.orders, order_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
    )