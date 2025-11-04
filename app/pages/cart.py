import reflex as rx
from app.state import MainState, DetailedCartItem
from app.components.navbar import navbar
from app.components.footer import footer


def cart_item_row(item: DetailedCartItem) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=item.get("product").get("image"),
            class_name="w-20 h-20 object-contain rounded-lg",
        ),
        rx.el.div(
            rx.el.h3(item.get("product").get("name"), class_name="font-semibold"),
            rx.el.p(
                "$" + item.get("product").get("price").to_string(),
                class_name="text-gray-600",
            ),
            class_name="flex-grow",
        ),
        rx.el.input(
            type="number",
            on_change=lambda val: MainState.update_quantity(
                item.get("product").get("id"), val
            ),
            class_name="w-20 p-2 border rounded-lg text-center",
            default_value=item.get("quantity").to_string(),
        ),
        rx.el.p(
            "$" + item.get("subtotal").to_string(),
            class_name="font-semibold w-24 text-right",
        ),
        rx.el.button(
            rx.icon("trash-2", class_name="h-5 w-5"),
            on_click=lambda: MainState.remove_from_cart(item.get("product").get("id")),
            class_name="text-red-500 hover:text-red-700",
        ),
        class_name="flex items-center gap-4 py-4 border-b",
    )


def cart() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Carrito de Compras",
                    class_name="text-3xl font-bold text-gray-900 mb-8",
                ),
                rx.cond(
                    MainState.cart.length() > 0,
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(MainState.cart_items_detailed, cart_item_row),
                            class_name="divide-y divide-gray-200",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Total:", class_name="text-lg font-semibold"),
                                rx.el.p(
                                    f"${MainState.cart_total:.2f}",
                                    class_name="text-2xl font-bold",
                                ),
                                class_name="flex justify-between items-center",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "Pagar",
                                    class_name="w-full bg-violet-500 text-white py-3 rounded-lg hover:bg-violet-600 transition-colors shadow-md",
                                ),
                                href="/checkout",
                                class_name="w-full mt-4",
                            ),
                            class_name="mt-8 p-6 bg-gray-100 rounded-lg",
                        ),
                        class_name="bg-white p-8 rounded-xl shadow-md border",
                    ),
                    rx.el.div(
                        rx.el.p("Tu carrito está vacío.", class_name="text-gray-500"),
                        rx.el.a(
                            "Seguir Comprando",
                            href="/",
                            class_name="mt-4 inline-block bg-violet-500 text-white px-6 py-2 rounded-lg",
                        ),
                        class_name="text-center p-16 bg-white rounded-xl shadow-md border",
                    ),
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
    )