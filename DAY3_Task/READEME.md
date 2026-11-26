# Sweet Crumbs Home Bakery Assistant — Day 3 Workshop

A beginner-friendly LangChain + Groq chatbot for **Sweet Crumbs Home Bakery**.
It includes chat history, 10 CSV test questions, a prompt-improvement task,
a temperature experiment, and two ordinary Python functions prepared for Day 4.

## Project structure

```text
sweet_crumbs_langchain/
├── app.py
├── test.csv
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 1. Setup (Windows PowerShell)

Open VS Code terminal inside this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt and run:
` .venv\Scripts\activate.bat `

Set your Groq API key in the current PowerShell window:

```powershell
$env:GROQ_API_KEY="YOUR_REAL_GROQ_API_KEY"
```

Get your key from the official Groq console. Do not paste the key into `app.py`
or upload it to GitHub.

## 2. Start the chatbot

```powershell
python app.py
```

Try:
- How much is a plum cake?
- Do you make eggless cakes?
- What is the price of 6 cupcakes?
- Can I get a cake today evening?
- Do you deliver to Kakinada?

Type `quit` to stop. Type `test` to run all 10 CSV test cases.
Type `experiment` to run the temperature comparison.

## 3. Business system prompt

The `SYSTEM` prompt in `app.py` was rewritten for Sweet Crumbs Home Bakery.
It contains the business prices, eggless-cake information, the 24-hour notice
rule, and safe handling of unknown delivery details. It tells the assistant
not to invent information or claim that an order is confirmed.

## 4. Customer tests and pass rate

`test.csv` contains 10 customer questions. Each row has:
- `question`: the customer's question
- `must_include`: the phrase that must appear in the answer

Run `test` in the chatbot. The program prints PASS or FAIL for each question
and calculates:

`Pass rate = (number of passed tests / 10) * 100`

Record your actual pass rate after running it with your API key. LLM outputs
can vary, so do not write a made-up pass rate in your submission.

## 5. Improve the prompt

One improvement made here: the prompt now gives explicit rules for each
business fact and tells the assistant exactly what to say when delivery or
other unknown information is requested. It also gives a quantity example:
6 cupcakes = Rs 480.

Run `test` before and after changing the prompt. Compare the pass rates and
note which test cases improved or failed.

## 6. Temperature experiment

The default assistant uses temperature `0.3`. Type `experiment` to run the
same ten tests twice at temperature `0.3` and twice at temperature `1.0`.

Record:
- pass rate for run 1 at 0.3
- pass rate for run 2 at 0.3
- pass rate for run 1 at 1.0
- pass rate for run 2 at 1.0

Temperature 1.0 may produce more varied wording. It does not guarantee a
higher pass rate. The exact results require running with your own API key.

## 7. Agent or not? Three bakery jobs

| Bakery job | Type | Reason |
|---|---|---|
| Show the fixed price of one cupcake using a normal Python dictionary/function | Plain code | The answer is fixed and needs no language understanding. |
| Reply politely to “Do you make eggless cakes?” using the LLM | LLM call | The model understands the customer's wording and forms a natural reply. |
| Check stock, calculate an order, and then arrange the next step by choosing and calling the right business functions | Agent | It can decide which tools/actions are needed to complete a multi-step task. |

This Day 3 chatbot is an **LLM chain with chat history**, not a full
tool-using agent yet. It does not autonomously call the bakery functions.

## 8. Before Day 4: two Python functions

At the bottom of `app.py`:
- `price_lookup(item, quantity=1)` returns a known total price in rupees.
- `availability_check(order_date, hours_notice)` checks the 24-hour notice rule.

Both functions have type hints and docstrings. They are ordinary Python
functions for now; tomorrow they can be connected as agent tools.

Example checks (optional, from the project folder):

```powershell
python -c "from app import price_lookup, availability_check; print(price_lookup('cupcake', 6)); print(availability_check('today evening', 5))"
```

Expected first result: `480`.

## 9. Push to GitHub

Create an empty repository on GitHub. Then run these commands from this folder:

```powershell
git init
git add .
git commit -m "Complete Day 3 bakery assistant workshop"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the example remote URL with your own GitHub repository URL.

**Important:** I cannot report live Groq test results without your API key and
an actual API run. Run `test` and `experiment`, then add your real pass-rate
observations to your workshop notes.
