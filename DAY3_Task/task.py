"""Day 3 Task: Sweet Crumbs Home Bakery Assistant.

Install:
    python -m pip install langchain langchain-core langchain-groq

PowerShell:
    $env:GROQ_API_KEY="YOUR_GROQ_API_KEY"

Run:
    python task.py

Commands inside the program: test, experiment, examples, quit.
"""
import os
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


# 1. Improved system prompt
SYSTEM = """
You are a friendly customer-support assistant for Sweet Crumbs Home Bakery.

BUSINESS DETAILS
- Plum cake: Rs 500
- Chocolate cake: Rs 650
- Cupcake: Rs 80 each
- Every cake is available in an eggless version.
- Cake orders require at least 24 hours' advance notice.
- Delivery availability and charges are not confirmed.

RULES
1. Answer only using the details above.
2. Never invent prices, discounts, stock, delivery areas, charges, or times.
3. State exact prices and calculate quantities accurately. Six cupcakes cost Rs 480.
4. Clearly say eggless versions are available when asked.
5. For urgent orders, mention the 24-hour advance-notice rule. Never promise an order.
6. For delivery questions or unknown information, say:
   "I'll check with the owner."
7. Be friendly and concise. Never claim an order is booked.
"""


def build_chain(temperature: float = 0.3):
    """Create a LangChain prompt -> Groq model -> text output chain."""
    if not os.getenv("GROQ_API_KEY"):
        raise EnvironmentError("GROQ_API_KEY is missing. Set your Groq API key.")

    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=temperature)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()


# 2. Chatbot with chat history
class BakeryAssistant:
    """Remembers messages during the current program session."""

    def __init__(self, temperature: float = 0.3):
        self.chain = build_chain(temperature)
        self.history = []

    def ask(self, question: str) -> str:
        answer = self.chain.invoke({
            "history": self.history,
            "question": question,
        })
        self.history.extend([("human", question), ("ai", answer)])
        return answer


# 3. Ten customer test cases (embedded; no separate CSV required)
TEST_CASES = [
    ("How much is a plum cake?", "Rs 500"),
    ("What is the price of a chocolate cake?", "Rs 650"),
    ("How much does one cupcake cost?", "Rs 80"),
    ("What is the price of 6 cupcakes?", "Rs 480"),
    ("Do you make eggless cakes?", "eggless"),
    ("Can I order an eggless chocolate cake?", "eggless"),
    ("Can I get a cake today evening?", "24 hours"),
    ("Can I place an order just 5 hours before pickup?", "24 hours"),
    ("Do you deliver to Kakinada?", "I'll check with the owner."),
    ("How much is delivery to my home?", "I'll check with the owner."),
]


def run_tests(chain, label: str = ""):
    """Run all ten tests and calculate the actual pass rate."""
    passed = 0
    print(f"\\nTEST RESULTS {label}\\n" + "=" * 60)
    for number, (question, expected) in enumerate(TEST_CASES, 1):
        answer = chain.invoke({"history": [], "question": question})
        success = expected.casefold() in answer.casefold()
        passed += int(success)
        print(f"\\n{number}. {'PASS' if success else 'FAIL'}")
        print("Question:", question)
        print("Expected:", expected)
        print("Answer:", answer)

    rate = passed / len(TEST_CASES) * 100
    print(f"\\nPASS RATE: {passed}/{len(TEST_CASES)} ({rate:.1f}%)")
    return passed, len(TEST_CASES)


# 4. Temperature experiment: two runs at each temperature
def temperature_experiment():
    for temperature in (0.3, 1.0):
        chain = build_chain(temperature)
        run_tests(chain, f"(temperature {temperature}, run 1)")
        run_tests(chain, f"(temperature {temperature}, run 2)")


# 5. Two ordinary Python functions prepared for Day 4
def price_lookup(item: str, quantity: int = 1) -> Optional[int]:
    """Return the total price, or None if the item is unknown."""
    prices = {"plum cake": 500, "chocolate cake": 650, "cupcake": 80}
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    unit_price = prices.get(item.strip().casefold())
    return None if unit_price is None else unit_price * quantity


def availability_check(order_date: str, hours_notice: int) -> str:
    """Check only the bakery's 24-hour advance-notice requirement."""
    if hours_notice < 0:
        raise ValueError("hours_notice cannot be negative")
    if hours_notice >= 24:
        return f"The 24-hour notice requirement is met for {order_date}."
    return (
        f"At least 24 hours' notice is required for {order_date}. "
        "Please check with the bakery before placing the order."
    )


# 6. Three agent-or-not examples
def show_examples():
    print("""
1. Display the fixed cupcake price from a Python dictionary.
   Plain code: fixed lookup; no language understanding is needed.

2. Reply politely to 'Do you make eggless cakes?' using the LLM.
   LLM call: understands the wording and generates a natural response.

3. Understand a multi-step customer request, choose the required business
   functions, call them, and use their results.
   Agent: decides which tools/actions are needed.

This Day 3 project is an LLM chain with chat history, not yet a
tool-using agent. The two Python functions are prepared for Day 4.
""")


def main():
    print("Sweet Crumbs Home Bakery — Day 3 Assistant")
    print("Commands: test | experiment | examples | quit")
    assistant = BakeryAssistant(temperature=0.3)

    while True:
        question = input("\\nYou: ").strip()
        command = question.casefold()

        if command in {"quit", "exit"}:
            print("Thank you for visiting Sweet Crumbs!")
            break
        if command == "test":
            run_tests(assistant.chain)
        elif command == "experiment":
            temperature_experiment()
        elif command == "examples":
            show_examples()
        elif question:
            try:
                print("Assistant:", assistant.ask(question))
            except Exception as error:
                print("Error:", error)


if __name__ == "__main__":
    main()
