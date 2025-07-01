import random

MAJOR = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant",
         "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man",
         "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
SUITS = {
    "Wands":      [f"{i} of Wands"      for i in range(1, 11)],
    "Cups":       [f"{i} of Cups"       for i in range(1, 11)],
    "Swords":     [f"{i} of Swords"     for i in range(1, 11)],
    "Pentacles":  [f"{i} of Pentacles"  for i in range(1, 11)]
}
COURTS = [f"{r} of {s}" for s in SUITS for r in ["Page", "Knight", "Queen", "King"]]
FULL_DECK = MAJOR + SUITS["Wands"] + SUITS["Cups"] + SUITS["Swords"] + SUITS["Pentacles"] + COURTS
DECCAN_DECK = SUITS["Wands"] + SUITS["Cups"] + SUITS["Swords"] + SUITS["Pentacles"]

YOUR_ENERGY_MAP = {
    "buy property": {
        "Year1": ["Ace of Cups", "3 of Pentacles"],
        "Year2": ["4 of Wands", "The World"]
    }
}
WEEKS_IN_MONTH = {i: 4 for i in range(1, 13)}
YOUR_DECCAN_MAP = {c: (random.randint(1, 12), random.randint(1, 4), random.randint(1, 7)) for c in DECCAN_DECK}

def draw(cards, n=1):
    return random.sample(cards, n)

def is_open_ended(question):
    keywords = ["love", "relationship", "luck", "health", "happiness", "money", "career", "success", "growth"]
    q = question.lower()
    return any(kw in q for kw in keywords)

def year_determination(question):
    open_ended = is_open_ended(question)
    cards = draw(FULL_DECK, 2)
    if not open_ended:
        return "Year1"
    year = None
    for y in ["Year1", "Year2"]:
        if any(card in YOUR_ENERGY_MAP.get(question, {}).get(y, []) for card in cards):
            year = y
            break
    if year is None:
        cards = draw(FULL_DECK, 1)
        for y in ["Year1", "Year2"]:
            if any(card in YOUR_ENERGY_MAP.get(question, {}).get(y, []) for card in cards):
                year = y
                break
    return year

def monthly_spread(current_month):
    months_left = 12 - current_month + 1
    sig = "Wheel of Fortune"
    pool = [sig] + draw([c for c in FULL_DECK if c != sig], months_left - 1)
    random.shuffle(pool)
    return current_month + pool.index(sig)

def weekly_spread(month):
    weeks = WEEKS_IN_MONTH.get(month, 4)
    sig = "Wheel of Fortune"
    pool = [sig] + draw([c for c in FULL_DECK if c != sig], weeks - 1)
    random.shuffle(pool)
    return pool.index(sig) + 1

def deccan_timing():
    card = draw(DECCAN_DECK, 1)[0]
    return YOUR_DECCAN_MAP.get(card, ("Unknown", "Unknown", "Unknown"))

def predict_timeline(question, current_month):
    year = year_determination(question)
    if not year:
        return {"error": "No energies in next 2 years"}
    month = monthly_spread(current_month)
    week = weekly_spread(month)
    exact = deccan_timing()
    return {"year": year, "month": month, "week": week, "exact": exact}

if __name__ == "__main__":
    question = input("Enter your question: ")
    current_month = int(input("Enter current month (1-12): "))
    result = predict_timeline(question, current_month)
    print(result)
