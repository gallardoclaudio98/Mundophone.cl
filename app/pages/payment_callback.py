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
                    PaymentState.payment_status == "Success",
                    rx.el.div(
                        rx.icon(
                            "check_check",
                            class_name="h-16 w-16 text-green-500 mx-auto mb-4",
                        ),
                        rx.el.h1(
                            "Payment Successful",
                            class_name="text-3xl font-bold text-center",
                        ),
                        rx.el.p(
                            "Your order is being processed.",
                            class_name="text-center mt-2",
                        ),
                        rx.el.a(
                            "View my orders",
                            href="/profile",
                            class_name="mt-6 inline-block bg-violet-500 text-white px-6 py-2 rounded-lg",
                        ),
                    ),
                    rx.cond(
                        PaymentState.payment_status == "Failed",
                        rx.el.div(
                            rx.icon(
                                "circle_x",
                                class_name="h-16 w-16 text-red-500 mx-auto mb-4",
                            ),
                            rx.el.h1(
                                "Payment Failed",
                                class_name="text-3xl font-bold text-center",
                            ),
                            rx.el.p(
                                "There was an issue with your payment. Please try again.",
                                class_name="text-center mt-2",
                            ),
                            rx.el.a(
                                "Go to cart",
                                href="/cart",
                                class_name="mt-6 inline-block bg-gray-500 text-white px-6 py-2 rounded-lg",
                            ),
                        ),
                        rx.cond(
                            PaymentState.payment_status == "Cancelled",
                            rx.el.div(
                                rx.icon(
                                    "ban",
                                    class_name="h-16 w-16 text-yellow-500 mx-auto mb-4",
                                ),
                                rx.el.h1(
                                    "Payment Cancelled",
                                    class_name="text-3xl font-bold text-center",
                                ),
                                rx.el.p(
                                    "You have cancelled the payment.",
                                    class_name="text-center mt-2",
                                ),
                                rx.el.a(
                                    "Go to cart",
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
                                    "Confirming Payment...",
                                    class_name="text-3xl font-bold text-center",
                                ),
                                rx.el.p(
                                    "Please do not close this page.",
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