import reflex as rx
from app.state import PaymentState
from app.components.navbar import navbar
from app.components.footer import footer


def payment_callback() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.cond(
                    PaymentState.payment_status == "Éxito",
                    rx.el.div(
                        rx.icon(
                            "check_check",
                            class_name="h-16 w-16 text-green-500 mx-auto mb-4",
                        ),
                        rx.el.h1(
                            "Pago Exitoso", class_name="text-3xl font-bold text-center"
                        ),
                        rx.el.p(
                            "Tu orden está siendo procesada.",
                            class_name="text-center mt-2",
                        ),
                        rx.el.a(
                            "Ver mis órdenes",
                            href="/profile",
                            class_name="mt-6 inline-block bg-violet-500 text-white px-6 py-2 rounded-lg",
                        ),
                    ),
                    rx.cond(
                        PaymentState.payment_status == "Fallido",
                        rx.el.div(
                            rx.icon(
                                "circle_x",
                                class_name="h-16 w-16 text-red-500 mx-auto mb-4",
                            ),
                            rx.el.h1(
                                "Pago Fallido",
                                class_name="text-3xl font-bold text-center",
                            ),
                            rx.el.p(
                                "Hubo un problema con tu pago. Por favor, intenta de nuevo.",
                                class_name="text-center mt-2",
                            ),
                            rx.el.a(
                                "Ir al carrito",
                                href="/cart",
                                class_name="mt-6 inline-block bg-gray-500 text-white px-6 py-2 rounded-lg",
                            ),
                        ),
                        rx.cond(
                            PaymentState.payment_status == "Cancelado",
                            rx.el.div(
                                rx.icon(
                                    "ban",
                                    class_name="h-16 w-16 text-yellow-500 mx-auto mb-4",
                                ),
                                rx.el.h1(
                                    "Pago Cancelado",
                                    class_name="text-3xl font-bold text-center",
                                ),
                                rx.el.p(
                                    "Has cancelado el pago.",
                                    class_name="text-center mt-2",
                                ),
                                rx.el.a(
                                    "Ir al carrito",
                                    href="/cart",
                                    class_name="mt-6 inline-block bg-gray-500 text-white px-6 py-2 rounded-lg",
                                ),
                            ),
                            rx.el.div(
                                rx.icon(
                                    "loader",
                                    class_name="h-16 w-16 text-gray-500 mx-auto animate-spin mb-4",
                                ),
                                rx.el.h1(
                                    "Confirmando Pago...",
                                    class_name="text-3xl font-bold text-center",
                                ),
                                rx.el.p(
                                    "Por favor, no cierres esta página.",
                                    class_name="text-center mt-2",
                                ),
                            ),
                        ),
                    ),
                ),
                class_name="max-w-xl mx-auto py-24",
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
        on_mount=PaymentState.confirm_payment,
    )