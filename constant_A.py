import re

def instruction_for_intent_classification(question): 
    return [
        {
            "role": "system",
            "content": (
                "You are an expert tarot assistant. Classify the user's tarot question into **ONE** of the following intents:\n\n"
                "INTENT CATEGORIES:\n"
                "- yes_no → User expects a Yes/No answer. Includes questions like 'Should I…', 'Will I…'.\n"
                "- comparison → User compares two options. Often contains the word 'or'.\n"
                "- timeline → Question involves 'when' something will happen.\n"
                "- insight → User seeks meaning or hidden understanding.\n"
                "- advice → User asks for advice or next steps.\n"
                "- general → None of the above clearly apply.\n\n"
                "Reply with ONLY the intent name. No explanation.\n\n"
                "Examples:\n"
                "Q: Will I get promoted this year?\nA: yes_no\n"
                "Q: Should I quit my job?\nA: yes_no\n"
                "Q: When will I meet my soulmate?\nA: timeline\n"
                "Q: Should I choose MBA or a startup?\nA: comparison\n"
                "Q: What does this situation mean for me?\nA: insight\n"
                "Q: What should I do next in my relationship?\nA: advice\n"
                "Q: What is this about?\nA: general"
            )
        },
        {"role": "user", "content": f"Q: {question}\nA:"},
    ]


def response_gen_prompt(user_input, intent, card_text):
    return (
        "You are a wise and friendly tarot reader. Use your understanding of tarot symbolism to answer.\n\n"
        f"User's question: {user_input}\n"
        f"Intent: {intent}\n"
        f"Cards drawn:\n{card_text}\n\n"
        "Respond with:\n"
        "- A clear and insightful answer, based on the intent.\n"
        "- If intent is 'yes_no', give a definite answer.\n"
        "- If 'timeline', estimate when.\n"
        "- If 'insight', explain hidden meaning.\n"
        "- If 'advice', offer practical advice.\n"
        "- If 'comparison', analyze both options.\n"
        "- Be conversational but precise. Avoid vague or repetitive replies."
    )

def response_gen_prompt_for_general(user_input):
    return (
        "You are a wise and friendly tarot reader. Use your understanding of tarot symbolism to answer.\n\n"
        f"User's question: {user_input}\n"
        "Intent: general\n"
        "Cards drawn: No cards were drawn because the question was too general.\n\n"
        "Respond with:\n"
        "- A follow-up question to clarify the user's intent.\n"
        "- Be conversational but precise. Avoid vague or repetitive replies."
    )
