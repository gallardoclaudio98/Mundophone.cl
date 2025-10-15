import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                "© 2024 MobileShop. All rights reserved.",
                class_name="text-sm text-gray-500",
            ),
            rx.el.div(
                rx.el.a(rx.icon("github"), href="#"),
                rx.el.a(rx.icon("twitter"), href="#"),
                rx.el.a(rx.icon("instagram"), href="#"),
                class_name="flex gap-4",
            ),
            class_name="flex justify-between items-center container mx-auto px-4",
        ),
        class_name="py-8 border-t border-gray-200 bg-gray-50",
    )