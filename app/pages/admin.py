import reflex as rx
from app.state import MainState, Order, AdminState, OrderStatus
from app.components.navbar import navbar
from app.components.footer import footer

STATUS_COLORS: dict[str, str] = {
    "Pendiente": "bg-yellow-100 text-yellow-800",
    "Procesando": "bg-blue-100 text-blue-800",
    "Enviado": "bg-indigo-100 text-indigo-800",
    "Entregado": "bg-green-100 text-green-800",
    "Cancelado": "bg-red-100 text-red-800",
    "Revisión Solicitada": "bg-orange-100 text-orange-800",
}
ORDER_STATUSES: list[OrderStatus] = [
    "Pendiente",
    "Procesando",
    "Enviado",
    "Entregado",
    "Cancelado",
    "Revisión Solicitada",
]


def order_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "Detalles de la Orden #",
                        AdminState.selected_order.get("id", "").to_string(),
                        class_name="text-2xl font-bold",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Cliente: ",
                            rx.el.strong(
                                AdminState.selected_order.get("customer_email")
                            ),
                        ),
                        rx.el.p(
                            "Fecha: ",
                            rx.el.strong(AdminState.selected_order.get("created_at")),
                        ),
                        rx.el.p(
                            "Total: ",
                            rx.el.strong(f"${AdminState.selected_order.get('total')}"),
                        ),
                        rx.el.p(
                            "Estado: ",
                            rx.el.span(
                                AdminState.selected_order.get("status"),
                                class_name=STATUS_COLORS.get("Procesando")
                                + " px-2 py-1 rounded-full text-xs",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4 my-4 text-sm",
                    ),
                    rx.el.h3("Items:", class_name="font-semibold mb-2"),
                    rx.el.ul(
                        rx.foreach(
                            AdminState.selected_order.get("items", []),
                            lambda item: rx.el.li(
                                f"{item.get('quantity')}x Producto ID {item.get('product_id')} ({item.get('color')})"
                            ),
                        ),
                        class_name="list-disc list-inside text-sm text-gray-700",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cerrar",
                                class_name="mt-6 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg",
                            )
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="bg-white p-6 rounded-lg shadow-xl max-w-lg w-full",
                ),
                class_name="fixed inset-0 flex items-center justify-center z-50",
            ),
        ),
        open=AdminState.show_order_detail,
        on_open_change=AdminState.set_show_order_detail,
    )


