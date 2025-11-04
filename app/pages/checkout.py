import reflex as rx
from app.state import MainState, PaymentState
from app.components.navbar import navbar
from app.components.footer import footer


def checkout() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Pagar", class_name="text-3xl font-bold mb-8"),
                rx.cond(
                    (MainState.cart.length() > 0)
                    | MainState.buy_now_item.is_not_none(),
                    rx.el.div(
                        rx.el.h2(
                            "Resumen de la Orden",
                            class_name="text-xl font-semibold mb-4",
                        ),
                        rx.cond(
                            MainState.buy_now_item.is_not_none(),
                            rx.foreach(
                                MainState.buy_now_item_detailed,
                                lambda item: rx.el.div(
                                    rx.el.p(
                                        f"{item.get('product').get('name')} x {item.get('quantity').to_string()}"
                                    ),
                                    rx.el.p(f"${item.get('subtotal')}"),
                                    class_name="flex justify-between",
                                ),
                            ),
                            rx.foreach(
                                MainState.cart_items_detailed,
                                lambda item: rx.el.div(
                                    rx.el.p(
                                        f"{item.get('product').get('name')} x {item.get('quantity').to_string()}"
                                    ),
                                    rx.el.p(f"${item.get('subtotal')}"),
                                    class_name="flex justify-between",
                                ),
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Total:", class_name="text-lg font-semibold"),
                            rx.el.p(
                                rx.cond(
                                    MainState.buy_now_item.is_not_none(),
                                    f"${MainState.buy_now_total:.2f}",
                                    f"${MainState.cart_total:.2f}",
                                ),
                                class_name="text-2xl font-bold",
                            ),
                            class_name="flex justify-between items-center mt-4",
                        ),
                        rx.el.button(
                            "Pagar con Webpay",
                            on_click=PaymentState.initiate_webpay_transaction,
                            is_loading=PaymentState.webpay_url != "",
                            class_name="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors shadow-md",
                        ),
                        class_name="bg-white p-8 rounded-xl shadow-md border max-w-lg mx-auto",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Tu carrito está vacío. No hay nada que pagar.",
                            class_name="text-gray-500",
                        ),
                        class_name="text-center p-16 bg-white rounded-xl shadow-md border max-w-lg mx-auto",
                    ),
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
        on_mount=MainState.clear_buy_now_item_if_not_checkout,
    )