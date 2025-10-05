import reflex as rx
from app.state import PokerState


def _info_card(icon: str, title: str, value: rx.Var[str | int | float]) -> rx.Component:
    """A card to display a piece of scenario information."""
    return rx.el.div(
        rx.icon(icon, class_name="text-orange-500 w-6 h-6"),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-xl font-semibold text-gray-800"),
            class_name="flex-1",
        ),
        class_name="flex items-center gap-4 bg-gray-50 p-4 rounded-lg border border-gray-200",
    )


def _result_display() -> rx.Component:
    """Component to display the results after a guess."""
    return rx.el.div(
        rx.el.p("Results", class_name="text-lg font-semibold text-gray-800 mb-4"),
        rx.el.div(
            rx.el.div(
                rx.el.p("Your Guess:", class_name="font-medium text-gray-600"),
                rx.el.p(
                    f"{PokerState.user_guess}%",
                    class_name="font-bold text-xl text-orange-600",
                ),
                class_name="text-center p-4 bg-orange-50 rounded-lg",
            ),
            rx.el.div(
                rx.el.p("Correct Answer:", class_name="font-medium text-gray-600"),
                rx.el.p(
                    f"{PokerState.correct_answer:.2f}%",
                    class_name="font-bold text-xl text-green-600",
                ),
                class_name="text-center p-4 bg-green-50 rounded-lg",
            ),
            rx.el.div(
                rx.el.p("Difference:", class_name="font-medium text-gray-600"),
                rx.el.p(
                    f"{PokerState.result_difference:.2f}%",
                    class_name="font-bold text-xl text-blue-600",
                ),
                class_name="text-center p-4 bg-blue-50 rounded-lg",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
        ),
        class_name="w-full mt-8 p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
    )


def index() -> rx.Component:
    """The main page of the poker training app."""
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.icon("spade", class_name="w-10 h-10 text-orange-500 mb-4"),
                rx.el.h1(
                    "Geometric Bet Sizing Quiz",
                    class_name="text-3xl font-bold text-gray-800 tracking-tight",
                ),
                rx.el.p(
                    "Calculate the bet size (%) to go all-in by the river.",
                    class_name="text-gray-500 mt-2",
                ),
                class_name="text-center mb-8",
            ),
            rx.el.div(
                rx.cond(
                    PokerState.loading,
                    rx.el.div(
                        class_name="animate-pulse bg-gray-200 h-96 rounded-2xl w-full"
                    ),
                    rx.el.div(
                        rx.el.div(
                            _info_card(
                                icon="circle-dollar-sign",
                                title="Pot Size",
                                value=f"${PokerState.pot_size}",
                            ),
                            _info_card(
                                icon="layers",
                                title="Effective Stack",
                                value=f"${PokerState.stack_size}",
                            ),
                            _info_card(
                                icon="route",
                                title="Streets to Play",
                                value=PokerState.streets,
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Your Bet Size Guess (%)",
                                class_name="block text-sm font-medium text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                placeholder="e.g., 75.5",
                                on_change=PokerState.set_user_guess,
                                type="number",
                                class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-shadow",
                                default_value=PokerState.user_guess,
                            ),
                            class_name="w-full",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Next Question",
                                on_click=PokerState.generate_new_question,
                                class_name="w-full py-3 px-4 text-center font-semibold rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 transition-colors shadow-sm",
                            ),
                            rx.el.button(
                                "Check Answer",
                                on_click=PokerState.check_answer,
                                class_name="w-full py-3 px-4 text-center font-semibold rounded-lg bg-orange-500 text-white hover:bg-orange-600 transition-colors shadow-md hover:shadow-lg",
                            ),
                            class_name="grid grid-cols-2 gap-4 mt-8",
                        ),
                        rx.cond(
                            PokerState.show_result, _result_display(), rx.fragment()
                        ),
                        class_name="w-full",
                    ),
                ),
                class_name="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 w-full max-w-2xl",
            ),
            class_name="flex flex-col items-center justify-center p-4",
        ),
        class_name="min-h-screen bg-gray-50 font-['Open_Sans'] flex items-center justify-center",
        on_mount=PokerState.on_load,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)