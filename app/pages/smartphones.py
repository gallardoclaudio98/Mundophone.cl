import reflex as rx
from app.state import MainState
from app.components.navbar import navbar
from app.components.footer import footer
from app.pages.index import product_card


def smartphones() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Smartphones", class_name="text-4xl font-bold text-gray-900"),
                rx.el.p(
                    "Descubre los últimos modelos y las mejores marcas.",
                    class_name="text-lg text-gray-600 mt-2",
                ),
                class_name="text-center py-16 bg-violet-50 rounded-xl",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Buscar en smartphones...",
                        on_change=MainState.set_search_query.debounce(300),
                        class_name="w-full md:w-1/3 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500 focus:outline-none",
                    ),
                    rx.el.select(
                        rx.el.option("Todas las marcas", value=""),
                        rx.foreach(
                            MainState.brands,
                            lambda brand: rx.el.option(brand, value=brand),
                        ),
                        on_change=MainState.set_filter_brand,
                        value=MainState.filter_brand,
                        class_name="p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500 focus:outline-none",
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="number",
                            placeholder="Min Price",
                            on_change=MainState.set_filter_min_price,
                            class_name="p-3 border rounded-lg w-full",
                        ),
                        rx.el.input(
                            type="number",
                            placeholder="Max Price",
                            on_change=MainState.set_filter_max_price,
                            class_name="p-3 border rounded-lg w-full",
                        ),
                        class_name="flex gap-2",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "Ordenar por: Precio (Bajo a Alto)", value="price_asc"
                        ),
                        rx.el.option(
                            "Ordenar por: Precio (Alto a Bajo)", value="price_desc"
                        ),
                        rx.el.option("Ordenar por: Nombre (A-Z)", value="name_asc"),
                        rx.el.option("Ordenar por: Nombre (Z-A)", value="name_desc"),
                        on_change=MainState.set_filter_sort,
                        value=MainState.filter_sort,
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
        on_mount=lambda: MainState.set_filter_category("smartphone"),
    )