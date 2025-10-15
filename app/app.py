import reflex as rx
from app.pages.index import index
from app.pages.sign_in import sign_in
from app.pages.sign_up import sign_up
from app.pages.cart import cart
from app.pages.profile import profile
from app.pages.product_detail import product_detail
from app.pages.admin import admin
from app.pages.checkout import checkout
from app.pages.payment_callback import payment_callback
from app.state import AuthState, MainState


def placeholder_page(title: str) -> rx.Component:
    def page() -> rx.Component:
        from app.components.navbar import navbar
        from app.components.footer import footer

        return rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(title, class_name="text-3xl font-bold"),
                    rx.el.p("This page is under construction."),
                    class_name="container mx-auto px-4 py-12 text-center",
                ),
                class_name="flex-grow",
            ),
            footer(),
            class_name="flex flex-col min-h-screen font-['Raleway'] bg-gray-50",
        )

    return page


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(sign_in, route="/sign-in")
app.add_page(sign_up, route="/sign-up")
app.add_page(cart, route="/cart")
app.add_page(profile, route="/profile", on_load=AuthState.check_session)
app.add_page(
    product_detail,
    route="/product/[product_id]",
    on_load=MainState.load_product_details,
)
app.add_page(admin, route="/admin", on_load=AuthState.check_admin)
app.add_page(checkout, route="/checkout", on_load=AuthState.check_session)
app.add_page(payment_callback, route="/payment/callback")
from app.pages.accessories import accessories
from app.pages.smartphones import smartphones
from app.pages.notebooks import notebooks

app.add_page(accessories, route="/accessories")
app.add_page(smartphones, route="/smartphones")
app.add_page(notebooks, route="/notebooks")
app.add_page(placeholder_page("Política"), route="/policy")
app.add_page(placeholder_page("Ubicación"), route="/location")
app.add_page(placeholder_page("Contáctanos"), route="/contact")
app.add_page(
    lambda: rx.fragment(),
    route="/auth/google/callback",
    on_load=AuthState.handle_google_callback,
)