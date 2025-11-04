import reflex as rx
from app.state import MainState, Product
from app.components.navbar import navbar
from app.components.footer import footer
from app.pages.index import product_card


def color_selector(color: str) -> rx.Component:
    return rx.el.button(
        class_name=rx.cond(
            MainState.selected_color == color,
            "ring-2 ring-offset-2 ring-violet-500",
            "ring-1 ring-gray-300",
        )
        + " w-8 h-8 rounded-full focus:outline-none transition-all",
        style={"background_color": color},
        on_click=lambda: MainState.set_selected_color(color),
    )


def product_detail() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.cond(
                MainState.selected_product,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=MainState.selected_product["image"],
                                class_name="w-full h-auto object-contain rounded-lg max-h-[500px]",
                            ),
                            class_name="md:w-1/2 p-8 bg-gray-100 rounded-xl",
                        ),
                        rx.el.div(
                            rx.el.h1(
                                MainState.selected_product["name"],
                                class_name="text-4xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                MainState.selected_product["brand"],
                                class_name="text-lg text-gray-500 mt-2",
                            ),
                            rx.el.p(
                                MainState.selected_product["description"],
                                class_name="text-gray-600 mt-4",
                            ),
                            rx.el.div(
                                rx.cond(
                                    MainState.selected_product["discount_price"],
                                    rx.el.div(
                                        rx.el.p(
                                            f"${MainState.selected_product['discount_price']:.2f}",
                                            class_name="text-3xl font-bold text-red-600",
                                        ),
                                        rx.el.p(
                                            f"${MainState.selected_product['price']:.2f}",
                                            class_name="text-xl text-gray-500 line-through ml-2",
                                        ),
                                        class_name="flex items-baseline",
                                    ),
                                    rx.el.p(
                                        f"${MainState.selected_product['price']:.2f}",
                                        class_name="text-3xl font-bold text-gray-900",
                                    ),
                                ),
                                class_name="mt-6",
                            ),
                            rx.el.div(
                                rx.el.p("Color:", class_name="font-semibold mb-2"),
                                rx.el.div(
                                    rx.foreach(
                                        MainState.selected_product["colors"],
                                        color_selector,
                                    ),
                                    class_name="flex gap-3",
                                ),
                                class_name="mt-6",
                            ),
                            rx.el.div(
                                rx.el.label("Quantity:", class_name="font-semibold"),
                                rx.el.input(
                                    type="number",
                                    default_value=MainState.selected_quantity.to_string(),
                                    on_change=MainState.set_selected_quantity,
                                    min=1,
                                    class_name="w-20 p-2 border rounded-lg text-center ml-2",
                                ),
                                class_name="flex items-center mb-4",
                            ),
                            rx.el.div(
                                rx.el.label("Cantidad:", class_name="font-semibold"),
                                rx.el.input(
                                    type="number",
                                    default_value=MainState.selected_quantity.to_string(),
                                    on_change=MainState.set_selected_quantity,
                                    min=1,
                                    class_name="w-20 p-2 border rounded-lg text-center ml-2",
                                ),
                                class_name="flex items-center mb-4",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("shopping-cart", class_name="mr-2"),
                                    "Añadir al Carrito",
                                    on_click=lambda: MainState.add_to_cart(
                                        MainState.selected_product["id"],
                                        MainState.selected_quantity,
                                        MainState.selected_color,
                                    ),
                                    class_name="w-full flex justify-center items-center bg-violet-500 text-white py-3 rounded-lg hover:bg-violet-600 transition-colors shadow-md",
                                ),
                                rx.el.button(
                                    rx.icon("zap", class_name="mr-2"),
                                    "Comprar Ahora",
                                    on_click=lambda: MainState.buy_now(
                                        MainState.selected_product["id"],
                                        MainState.selected_quantity,
                                        MainState.selected_color,
                                    ),
                                    class_name="w-full flex justify-center items-center bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition-colors shadow-md",
                                ),
                                class_name="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4",
                            ),
                            class_name="md:w-1/2 p-8 flex flex-col justify-center",
                        ),
                        class_name="flex flex-col md:flex-row bg-white rounded-xl shadow-lg border",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "En Oferta Ahora",
                            class_name="text-2xl font-bold text-center mb-8",
                        ),
                        rx.el.div(
                            rx.foreach(MainState.discounted_products, product_card),
                            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8",
                        ),
                        class_name="mt-16",
                    ),
                    class_name="container mx-auto px-4 py-12",
                ),
                rx.el.div(
                    rx.el.p("Cargando producto..."), class_name="text-center py-20"
                ),
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
    )