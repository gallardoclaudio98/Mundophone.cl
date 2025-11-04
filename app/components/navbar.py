import reflex as rx
from app.state import AuthState, AdminState, Notification


def notification_item(notification: Notification) -> rx.Component:
    return rx.el.div(
        rx.el.p(notification["message"], class_name="text-sm"),
        rx.el.p(notification["created_at"], class_name="text-xs text-gray-500 mt-1"),
        class_name=rx.cond(
            notification["read"],
            "p-2 border-b border-gray-100",
            "p-2 border-b border-gray-100 bg-blue-50",
        ),
        on_click=AdminState.mark_notification_as_read(notification["id"]),
    )


def notifications_panel() -> rx.Component:
    return rx.radix.dropdown_menu.root(
        rx.radix.dropdown_menu.trigger(
            rx.el.button(
                rx.icon("bell", class_name="h-6 w-6"),
                rx.cond(
                    AdminState.unread_notifications_count > 0,
                    rx.el.span(
                        AdminState.unread_notifications_count.to_string(),
                        class_name="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-red-500 text-white text-xs flex items-center justify-center",
                    ),
                    rx.fragment(),
                ),
                class_name="relative p-2 rounded-full hover:bg-gray-100 transition-colors",
            )
        ),
        rx.radix.dropdown_menu.content(
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Notificaciones", class_name="font-semibold"),
                    rx.el.button(
                        "Marcar todo como leído",
                        on_click=AdminState.mark_all_as_read,
                        class_name="text-sm text-blue-600 hover:underline",
                    ),
                    class_name="flex justify-between items-center p-2 border-b",
                ),
                rx.el.div(
                    rx.foreach(AdminState.notifications, notification_item),
                    class_name="max-h-96 overflow-y-auto",
                ),
                rx.cond(
                    AdminState.notifications.length() == 0,
                    rx.el.p(
                        "No hay notificaciones",
                        class_name="p-4 text-center text-sm text-gray-500",
                    ),
                    rx.fragment(),
                ),
            ),
            class_name="w-80 bg-white rounded-lg shadow-lg border z-50",
        ),
    )


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
                            AuthState.is_admin, notifications_panel(), rx.fragment()
                        ),
                        rx.cond(
                            AuthState.is_admin,
                            rx.fragment(),
                            rx.el.a(
                                rx.icon("shield", class_name="h-6 w-6"),
                                href="/admin",
                                class_name="p-2 rounded-full hover:bg-gray-100 transition-colors text-blue-600",
                            ),
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