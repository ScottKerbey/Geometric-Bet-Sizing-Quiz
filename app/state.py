import reflex as rx
import random
import logging


def calculate_geometric_bet(pot: float, stack: float, streets: int) -> float:
    """
    Calculates the optimal geometric bet size as a percentage of the pot.
    """
    if streets <= 0 or pot <= 0 or stack <= 0:
        return 0.0
    try:
        ratio = (pot + 2 * stack) / pot
        growth_factor = ratio ** (1 / streets)
        k = 0.5 * (growth_factor - 1)
    except (ValueError, ZeroDivisionError):
        logging.exception("Error calculating geometric bet")
        return 0.0
    return k * 100


class PokerState(rx.State):
    pot_size: float = 100.0
    stack_size: float = 500.0
    streets: int = 3
    correct_answer: float = 0.0
    user_guess: str = ""
    result_difference: float = 0.0
    show_result: bool = False
    loading: bool = True

    @rx.event
    def on_load(self):
        """Initial question generation on page load."""
        yield PokerState.generate_new_question

    @rx.event
    def generate_new_question(self):
        """Generates a new random poker scenario and calculates the answer."""
        self.show_result = False
        self.user_guess = ""
        self.pot_size = round(random.uniform(50, 200), 2)
        self.stack_size = round(
            random.uniform(self.pot_size * 1.5, self.pot_size * 5), 2
        )
        self.streets = random.randint(2, 3)
        self.correct_answer = calculate_geometric_bet(
            self.pot_size, self.stack_size, self.streets
        )
        self.loading = False

    @rx.event
    def check_answer(self):
        """Checks the user's guess against the correct answer."""
        if self.user_guess == "":
            return rx.toast.error("Please enter a guess.")
        try:
            guess = float(self.user_guess)
            self.result_difference = abs(guess - self.correct_answer)
            self.show_result = True
        except ValueError:
            logging.exception("Invalid user guess")
            self.user_guess = ""
            return rx.toast.error("Invalid input. Please enter a number.")