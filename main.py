# import os
# import time
# from fpdf import FPDF
# # from playsound import playsound
# from intent.intent import classify_intent_cached
# from tarot.tarot_reader import cached_reading
# from voice.input import record_from_mic, transcribe_audio
# # from voice.output import synthesize_voice, play_voice_response
# from langdetect import detect
# from deep_translator import GoogleTranslator
# from user_info.user_info import collect_user_info  
# from utils.decorators import log_timing

# #  also in constant 
# def main():
#     print("\U0001f52e Welcome to TarotTara – your magical tarot guide (type 'exit' to quit)\n")
#     collect_user_info()

#     # Ask user for their preferred language
#     user_language = input("Please select your language (en, hi, es, fr): ").strip().lower()
#     print("\n✨ Thank you! How can I help you today?\n")

#     while True:
#         print("\n🎧 You may (1) Speak into mic, (2) Upload audio, or (3) Type your question.")
#         choice = input("Choose input method [1/2/3]: ").strip()

#         question = None
#         if choice == "1":
#             question = record_from_mic()
#             if not question:
#                 continue
#         elif choice == "2":
#             file_path = input("Enter path to audio file (.wav or .mp3): ").strip()
#             if not os.path.exists(file_path):
#                 print("❌ File not found. Please try again.")
#                 continue
#             print("🔁 Transcribing your audio...")
#             try:
#                 with open(file_path, "rb") as f:
#                     question = transcribe_audio(f)
#                     print(f"✅ You said: {question}")
#             except Exception as e:
#                 print(f"⚠️ Error transcribing audio: {e}")
#                 continue
#         elif choice == "3":
#             question = input("\n🧘 Ask your question:\n> ")
#         else:
#             print("❌ Invalid choice. Please select 1, 2 or 3.")
#             continue

#         if question.lower() in {"exit", "quit"}:
#             print("🌙 Farewell. Trust the journey ahead.")
#             break

#         total_start = time.time()

#         # Detect language and translate question to English if needed
#         from_lang = detect(question)
#         translated_question = GoogleTranslator(source='auto', target='en').translate(question) if from_lang != "en" else question
#         #  python decorator 
#         # Intent classification
#         intent_start = time.time()
#         intent = classify_intent_cached(translated_question)
#         intent_duration = time.time() - intent_start
#         print(f"\n✨ Intent detected: {intent} (in {intent_duration:.2f} sec)")

#         timed_cached_reading = log_timing("🔮 Tarot reading")(cached_reading)
#         result, prediction_duration = timed_cached_reading(translated_question, intent)

#         if "error" in result:
#             print(f"⚠️ Error: {result['error']}")
#             continue
#         # decorator in reading 
#         answer_en = result["interpretation"]

#         print("\n🔍 TarotTara says:")
#         #  crash problem 
#         if intent == "timeline":
#             card = result["card"]
#             date_range = result["date_range"]
#             print(f"Card: {card}")
#             print(f"Timeframe: {date_range[0].strftime('%B %#d')} – {date_range[1].strftime('%B %#d')}")
#         elif intent == "factual":
#             print("\nAnswer:")
#         else:
#             cards = result.get("cards", [])
#             print(f"Cards Drawn: {', '.join(cards)}")
    
#         # Translate back to user's preferred language
#         final_answer = GoogleTranslator(source='en', target=user_language).translate(answer_en) if user_language != "en" else answer_en
#         print(f"\n🕡 TarotTara ({user_language}):\n{final_answer}")

#         # Voice generation
#         # try:
#             # print("\n🔊 Speaking the response...")
#             # audio_path = synthesize_voice(final_answer, user_input_lang=user_language)

#             #play_voice_response(audio_path)
#         # except Exception as e:
#         #     print(f"⚠️ Error playing voice response: {e}")

#         total_duration = time.time() - total_start
#         print("\n⏱️ Timing Summary:")
#         print(f"• Intent classification: {intent_duration:.2f} sec")
#         print(f"• Prediction (LLM + RAG): {prediction_duration:.2f} sec")
#         print(f"• Total time: {total_duration:.2f} sec")

# if __name__ == "__main__":
#     main()

import time
import datetime
from langdetect import detect  # For detecting language
from translate import Translator  # For translation (alternative to GoogleTranslator)
from intent.intent import classify_intent_cached
from core.tarot_reader import cached_reading
from initialize.cache import get_cached, set_cached
from utils.voice_assistant import listen_for_question  # For voice input

