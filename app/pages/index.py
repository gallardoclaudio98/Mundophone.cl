import reflex as rx
from app.state import MainState, Product
from app.components.navbar import navbar
from app.components.footer import footer


def product_card(product: Product) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src=product["image"],
                        class_name="h-48 w-full object-contain rounded-t-xl",
                    ),
                    class_name="bg-gray-100 rounded-t-xl group-hover:bg-gray-200 transition-colors",
                ),
                rx.el.div(
                    rx.el.h3(
                        product["name"],
                        class_name="text-lg font-semibold text-gray-800",
                    ),
                    rx.el.p(
                        f"${product['price']:.2f}",
                        class_name="text-violet-600 font-bold",
                    ),
                    rx.el.p(
                        product["description"],
                        class_name="text-sm text-gray-500 mt-2 h-10 overflow-hidden",
                    ),
                    class_name="p-4 flex-grow",
                ),
            ),
            href=f"/product/{product['id']}",
        ),
        rx.el.div(
            rx.el.button(
                "Ver Detalles",
                on_click=rx.redirect(f"/product/{product['id']}"),
                class_name="w-full bg-violet-500 text-white py-2 rounded-lg hover:bg-violet-600 transition-all duration-300 shadow-md hover:shadow-lg",
            ),
            rx.el.button(
                "Comprar Ahora",
                on_click=MainState.buy_now(product["id"], 1, product["colors"][0]),
                class_name="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-all duration-300 shadow-md hover:shadow-lg mt-2",
            ),
            class_name="p-4 pt-0",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-xl transition-shadow duration-300 flex flex-col justify-between group",
    )


def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Encuentra tu Próximo Teléfono",
                    class_name="text-4xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Los mejores modelos de las marcas líderes, solo para ti.",
                    class_name="text-lg text-gray-600 mt-2",
                ),
                class_name="text-center py-16 bg-violet-50 rounded-xl",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Buscar un teléfono...",
                        on_change=MainState.set_search_query.debounce(300),
                        class_name="w-full md:w-1/2 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500 focus:outline-none",
                    ),
                    rx.el.select(
                        rx.el.option("Todas las Marcas", value=""),
                        rx.foreach(
                            MainState.brands,
                            lambda brand: rx.el.option(brand, value=brand),
                        ),
                        on_change=MainState.set_filter_brand,
                        value=MainState.filter_brand,
                        class_name="p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500 focus:outline-none",
                    ),
                    class_name="flex flex-col md:flex-row gap-4 mb-8",
                ),
                rx.el.div(
                    rx.foreach(MainState.filtered_and_sorted_products, product_card),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8",
                ),
                class_name="container mx-auto px-4 py-12",
            ),
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
    )