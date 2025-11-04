import reflex as rx
from app.state import AuthState


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("smartphone", class_name="text-violet-500"),
                        rx.el.span("MobileShop", class_name="font-bold text-xl"),
                        class_name="flex items-center gap-2",
                    ),
                    href="/",
                ),
                rx.el.nav(
                    rx.el.a(
                        "Smartphones",
                        href="/smartphones",
                        class_name="text-sm font-medium text-gray-600 hover:text-violet-600",
                    ),
                    rx.el.a(
                        "Notebooks",
                        href="/notebooks",
                        class_name="text-sm font-medium text-gray-600 hover:text-violet-600",
                    ),
                    rx.el.a(
                        "Accesorios",
                        href="/accessories",
                        class_name="text-sm font-medium text-gray-600 hover:text-violet-600",
                    ),
                    rx.el.a(
                        "Política",
                        href="/policy",
                        class_name="text-sm font-medium text-gray-600 hover:text-violet-600",
                    ),
                    rx.el.a(
                        "Ubicación",
                        href="/location",
                        class_name="text-sm font-medium text-gray-600 hover:text-violet-600",
                    ),
                    rx.el.a(
                        "Contáctanos",
                        href="/contact",
                        class_name="text-sm font-medium text-gray-600 hover:text-violet-600",
                    ),
                    class_name="hidden md:flex items-center gap-6",
                ),
                class_name="flex items-center gap-8",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("shopping-cart", class_name="h-6 w-6"),
                    href="/cart",
                    class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                ),
                rx.cond(
                    AuthState.in_session,
                    rx.el.div(
                        rx.cond(
                            AuthState.is_admin,
                            rx.el.a(
                                rx.icon("shield", class_name="h-6 w-6"),
                                href="/admin",
                                class_name="p-2 rounded-full hover:bg-gray-100 transition-colors text-blue-600",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.a(
                            rx.icon("user", class_name="h-6 w-6"),
                            href="/profile",
                            class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.a(
                        "Iniciar Sesión",
                        href="/sign-in",
                        class_name="px-4 py-2 text-sm font-medium text-violet-600 border border-violet-200 rounded-lg hover:bg-violet-50",
                    ),
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between container mx-auto px-4",
        ),
        class_name="w-full py-4 bg-white/80 backdrop-blur-md sticky top-0 z-40 border-b border-gray-200",
    )