# ——— Conversation history buffer ———
# keep last 6 turns (user + assistant)
conversation_history: list[tuple[str, str]] = []

def append_to_history(role: str, text: str):
    conversation_history.append((role, text))
    if len(conversation_history) > 6:
        conversation_history.pop(0)

# Function to format dates in the desired format
def format_date(dt: datetime.date) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"

# Function to detect language and translate to English if necessary
def detect_and_translate(input_text: str, target_language='en'):
    detected_language = detect(input_text)
    if detected_language != target_language:
        translator = Translator(to_lang=target_language)
        translated_text = translator.translate(input_text)
        return translated_text, detected_language
    else:
        return input_text, detected_language

# Function to translate the result back to the user's language
def translate_back(result_text: str, target_language: str):
    if target_language == 'en':
        return result_text
    translator = Translator(to_lang=target_language)
    return translator.translate(result_text)

def main():
    print("🔮 Welcome to TarotTara – your magical tarot guide!")
    # (Optional) let user choose a display language up front
    language_choice = input("Please select your language (en, hi, es, fr): ").strip().lower()

    while True:
        # 1️⃣ Choose input method
        method = input("\nDo you want to enter your question by voice or chat? (voice/chat): ").strip().lower()
        if method == 'voice':
            print("🎙️ Listening for your question...")
            question = listen_for_question() or ""
        else:
            question = input("\n🧘 Ask your question:\n> ").strip()

        if not question:
            continue
        if question.lower() in {'exit', 'quit'}:
            print("🌙 Farewell. Trust the journey ahead.")
            break

        # 2️⃣ Record user turn in history
        append_to_history("user", question)

        # 3️⃣ Detect & translate user question to English
        translated_q, detected_lang = detect_and_translate(question, target_language='en')
        print(f"\n✨ Detected language: {detected_lang} (processing in English)")

        # 4️⃣ Try cache
        cached = get_cached(question)
        if cached:
            print("🧠 Serving from Redis cache!")
            result = cached
            intent = result.get("intent", "general")
        else:
            start_total = time.time()

            # 5️⃣ Intent classification
            t0 = time.time()
            intent = classify_intent_cached(translated_q)
            dt_intent = time.time() - t0
            print(f"\n✨ Intent detected: {intent} (in {dt_intent:.2f}s)")

            # 6️⃣ Perform reading / conversation / polite factual
            t1 = time.time()
            result = cached_reading(translated_q, intent, conversation_history)
            dt_read = time.time() - t1
            total_time = time.time() - start_total

            if "error" in result:
                print(f"⚠️ Error: {result['error']}")
                continue

            # 7️⃣ Store intent + serialize dates
            result["intent"] = intent
            if dr := result.get("date_range"):
                result["date_range"] = [dr[0].isoformat(), dr[1].isoformat()]

            # 8️⃣ Cache fresh result
            set_cached(question, result)

        # 9️⃣ Record assistant turn in history
        append_to_history("assistant", result["interpretation"])

        # 🔟 Display
        print("\n🔍 TarotTara says:")
        # Build a single result_text for translation
        if intent == "factual":
            result_text = "Sorry, I cannot provide factual information at the moment. Please ask a tarot-related question."
        elif intent == "conversation":
            result_text = result["interpretation"]
        elif intent == "timeline" and result.get("card"):
            card = result["card"]
            ds_iso, de_iso = result["date_range"]
            ds = datetime.date.fromisoformat(ds_iso)
            de = datetime.date.fromisoformat(de_iso)
            result_text = (
                f"Card: {card}\n"
                f"Timeframe: {format_date(ds)} – {format_date(de)}\n\n"
                f"{result['interpretation']}"
            )
        else:
            # guidance, insight, yes_no, or general 3-card
            if cards := result.get("cards"):
                result_text = f"Cards Drawn: {', '.join(cards)}\n\n{result['interpretation']}"
            else:
                result_text = result["interpretation"]

        # Print English (or untranslated) version
        print(f"\n{result_text}")

        # ⓫ Translate back and show
        back = translate_back(result_text, detected_lang)
        if detected_lang != 'en':
            print(f"\nResult in {detected_lang}:\n{back}")

        # ⓬ Timing summary if fresh
        if not cached:
            print("\n⏱️ Timing Summary:")
            print(f" • Intent classification: {dt_intent:.2f}s")
            print(f" • Prediction (LLM + RAG): {dt_read:.2f}s")
            print(f" • Total: {total_time:.2f}s")

    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
