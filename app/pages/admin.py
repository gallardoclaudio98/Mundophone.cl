import reflex as rx
from app.state import MainState, Order
from app.components.navbar import navbar
from app.components.footer import footer


def stat_card(label: str, value: rx.Var[int], color: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6"),
            class_name=f"p-3 rounded-full bg-{color}-100 text-{color}-600",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        ),
        class_name="flex items-center gap-4 p-6 bg-white rounded-xl shadow-sm border",
    )


def order_row(order: Order) -> rx.Component:
    return rx.el.tr(
        rx.el.td(f"#{order.get('id', 'N/A')}", class_name="px-4 py-3"),
        rx.el.td(
            rx.el.ul(
                rx.foreach(
                    order.get("items"),
                    lambda item: rx.el.li(
                        item.get("quantity").to_string()
                        + "x Product ID "
                        + item.get("product_id").to_string()
                        + " ("
                        + item.get("color")
                        + ")"
                    ),
                )
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            "$" + order.get("total").to_string(), class_name="px-4 py-3 font-semibold"
        ),
        rx.el.td(
            rx.el.span(
                order.get("status"),
                class_name=rx.cond(
                    order.get("status") == "Delivered",
                    "bg-green-100 text-green-800",
                    rx.cond(
                        order.get("status") == "Shipped",
                        "bg-blue-100 text-blue-800",
                        rx.cond(
                            order.get("status") == "Processing",
                            "bg-yellow-100 text-yellow-800",
                            "bg-orange-100 text-orange-800",
                        ),
                    ),
                )
                + " text-xs font-medium px-2.5 py-1 rounded-full",
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-b hover:bg-gray-50",
    )


def admin() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Admin Dashboard", class_name="text-3xl font-bold"),
                    rx.el.button(
                        rx.icon("download", class_name="mr-2"),
                        "Export Orders",
                        on_click=MainState.export_orders,
                        class_name="flex items-center bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-8",
                ),
                rx.el.div(
                    stat_card(
                        "Processing",
                        MainState.order_stats["Processing"],
                        "yellow",
                        "loader",
                    ),
                    stat_card(
                        "Shipped", MainState.order_stats["Shipped"], "blue", "truck"
                    ),
                    stat_card(
                        "Delivered",
                        MainState.order_stats["Delivered"],
                        "green",
                        "check_check",
                    ),
                    stat_card(
                        "Revision",
                        MainState.order_stats["Revision Requested"],
                        "orange",
                        "flag_triangle_right",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.h2("All Orders", class_name="text-2xl font-semibold mb-4"),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Order ID", class_name="text-left px-4 py-3"
                                    ),
                                    rx.el.th("Items", class_name="text-left px-4 py-3"),
                                    rx.el.th("Total", class_name="text-left px-4 py-3"),
                                    rx.el.th(
                                        "Status", class_name="text-left px-4 py-3"
                                    ),
                                    class_name="bg-gray-100 border-b",
                                )
                            ),
                            rx.el.tbody(rx.foreach(MainState.orders, order_row)),
                            class_name="w-full text-sm",
                        ),
                        class_name="w-full overflow-x-auto",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-md border",
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
    )