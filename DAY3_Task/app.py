"""
Sweet Crumbs Home Bakery Assistant
Day 3 workshop task: LangChain + Groq + chat history + CSV tests.

The two bakery functions at the bottom are prepared for Day 4.
They are NOT connected to the LLM as tools yet.
"""
import csv
import os
from pathlib import Path
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

BASE_DIR = Path(__file__).resolve().parent
TEST_FILE = BASE_DIR / "test.csv"

# Business chosen: Sweet Crumbs Home Bakery
SYSTEM = """
You are the friendly and accurate customer-support assistant for
Sweet Crumbs Home Bakery.

BUSINESS DETAILS
- Plum cake: Rs 500
- Chocolate cake: Rs 650
- Cupcake: Rs 80 each
- Every cake is available in an eggless version.
- Customers must place cake orders at least 24 hours in advance.
- Delivery availability and delivery charges have not been confirmed.

RESPONSE RULES
1. Answer only using the business details above.
2. Never invent a price, discount, ingredient, stock status, delivery area,
   delivery charge, or delivery time.
3. If asked about a price, state the exact price. For quantities, calculate
   the total accurately (example: 6 cupcakes = Rs 480).
4. If asked for an eggless cake, clearly say that eggless versions are available.
5. If asked for same-day or urgent cake orders, clearly mention the
   24 hours' advance-notice requirement. Do not promise the order.
6. If asked about delivery, say: "I'll check with the owner."
7. If a detail is not provided, say: "I'll check with the owner."
8. Be friendly and concise (under 50 words). Do not claim an order is booked.
"""

def build_chain(temperature: float = 0.3):
    """Build a LangChain prompt -> Groq model -> string output pipeline."""
    if not os.getenv("GROQ_API_KEY"):
        raise EnvironmentError(
            "GROQ_API_KEY is missing. Set your Groq API key before running."
        )

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=temperature,
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()


class BakeryAssistant:
    """Chat assistant that remembers earlier messages during this run."""

    def __init__(self, temperature: float = 0.3):
        self.chain = build_chain(temperature)
        self.history = []

    def ask(self, question: str) -> str:
        """Send a question, return the answer, and save both in chat history."""
        answer = self.chain.invoke({
            "history": self.history,
            "question": question,
        })
        self.history.extend([
            ("human", question),
            ("ai", answer),
        ])
        return answer


def run_tests(chain, path: Path = TEST_FILE, run_label: str = "") -> tuple[int, int]:
    """Run all CSV checks and return the number passed and total."""
    if not path.exists():
        raise FileNotFoundError(f"Test CSV not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    passed = 0
    print(f"\nTEST RUN {run_label}".strip())
    print("=" * 72)

    for index, row in enumerate(rows, start=1):
        question = row["question"].strip()
        expected = row["must_include"].strip()
        answer = chain.invoke({"history": [], "question": question})
        success = expected.casefold() in answer.casefold()
        passed += int(success)

        print(f"{index}. {'PASS' if success else 'FAIL'}")
        print(f"Question : {question}")
        print(f"Expected : {expected}")
        print(f"Answer   : {answer}\n")

    total = len(rows)
    rate = (passed / total * 100) if total else 0
    print(f"PASS RATE: {passed}/{total} ({rate:.1f}%)")
    return passed, total


def temperature_experiment():
    """
    Run the same CSV tests twice at temperature 0.3 and twice at 1.0.
    Compare the pass rates and observe whether answer wording changes.
    """
    for temperature in (0.3, 1.0):
        print(f"\n{'#' * 72}\nTEMPERATURE = {temperature}\n{'#' * 72}")
        chain = build_chain(temperature)
        run_tests(chain, run_label=f"(temperature {temperature}, run 1)")
        run_tests(chain, run_label=f"(temperature {temperature}, run 2)")


# BEFORE DAY 4: functions that can later become agent tools.
# They are intentionally ordinary Python functions for now.

def price_lookup(item: str, quantity: int = 1) -> Optional[int]:
    """
    Return the total price in rupees for a known bakery item.

    Args:
        item: Bakery item name, such as 'plum cake', 'chocolate cake',
              or 'cupcake'.
        quantity: Number of items. Must be a positive integer.

    Returns:
        Total price in rupees, or None if the item is not in the price list.
    """
    prices = {
        "plum cake": 500,
        "chocolate cake": 650,
        "cupcake": 80,
    }
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    unit_price = prices.get(item.strip().casefold())
    return unit_price * quantity if unit_price is not None else None


def availability_check(order_date: str, hours_notice: int) -> str:
    """
    Check whether an order meets the bakery's 24-hour advance-notice rule.

    Args:
        order_date: A human-readable requested order date/time.
        hours_notice: Number of hours remaining before the requested time.

    Returns:
        A message explaining whether the notice requirement is met.

    Note:
        This checks only the notice rule, not actual stock or delivery.
    """
    if hours_notice < 0:
        raise ValueError("hours_notice cannot be negative")
    if hours_notice >= 24:
        return f"The 24-hour notice requirement is met for {order_date}."
    return (
        f"At least 24 hours' notice is required for {order_date}. "
        "Please check with the bakery before placing the order."
    )


def main():
    print("Sweet Crumbs Home Bakery Assistant")
    print("Commands: test | experiment | quit\n")

    assistant = BakeryAssistant(temperature=0.3)
    while True:
        question = input("You: ").strip()
        command = question.casefold()

        if command in {"quit", "exit"}:
            print("Assistant: Thank you for visiting Sweet Crumbs!")
            break
        if command == "test":
            run_tests(assistant.chain)
            continue
        if command == "experiment":
            temperature_experiment()
            continue
        if not question:
            continue

        try:
            print("Assistant:", assistant.ask(question), "\n")
        except Exception as error:
            print(f"An error occurred: {error}\n")


if __name__ == "__main__":
    main()
