import reflex as rx
from app.state import AdminState
from app.components.navbar import navbar
from app.components.footer import footer


def stat_card(icon: str, title: str, value: rx.Var, color: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name=f"h-8 w-8 text-{color}-500"),
        rx.el.div(
            rx.el.p(title, class_name="text-sm text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm border",
    )


def finance() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Dashboard Financiero", class_name="text-3xl font-bold mb-8"),
                rx.el.div(
                    stat_card(
                        "dollar-sign",
                        "Ventas Totales",
                        f"${AdminState.total_sales:.2f}",
                        "green",
                    ),
                    stat_card(
                        "receipt",
                        "Órdenes Totales",
                        AdminState.orders.length().to_string(),
                        "blue",
                    ),
                    stat_card(
                        "bar-chart",
                        "Valor Promedio de Orden",
                        f"${AdminState.average_order_value:.2f}",
                        "violet",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Ingresos Mensuales",
                            class_name="text-xl font-semibold mb-4",
                        ),
                        rx.recharts.bar_chart(
                            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                            rx.recharts.x_axis(data_key="month"),
                            rx.recharts.y_axis(),
                            rx.recharts.tooltip(),
                            rx.recharts.bar(
                                data_key="ingresos", fill="#8884d8", name="Ingresos"
                            ),
                            data=AdminState.monthly_income_chart_data,
                            height=300,
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(class_name="w-4 h-4 bg-[#8884d8]"),
                                rx.el.p("Ingresos"),
                            ),
                            class_name="flex justify-center items-center gap-4 mt-4 text-sm text-gray-600",
                        ),
                        class_name="p-6 bg-white rounded-xl shadow-sm border",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Transacciones Recientes",
                            class_name="text-xl font-semibold mb-4",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th("ID Transacción"),
                                        rx.el.th("ID Orden"),
                                        rx.el.th("Tipo"),
                                        rx.el.th("Monto"),
                                        rx.el.th("Fecha"),
                                        rx.el.th("Descripción"),
                                        class_name="text-left text-sm font-semibold text-gray-600 border-b",
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        AdminState.transactions,
                                        lambda tx: rx.el.tr(
                                            rx.el.td(tx.get("id")),
                                            rx.el.td(tx.get("order_id")),
                                            rx.el.td(tx.get("type")),
                                            rx.el.td(f"${tx.get('amount')}"),
                                            rx.el.td(tx.get("date")),
                                            rx.el.td(tx.get("description")),
                                            class_name="text-sm",
                                        ),
                                    )
                                ),
                                class_name="w-full table-auto",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        class_name="p-6 bg-white rounded-xl shadow-sm border",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
    )