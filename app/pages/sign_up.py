import reflex as rx
from app.state import AuthState


def sign_up_card():
    return rx.el.div(
        rx.el.h2(
            "Create Account", class_name="text-2xl font-bold text-center text-gray-800"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label("Email", class_name="text-sm font-medium text-gray-700"),
                rx.el.input(
                    type="email",
                    name="email",
                    placeholder="user@example.com",
                    required=True,
                    class_name="w-full p-3 mt-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label("Password", class_name="text-sm font-medium text-gray-700"),
                rx.el.input(
                    type="password",
                    name="password",
                    required=True,
                    class_name="w-full p-3 mt-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Sign Up",
                type="submit",
                class_name="w-full bg-violet-500 text-white py-3 rounded-lg hover:bg-violet-600 transition-colors duration-300 shadow-md hover:shadow-lg",
            ),
            on_submit=AuthState.sign_up,
            reset_on_submit=True,
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.div(class_name="flex-grow border-t border-gray-300"),
            rx.el.span("OR", class_name="px-4 text-sm text-gray-500"),
            rx.el.div(class_name="flex-grow border-t border-gray-300"),
            class_name="flex items-center my-6",
        ),
        rx.el.button(
            rx.el.img(src="placeholder.svg", class_name="h-5 w-5 mr-3"),
            "Continue with Google",
            on_click=AuthState.initiate_google_oauth,
            class_name="w-full flex justify-center items-center bg-white text-gray-700 py-3 rounded-lg border border-gray-300 hover:bg-gray-100 transition-colors duration-300 shadow-sm",
        ),
        rx.el.p(
            "Already have an account? ",
            rx.el.a(
                "Sign In", href="/sign-in", class_name="text-violet-600 hover:underline"
            ),
            class_name="text-center text-sm text-gray-600 mt-6",
        ),
        class_name="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg border border-gray-200",
    )


def sign_up() -> rx.Component:
    return rx.el.div(
        sign_up_card(),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 font-['Raleway']",
    )