def order_row(order: Order) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.button(
                f"#{order.get('id', 'N/A')}",
                on_click=AdminState.view_order_details(order),
                class_name="text-blue-600 hover:underline font-semibold",
            ),
            class_name="px-4 py-3 whitespace-nowrap",
        ),
        rx.el.td(order.get("customer_email"), class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(order.get("created_at"), class_name="px-4 py-3 whitespace-nowrap"),
        rx.el.td(
            "$" + order.get("total").to_string(), class_name="px-4 py-3 font-semibold"
        ),
        rx.el.td(
            rx.el.span(
                order.get("status"),
                class_name=STATUS_COLORS.get(order.get("status", ""), "")
                + " text-xs font-medium px-2.5 py-1 rounded-full",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.cond(
                    order.get("status") == "Pendiente",
                    rx.el.button(
                        rx.icon("check", class_name="h-4 w-4"),
                        on_click=AdminState.accept_order(order.get("id")),
                        class_name="p-1 bg-green-500 text-white rounded hover:bg-green-600",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    (order.get("status") != "Cancelado")
                    & (order.get("status") != "Entregado"),
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=AdminState.cancel_order(order.get("id")),
                        class_name="p-1 bg-red-500 text-white rounded hover:bg-red-600",
                    ),
                    rx.fragment(),
                ),
                rx.el.select(
                    rx.foreach(
                        ORDER_STATUSES,
                        lambda status: rx.el.option(status, value=status),
                    ),
                    value=order.get("status"),
                    on_change=lambda status: AdminState.change_order_status(
                        order.get("id"), status
                    ),
                    class_name="ml-2 text-xs rounded border-gray-300",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-b hover:bg-gray-50 text-sm",
    )


def admin() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Panel de Administrador", class_name="text-3xl font-bold mb-8"
                ),
                rx.el.div(
                    rx.el.h2("Filtros", class_name="text-xl font-semibold mb-4"),
                    rx.el.div(
                        rx.el.input(
                            type="date",
                            on_change=AdminState.set_filter_date_from,
                            class_name="p-2 border rounded-lg",
                        ),
                        rx.el.input(
                            type="date",
                            on_change=AdminState.set_filter_date_to,
                            class_name="p-2 border rounded-lg",
                        ),
                        rx.el.select(
                            rx.el.option("Todos los Clientes", value=""),
                            rx.foreach(
                                AdminState.unique_customers,
                                lambda customer: rx.el.option(customer, value=customer),
                            ),
                            on_change=AdminState.set_filter_customer,
                            value=AdminState.filter_customer,
                            class_name="p-2 border rounded-lg",
                        ),
                        rx.el.select(
                            rx.el.option("Todos los Estados", value=""),
                            rx.foreach(
                                ORDER_STATUSES,
                                lambda status: rx.el.option(status, value=status),
                            ),
                            on_change=AdminState.set_filter_order_status,
                            value=AdminState.filter_order_status,
                            class_name="p-2 border rounded-lg",
                        ),
                        rx.el.button(
                            "Limpiar Filtros",
                            on_click=AdminState.clear_filters,
                            class_name="bg-gray-300 px-4 py-2 rounded-lg",
                        ),
                        class_name="grid grid-cols-2 md:grid-cols-5 gap-4 items-end",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-md border mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2("Órdenes", class_name="text-2xl font-semibold mb-4"),
                        rx.el.div(
                            rx.el.span(
                                f"{AdminState.filtered_orders.length()} órdenes encontradas",
                                class_name="text-sm text-gray-600",
                            ),
                            rx.el.button(
                                rx.icon("download", class_name="mr-2"),
                                "Exportar",
                                on_click=MainState.export_orders,
                                class_name="flex items-center bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors",
                            ),
                            class_name="flex justify-between items-center mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th("ID", class_name="text-left px-4 py-3"),
                                    rx.el.th(
                                        "Cliente", class_name="text-left px-4 py-3"
                                    ),
                                    rx.el.th("Fecha", class_name="text-left px-4 py-3"),
                                    rx.el.th("Total", class_name="text-left px-4 py-3"),
                                    rx.el.th(
                                        "Estado", class_name="text-left px-4 py-3"
                                    ),
                                    rx.el.th(
                                        "Acciones", class_name="text-left px-4 py-3"
                                    ),
                                    class_name="bg-gray-100 border-b",
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(AdminState.paginated_orders, order_row)
                            ),
                            class_name="w-full text-sm",
                        ),
                        class_name="w-full overflow-x-auto",
                    ),
                    rx.el.div(
                        rx.el.p(
                            f"Página {AdminState.current_page} de {AdminState.total_pages}"
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Anterior",
                                on_click=AdminState.prev_page,
                                disabled=AdminState.current_page <= 1,
                                class_name="px-4 py-2 bg-gray-200 rounded-lg disabled:opacity-50",
                            ),
                            rx.el.button(
                                "Siguiente",
                                on_click=AdminState.next_page,
                                disabled=AdminState.current_page
                                >= AdminState.total_pages,
                                class_name="px-4 py-2 bg-gray-200 rounded-lg disabled:opacity-50",
                            ),
                            class_name="flex gap-2",
                        ),
                        class_name="flex justify-between items-center mt-4",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-md border",
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        order_detail_modal(),
        class_name="bg-gray-50 min-h-screen font-['Raleway']",
    )