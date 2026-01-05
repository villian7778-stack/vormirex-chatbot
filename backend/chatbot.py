# from backend.config import CONTACT_NUMBER
# from backend.prompts import SYSTEM_PROMPT
# from backend.intent import detect_intent

# import requests
# from backend.config import (
#     OPENROUTER_API_KEY,
#     OPENROUTER_MODEL,
#     CONTACT_NUMBER
# )
# from backend.prompts import SYSTEM_PROMPT
# from backend.intent import detect_intent


# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# def call_openrouter(user_message):
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://vormirex.ai",
#         "X-Title": "Vormirex Chatbot"
#     }

#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": [
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_message}
#         ],
#         "max_tokens": 120,
#         "temperature": 0.3
#     }

#     response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
#     return response.json()["choices"][0]["message"]["content"]


# def chatbot_reply(user_message: str):
#     intent = detect_intent(user_message)

#     if intent == "FEES":
#         return f"Our team will explain fees clearly. Please contact 📞 {CONTACT_NUMBER}."

#     if intent == "CONTENT":
#         return f"Our mentors can guide you personally. Please call 📞 {CONTACT_NUMBER}."

#     if intent == "LEAD":
#         return "Great 😊 Please share your name and phone number."

#     return call_openrouter(user_message)

# import re
# import requests
# from datetime import datetime

# from backend.config import (
#     OPENROUTER_API_KEY,
#     OPENROUTER_MODEL,
#     CONTACT_NUMBER
# )
# from backend.prompts import SYSTEM_PROMPT
# from backend.intent import detect_intent
# from backend.google_sheets import save_lead   # ✅ IMPORTANT


# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# # -------------------------------
# # OpenRouter GPT Call
# # -------------------------------
# def call_openrouter(user_message: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://vormirex.ai",
#         "X-Title": "Vormirex Chatbot"
#     }

#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": [
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_message}
#         ],
#         "max_tokens": 120,
#         "temperature": 0.3
#     }

#     response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
#     response.raise_for_status()

#     return response.json()["choices"][0]["message"]["content"]


# # -------------------------------
# # Main Chatbot Logic
# # -------------------------------
# def chatbot_reply(user_message: str) -> str:
#     intent = detect_intent(user_message)

#     # 1️⃣ Fee-related intent
#     if intent == "FEES":
#         return (
#             f"Our team will explain the fee structure clearly 😊\n"
#             f"Please contact 📞 {CONTACT_NUMBER}."
#         )

#     # 2️⃣ Course / content intent
#     if intent == "CONTENT":
#         return (
#             f"Our mentors will guide you personally 📘\n"
#             f"Please contact 📞 {CONTACT_NUMBER}."
#         )

#     # 3️⃣ Lead intent (ask for details)
#     if intent == "LEAD":
#         return "Great 😊 Please share your *name and 10-digit phone number*."

#     # 4️⃣ Detect name + phone number automatically
#     phone_match = re.search(r"\b\d{10}\b", user_message)

#     if phone_match:
#         phone = phone_match.group()
#         name = user_message.replace(phone, "").strip()

#         # Safety fallback
#         if not name:
#             name = "Unknown"

#         # ✅ SAVE TO GOOGLE SHEET
#         save_lead(
#             name=name,
#             phone=phone,
#             source="Vormirex Chatbot"
#         )

#         return (
#             f"Thank you {name}! 🙌\n\n"
#             "Your details have been saved successfully.\n"
#             "Our team will contact you shortly with complete course information.\n\n"
#             "Is there anything else I can help you with?"
#         )

#     # 5️⃣ Default → GPT handles normal chat
#     return call_openrouter(user_message)





# import requests
# import re

# from backend.config import (
#     OPENROUTER_API_KEY,
#     OPENROUTER_MODEL,
#     CONTACT_NUMBER
# )
# from backend.prompts import SYSTEM_PROMPT
# from backend.intent import detect_intent
# from backend.google_sheets import save_lead


# OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# # -----------------------------
# # OpenRouter LLM Call
# # -----------------------------
# def call_openrouter(user_message: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://vormirex.ai",
#         "X-Title": "Vormirex Chatbot"
#     }

#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": [
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_message}
#         ],
#         "max_tokens": 180,
#         "temperature": 0.3
#     }

#     response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
#     response.raise_for_status()
#     return response.json()["choices"][0]["message"]["content"]


# # -----------------------------
# # Utility: Extract Name & Phone
# # -----------------------------
# def extract_lead(text: str):
#     phone_match = re.search(r"\b[6-9]\d{9}\b", text)
#     phone = phone_match.group() if phone_match else None

#     if phone:
#         name = text.replace(phone, "").strip().title()
#         name = name if len(name.split()) <= 4 else None
#     else:
#         name = None

#     return name, phone


# # -----------------------------
# # Main Chatbot Logic
# # -----------------------------
# def chatbot_reply(user_message: str) -> str:
#     msg = user_message.lower().strip()
#     intent = detect_intent(user_message)

#     # 1️⃣ SAVE LEAD (highest priority)
#     name, phone = extract_lead(user_message)
#     if name and phone:
#         save_lead(
#             name=name,
#             phone=phone,
#             source="Vormirex Website Chatbot"
#         )
#         return (
#             f"Thank you, *{name}* 🙏\n\n"
#             "Your details have been saved successfully.\n"
#             "Our Vormirex counselor will contact you shortly to guide you personally.\n\n"
#             "Meanwhile, feel free to ask me anything about our courses 😊"
#         )

#     # 2️⃣ Greeting
#     if intent == "GREETING":
#         return (
#             "Hello 👋 I’m *vormi*, your AI education counselor from *Vormirex*.\n\n"
#             "I’m here to help you with:\n"
#             "📘 Data Science course details\n"
#             "🔐 Cyber Security course details\n"
#             "🎯 Career & interview preparation\n\n"
#             "Which course would you like to explore today?"
#         )

#     # 3️⃣ Course List
#     if "course" in msg or "courses" in msg:
#         return (
#             "At Vormirex, we currently offer two industry-focused programs 🚀\n\n"
#             "📘 *Data Science*\n"
#             "🔐 *Cyber Security*\n\n"
#             "Both programs include live training, hands-on practice, and career guidance.\n"
#             "Please tell me which course you’re interested in 😊"
#         )

#     # 4️⃣ Data Science Course
#     if "data science" in msg:
#         return (
#             "📘 *Data Science Course at Vormirex*\n\n"
#             "🔹 *What you will learn:*\n"
#             "- Python, SQL & Statistics\n"
#             "- Machine Learning & basic AI\n"
#             "- Real-world data analysis projects\n\n"
#             "🔹 *How we teach:*\n"
#             "- Live mentor-led classes\n"
#             "- Hands-on coding practice\n"
#             "- Practical assignments & projects\n\n"
#             "🔹 *Career preparation:*\n"
#             "- Interview-ready questions\n"
#             "- Resume & project guidance\n"
#             "- Regular doubt-clearing sessions\n\n"
#             "Would you like to know about *duration*, *syllabus*, or *job roles*?"
#         )

#     # 5️⃣ Cyber Security Course
#     if "cyber" in msg or "security" in msg:
#         return (
#             "🔐 *Cyber Security Course at Vormirex*\n\n"
#             "🔹 *What you will learn:*\n"
#             "- Networking & security fundamentals\n"
#             "- Ethical hacking concepts\n"
#             "- Threat detection & prevention\n\n"
#             "🔹 *How we teach:*\n"
#             "- Practical labs & live demos\n"
#             "- Real-world attack scenarios\n"
#             "- Mentor-guided learning\n\n"
#             "🔹 *Career preparation:*\n"
#             "- Certification guidance\n"
#             "- Interview & exam preparation\n"
#             "- Dedicated doubt-clearing sessions\n\n"
#             "Would you like to know about *certifications* or *career scope*?"
#         )

#     # 6️⃣ Teaching Method
#     if "teach" in msg or "training" in msg or "class" in msg:
#         return (
#             "At Vormirex, we strongly believe in *learning by doing* 🧠💻\n\n"
#             "✅ Live mentor-led sessions\n"
#             "✅ Hands-on practical training\n"
#             "✅ Real-world projects\n"
#             "✅ Regular doubt-clearing sessions\n"
#             "✅ Interview & exam preparation\n\n"
#             "Our goal is to make you *job-ready*, not just theory-ready."
#         )

#     # 7️⃣ Lead Intent (ask politely)
#     if intent == "LEAD":
#         return (
#             "That’s great to hear 😊\n\n"
#             "Please share your *name* and *phone number*, and our team will guide you personally."
#         )

#     # 8️⃣ Fees / Contact
#     if intent == "FEES":
#         return (
#             "Our counselor will explain the fee structure clearly and transparently 😊\n\n"
#             f"You can also contact us directly at 📞 {CONTACT_NUMBER}"
#         )

#     # 9️⃣ Default Fallback (LLM)
#     return call_openrouter(user_message)


# import re
# import difflib
# from backend.google_sheets import save_lead
# from backend.config import CONTACT_NUMBER

# # ---------------------------
# # In-memory session storage
# # ---------------------------
# SESSIONS = {}

# # ---------------------------
# # Utilities
# # ---------------------------
# def extract_phone(text):
#     # Return a contiguous digit sequence if present (7-13 digits). Caller
#     # will validate exact length/format. This helps handle typos and spaced
#     # numbers like '87886 52485' or slightly-short inputs.
#     digits = re.sub(r"\D", "", text)
#     match = re.search(r"\d{7,13}", digits)
#     return match.group() if match else None


# def is_valid_phone(phone: str) -> bool:
#     # Strict validation: 10 digits starting with 6-9 (common mobile pattern).
#     return bool(re.fullmatch(r"[6-9]\d{9}", phone))

# def extract_name(text):
#     # Remove digit sequences that look like phone numbers, then keep alphabetic
#     # characters. Limit to short names (<= 3 words).
#     text = re.sub(r"\d{7,13}", "", text)
#     text = re.sub(r"[^a-zA-Z ]", "", text).strip()
#     return text.title() if text and len(text.split()) <= 3 else None

# # ---------------------------
# # Chatbot Logic
# # ---------------------------
# def chatbot_reply(user_id: str, user_message: str):
#     msg = user_message.lower().strip()

#     # Create session if not exists
#     if user_id not in SESSIONS:
#         SESSIONS[user_id] = {
#             "name": None,
#             "phone": None,
#             "lead_saved": False,
#             "course_selected": None,
#             "waiting_for_other_course": False
#         }

#     session = SESSIONS[user_id]

#     # If user selected "Other" and is waiting for course input
#     if session.get("waiting_for_other_course"):
#         # Capture their course input
#         other_course = user_message.strip()
#         if other_course and len(other_course) > 2:  # Ensure it's a meaningful input
#             session["course_selected"] = other_course
#             save_lead(
#                 name=session["name"],
#                 phone=session["phone"],
#                 course=other_course,
#                 source="Chatbot"
#             )
#             session["lead_saved"] = True
#             session["waiting_for_other_course"] = False
#             return {
#                 "reply": (
#                     f"Thank you! 🙏 We've noted your interest in *{other_course}*.\n\n"
#                     f"Our counselors will reach out shortly to provide you with detailed information.\n\n"
#                     f"📞 You can also contact us directly if you'd like to discuss further!"
#                 )
#             }
#         else:
#             return {"reply": "Please provide a valid course name (e.g., Web Development, AI, etc.)"}

#     # If lead already saved, handle course selection first
#     if session.get("lead_saved"):
#         # Check for fee/pricing inquiries
#         if any(keyword in msg for keyword in ["fee", "price", "cost", "charge", "payment", "fee structure", "pricing", "charges"]):
#             return {
#                 "reply": (
#                     f"Great question! 💰\n\n"
#                     f"Our counselors will explain the fee structure clearly and transparently.\n\n"
#                     f"📞 Please contact us: *{CONTACT_NUMBER}*\n\n"
#                     f"Our team will connect with you shortly to discuss fees, payment plans, and scholarships!"
#                 )
#             }
        
#         # Allow front-end button ids as well as fuzzy text matches
#         if msg in ["data_science", "data science", "data"]:
#             session["course_selected"] = "Data Science"
#             # Update Google Sheets with course selection
#             save_lead(
#                 name=session["name"],
#                 phone=session["phone"],
#                 source="Chatbot - Course Selected",
#                 course="Data Science"
#             )
#             return {
#                 "reply": (
#                     "📘 *Data Science Course*\n\n"
#                     "✔ Python, SQL, ML & AI\n"
#                     "✔ Real-world projects\n"
#                     "✔ Interview preparation\n"
#                     "✔ Live mentor-led sessions\n\n"
#                     "Ask me about syllabus, career roles, or fees! 😊"
#                 )
#             }

#         if msg in ["cyber_security", "cyber security", "cyber", "security"]:
#             session["course_selected"] = "Cyber Security"
#             # Update Google Sheets with course selection
#             save_lead(
#                 name=session["name"],
#                 phone=session["phone"],
#                 source="Chatbot - Course Selected",
#                 course="Cyber Security"
#             )
#             return {
#                 "reply": (
#                     "🔐 *Cyber Security Course*\n\n"
#                     "✔ Networking & Ethical Hacking\n"
#                     "✔ Practical labs\n"
#                     "✔ Certification guidance\n"
#                     "✔ Interview preparation\n\n"
#                     "Ask me about certifications, career scope, or fees! 😊"
#                 )
#             }

#         # fuzzy match common typos like 'dara science' -> 'data science'
#         choices = ["data science", "cyber security"]
#         close = difflib.get_close_matches(msg, choices, n=1, cutoff=0.5)
#         if close:
#             choice = close[0]
#             if choice == "data science":
#                 session["course_selected"] = "Data Science"
#                 save_lead(
#                     name=session["name"],
#                     phone=session["phone"],
#                     source="Chatbot - Course Selected",
#                     course="Data Science"
#                 )
#                 return {
#                     "reply": (
#                         "📘 *Data Science Course*\n\n"
#                         "✔ Python, SQL, ML & AI\n"
#                         "✔ Real-world projects\n"
#                         "✔ Interview preparation\n"
#                         "✔ Live mentor-led sessions\n\n"
#                         "Ask me about syllabus, career roles, or fees! 😊"
#                     )
#                 }
#             if choice == "cyber security":
#                 session["course_selected"] = "Cyber Security"
#                 save_lead(
#                     name=session["name"],
#                     phone=session["phone"],
#                     source="Chatbot - Course Selected",
#                     course="Cyber Security"
#                 )
#                 return {
#                     "reply": (
#                         "🔐 *Cyber Security Course*\n\n"
#                         "✔ Networking & Ethical Hacking\n"
#                         "✔ Practical labs\n"
#                         "✔ Certification guidance\n"
#                         "✔ Interview preparation\n\n"
#                         "Ask me about certifications, career scope, or fees! 😊"
#                     )
#                 }

#         # If no clear selection, re-present course buttons instead of asking for phone/name
#         return {
#             "reply": "Please choose a course below 👇",
#             "buttons": [
#                 {"id": "data_science", "label": "📘 Data Science"},
#                 {"id": "cyber_security", "label": "🔐 Cyber Security"}
#             ]
#         }

#     # ---------------------------
#     # Step 1: Greeting
#     # ---------------------------
#     if msg in ["hi", "hello", "hey"] and not session["lead_saved"]:
#         return {
#             "reply": (
#                 "Hi 👋 I’m *vormi*, your AI education assistant from *Vormirex*.\n"
#                 "I can guide you about our professional IT courses.\n\n"
#                 "👉 Please share your *Name* and *Phone Number* to continue."
#             )
#         }

#     # ---------------------------
#     # Step 2: Lead Capture (improved)
#     # ---------------------------
#     raw_phone = extract_phone(user_message)
#     name = extract_name(user_message)

#     # Set name if detected and not already present
#     if name and not session["name"]:
#         session["name"] = name
#     else:
#         # store a lightweight candidate if message contains alphabetic tokens
#         alpha = re.sub(r"[^a-zA-Z ]", "", user_message).strip()
#         if alpha and not session.get("name_candidate"):
#             # take up to first two words as a candidate
#             session["name_candidate"] = " ".join(alpha.split()[:2]).title()

#     # If we found a digit sequence, validate it strictly
#     if raw_phone:
#         if is_valid_phone(raw_phone):
#             if not session["phone"]:
#                 session["phone"] = raw_phone
#             # if we have a prior name candidate, use it
#             if not session.get("name") and session.get("name_candidate"):
#                 session["name"] = session.get("name_candidate")
#         else:
#             # Keep a candidate so we can show a helpful message instead of
#             # bouncing the user back to name prompt.
#             session["phone_candidate"] = raw_phone

#             if session.get("name"):
#                 return {"reply": f"I found {raw_phone}. Please send a valid 10-digit phone number (e.g. 9876543210)."}
#             else:
#                 return {"reply": "I found a phone number but no name yet — please share your *Name* and a valid 10-digit *Phone Number* (example: 9876543210)."}

#     # Ask missing field — prefer not to re-ask name when user sends only digits
#     if not session.get("name"):
#         return {"reply": "Thanks 😊 Please share your *Name*."}

#     if not session.get("phone"):
#         return {"reply": f"Thanks *{session['name']}* 😊 Please share your *Phone Number*."}

#     # ---------------------------
#     # Step 3: Save Lead (Once - but wait for course selection)
#     # ---------------------------
#     if not session["lead_saved"]:
#         # Mark as "lead captured" so we move to course selection flow
#         session["lead_saved"] = True
#         # Don't save to Google Sheets yet - wait until user selects a course
#         # Just return the button prompt
#         return {
#             "reply": f"Thank you *{session['name']}* 🙏 Which course are you interested in?",
#             "buttons": [
#                 {"id": "data_science", "label": "📘 Data Science"},
#                 {"id": "cyber_security", "label": "🔐 Cyber Security"},
#                 {"id": "other", "label": "❓ Other"}
#             ]
#         }

#     # ---------------------------
#     # Step 4: Course Selection (Save lead with course)
#     # ---------------------------
    
#     # Handle "Other" course selection
#     if msg in ["other", "other course"]:
#         session["waiting_for_other_course"] = True
#         return {
#             "reply": (
#                 "Thank you for your interest! 🎓\n\n"
#                 "Please tell us which course you're interested in.\n"
#                 "For example: Web Development, Mobile App, AI, Cloud Computing, etc."
#             )
#         }
    
#     if msg == "data science":
#         session["course_selected"] = "Data Science"
#         # Save ONLY when course is selected
#         if session["lead_saved"]:
#             save_lead(
#                 name=session["name"],
#                 phone=session["phone"],
#                 course="Data Science",
#                 source="Chatbot"
#             )
#         return {
#             "reply": (
#                 "📘 *Data Science Course*\n\n"
#                 "✔ Python, SQL, ML & AI\n"
#                 "✔ Real-world projects\n"
#                 "✔ Interview preparation\n"
#                 "✔ Live mentor-led sessions\n\n"
#                 "Ask me about syllabus, career roles, or fees! 😊"
#             )
#         }

#     if msg == "cyber security":
#         session["course_selected"] = "Cyber Security"
#         # Save ONLY when course is selected
#         if session["lead_saved"]:
#             save_lead(
#                 name=session["name"],
#                 phone=session["phone"],
#                 course="Cyber Security",
#                 source="Chatbot"
#             )
#         return {
#             "reply": (
#                 "🔐 *Cyber Security Course*\n\n"
#                 "✔ Networking & Ethical Hacking\n"
#                 "✔ Practical labs\n"
#                 "✔ Certification guidance\n"
#                 "✔ Interview preparation\n\n"
#                 "Ask me about certifications, career scope, or fees! 😊"
#             )
#         }

#     # ---------------------------
#     # Default
#     # ---------------------------
#     return {"reply": "I’m here to help 😊 Please choose a course or ask a question."}

# import re
# import difflib
# from backend.google_sheets import save_lead
# from backend.config import CONTACT_NUMBER

# # ---------------------------
# # In-memory session storage
# # ---------------------------
# SESSIONS = {}

# # ---------------------------
# # Utilities
# # ---------------------------
# def extract_phone(text):
#     digits = re.sub(r"\D", "", text)
#     match = re.search(r"\d{7,13}", digits)
#     return match.group() if match else None

# def is_valid_phone(phone):
#     return bool(re.fullmatch(r"[6-9]\d{9}", phone))

# def extract_name(text):
#     text = re.sub(r"\d{7,13}", "", text)
#     text = re.sub(r"[^a-zA-Z ]", "", text).strip()
#     return text.title() if text and len(text.split()) <= 3 else None

# # ---------------------------
# # Chatbot Logic
# # ---------------------------
# def chatbot_reply(user_id: str, user_message: str):
#     msg = user_message.lower().strip()

#     # Create session
#     if user_id not in SESSIONS:
#         SESSIONS[user_id] = {
#             "name": None,
#             "phone": None,
#             "lead_saved": False,
#             "course_selected": None,
#             "waiting_for_other_course": False
#         }

#     session = SESSIONS[user_id]

#     # =====================================================
#     # 🔴 TOP PRIORITY: Handle "Other course" input
#     # =====================================================
#     if session["waiting_for_other_course"]:
#         course = user_message.strip()

#         if len(course) < 3:
#             return {"reply": "Please enter a valid course name (e.g. Web Development, AI, Cloud)."}

#         session["course_selected"] = course
#         session["waiting_for_other_course"] = False

#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             course=course,
#             source="Chatbot"
#         )

#         return {
#             "reply": (
#                 f"Thank you 🙏 We've noted your interest in *{course}*.\n\n"
#                 "Our counselor will contact you shortly with complete details 😊"
#             )
#         }

#     # =====================================================
#     # Greeting
#     # =====================================================
#     if msg in ["hi", "hello", "hey"] and not session["lead_saved"]:
#         return {
#             "reply": (
#                 "Hi 👋 I’m *vormi*, your AI education assistant from *Vormirex*.\n\n"
#                 "👉 Please share your *Name* and *Phone Number* to continue."
#             )
#         }

#     # =====================================================
#     # Lead Capture
#     # =====================================================
#     phone = extract_phone(user_message)
#     name = extract_name(user_message)

#     if name and not session["name"]:
#         session["name"] = name

#     if phone and is_valid_phone(phone) and not session["phone"]:
#         session["phone"] = phone

#     if not session["name"]:
#         return {"reply": "Thanks 😊 Please share your *Name*."}

#     if not session["phone"]:
#         return {"reply": f"Thanks *{session['name']}* 😊 Please share your *Phone Number*."}

#     # =====================================================
#     # Lead captured → Ask course
#     # =====================================================
#     if not session["lead_saved"]:
#         session["lead_saved"] = True
#         return {
#             "reply": f"Thank you *{session['name']}* 🙏 Which course are you interested in?",
#             "buttons": [
#                 {"id": "data_science", "label": "📘 Data Science"},
#                 {"id": "cyber_security", "label": "🔐 Cyber Security"},
#                 {"id": "other", "label": "❓ Other"}
#             ]
#         }

#     # =====================================================
#     # Course Selection
#     # =====================================================
#     if msg in ["data science", "data_science"]:
#         save_lead(session["name"], session["phone"], "Data Science", "Chatbot")
#         return {
#             "reply": (
#                 "📘 *Data Science Course*\n\n"
#                 "✔ Python, ML, AI\n"
#                 "✔ Real-world projects\n"
#                 "✔ Interview preparation\n\n"
#                 "Ask me about syllabus or careers 😊"
#             )
#         }

#     if msg in ["cyber security", "cyber_security"]:
#         save_lead(session["name"], session["phone"], "Cyber Security", "Chatbot")
#         return {
#             "reply": (
#                 "🔐 *Cyber Security Course*\n\n"
#                 "✔ Ethical Hacking\n"
#                 "✔ Practical labs\n"
#                 "✔ Certification guidance\n\n"
#                 "Ask me about scope or fees 😊"
#             )
#         }

#     # =====================================================
#     # Other button click
#     # =====================================================
#     if msg == "other":
#         session["waiting_for_other_course"] = True
#         return {
#             "reply": (
#                 "Great choice 🎓\n\n"
#                 "Please type the *course name* you’re interested in.\n"
#                 "Example: Web Development, AI, Cloud Computing"
#             )
#         }

#     # =====================================================
#     # Fees → Human only
#     # =====================================================
#     if any(k in msg for k in ["fee", "price", "cost", "payment"]):
#         return {
#             "reply": (
#                 "💰 Fee details are explained by our counselor personally.\n\n"
#                 f"📞 Contact: *{CONTACT_NUMBER}*"
#             )
#         }

#     return {"reply": "I’m here to help 😊 Please choose a course or ask a question."}


# import re
# import difflib
# from backend.google_sheets import save_lead
# from backend.config import CONTACT_NUMBER

# # ===========================
# # In-memory session storage
# # ===========================
# SESSIONS = {}

# # ===========================
# # Utilities
# # ===========================
# def extract_phone(text):
#     digits = re.sub(r"\D", "", text)
#     match = re.search(r"\d{7,13}", digits)
#     return match.group() if match else None

# def is_valid_phone(phone):
#     return bool(re.fullmatch(r"[6-9]\d{9}", phone))

# def extract_name(text):
#     text = re.sub(r"\d{7,13}", "", text)
#     text = re.sub(r"[^a-zA-Z ]", "", text).strip()
#     return text.title() if text and len(text.split()) <= 3 else None


# # ===========================
# # Chatbot Logic
# # ===========================
# def chatbot_reply(user_id: str, user_message: str):
#     msg = user_message.lower().strip()

#     # Create session
#     if user_id not in SESSIONS:
#         SESSIONS[user_id] = {
#             "name": None,
#             "phone": None,
#             "lead_saved": False,
#             "course_selected": None,
#             "waiting_for_other_course": False
#         }

#     session = SESSIONS[user_id]

#     # =====================================================
#     # 🔴 PRIORITY: OTHER COURSE FLOW (FIXED)
#     # =====================================================
#     if session["waiting_for_other_course"]:
#         course = user_message.strip()

#         if len(course) < 3:
#             return {"reply": "Please type a valid course name (e.g. Web Development, AI, Cloud)."}

#         session["course_selected"] = course
#         session["waiting_for_other_course"] = False

#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             course=course,
#             source="Chatbot"
#         )

#         return {
#             "reply": (
#                 f"✅ Got it! You’re interested in *{course}*.\n\n"
#                 "Our counselor will contact you shortly with complete details 😊\n\n"
#                 f"📞 You can also reach us at *{CONTACT_NUMBER}*"
#             )
#         }

#     # =====================================================
#     # GREETING & BASIC INFO
#     # =====================================================
#     if msg in ["hi", "hello", "hey"]:
#         return {
#             "reply": (
#                 "Hi 👋 I’m *vormi*, your AI education assistant from *Vormirex*.\n\n"
#                 "I help students choose the right IT career path.\n\n"
#                 "👉 Please share your *Name* and *Phone Number* to continue."
#             )
#         }

#     if "who are you" in msg or "are you ai" in msg:
#         return {"reply": "I’m vormi 🤖, an AI assistant from Vormirex, here to guide you about courses and careers."}

#     if "what is vormirex" in msg or "what does vormirex do" in msg:
#         return {
#             "reply": (
#                 "*Vormirex* is an online IT education platform.\n\n"
#                 "We offer industry-focused courses like *Data Science* and *Cyber Security* "
#                 "with practical training and career guidance."
#             )
#         }

#     # =====================================================
#     # LEAD CAPTURE
#     # =====================================================
#     phone = extract_phone(user_message)
#     name = extract_name(user_message)

#     if name and not session["name"]:
#         session["name"] = name

#     if phone and is_valid_phone(phone) and not session["phone"]:
#         session["phone"] = phone

#     if not session["name"]:
#         return {"reply": "Thanks 😊 Please share your *Name*."}

#     if not session["phone"]:
#         return {"reply": f"Thanks *{session['name']}* 😊 Please share your *Phone Number*."}

#     # =====================================================
#     # ASK COURSE (ONCE)
#     # =====================================================
#     if not session["lead_saved"]:
#         session["lead_saved"] = True
#         return {
#             "reply": f"Thank you *{session['name']}* 🙏 Please choose a course 👇",
#             "buttons": [
#                 {"id": "data_science", "label": "📘 Data Science"},
#                 {"id": "cyber_security", "label": "🔐 Cyber Security"},
#                 {"id": "other", "label": "❓ Other"}
#             ]
#         }

#     # =====================================================
#     # COURSE SELECTION
#     # =====================================================
#     if msg in ["data science", "data_science"]:
#         session["course_selected"] = "Data Science"
#         save_lead(session["name"], session["phone"], "Data Science", "Chatbot")
#         return {
#             "reply": (
#                 "📘 *Data Science Course*\n\n"
#                 "✔ Python, Statistics, ML & AI\n"
#                 "✔ Real-world projects\n"
#                 "✔ Interview preparation & mock interviews\n"
#                 "✔ Beginner-friendly\n\n"
#                 "Ask me about syllabus, eligibility, or career roles 😊"
#             )
#         }

#     if msg in ["cyber security", "cyber_security"]:
#         session["course_selected"] = "Cyber Security"
#         save_lead(session["name"], session["phone"], "Cyber Security", "Chatbot")
#         return {
#             "reply": (
#                 "🔐 *Cyber Security Course*\n\n"
#                 "✔ Networking & Ethical Hacking\n"
#                 "✔ Hands-on labs\n"
#                 "✔ Certification & interview prep\n"
#                 "✔ Suitable for non-IT backgrounds\n\n"
#                 "Ask me about scope, certifications, or jobs 😊"
#             )
#         }

#     if msg == "other":
#         session["waiting_for_other_course"] = True
#         return {
#             "reply": (
#                 "Great choice 🎓\n\n"
#                 "Please type the *course name* you’re interested in.\n"
#                 "Example: Web Development, AI, Cloud Computing"
#             )
#         }

#     # =====================================================
#     # TEACHING & LEARNING
#     # =====================================================
#     if "how do you teach" in msg or "practical" in msg:
#         return {
#             "reply": (
#                 "Our training is *practical-first* 💡\n\n"
#                 "✔ Live mentor-led sessions\n"
#                 "✔ Hands-on projects\n"
#                 "✔ Doubt-clearing sessions\n"
#                 "✔ Real-world use cases"
#             )
#         }

#     # =====================================================
#     # CAREER (SAFE ANSWERS)
#     # =====================================================
#     if "job" in msg or "career" in msg:
#         return {
#             "reply": (
#                 "Our courses are designed to make you *industry-ready* 🚀\n\n"
#                 "✔ Strong fundamentals\n"
#                 "✔ Interview preparation\n"
#                 "✔ Guidance on job roles\n\n"
#                 "Final outcomes depend on your effort and consistency 💪"
#             )
#         }

#     # =====================================================
#     # FEES → HUMAN ONLY
#     # =====================================================
#     if any(k in msg for k in ["fee", "price", "cost", "emi", "payment", "discount"]):
#         return {
#             "reply": (
#                 "💰 Fees & payment details are handled by our counselor.\n\n"
#                 f"📞 Please call *{CONTACT_NUMBER}* for complete information."
#             )
#         }

#     # =====================================================
#     # TRUST / OBJECTION → HUMAN
#     # =====================================================
#     if any(k in msg for k in ["trust", "worth", "cheaper", "fake", "scam"]):
#         return {
#             "reply": (
#                 "That’s a valid concern 👍\n\n"
#                 "Our counselor can explain everything transparently and answer your doubts.\n\n"
#                 f"📞 Contact: *{CONTACT_NUMBER}*"
#             )
#         }

#     # =====================================================
#     # DEFAULT
#     # =====================================================
#     return {"reply": "I’m here to help 😊 Please ask about courses, learning style, or careers."}

# import re
# import difflib
# import requests
# from backend.google_sheets import save_lead
# from backend.config import CONTACT_NUMBER, OPENROUTER_API_KEY, OPENROUTER_MODEL

# # =====================================================
# # In-memory session storage
# # =====================================================
# SESSIONS = {}

# # =====================================================
# # OpenRouter LLM fallback (SAFE answers only)
# # =====================================================
# def llm_fallback(question: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://vormirex.ai",
#         "X-Title": "Vormirex Chatbot"
#     }

#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are vormi, an AI education assistant for Vormirex.\n"
#                     "Answer politely, clearly, and safely.\n"
#                     "Do NOT give fee details, discounts, or guarantees.\n"
#                     "Encourage speaking to a counselor when needed."
#                 )
#             },
#             {"role": "user", "content": question}
#         ],
#         "temperature": 0.3,
#         "max_tokens": 180
#     }

#     try:
#         r = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json=payload,
#             timeout=10
#         )
#         return r.json()["choices"][0]["message"]["content"]
#     except Exception:
#         return "That’s a great question 😊 Our counselor can explain this better. Please share your details or call us."

# # =====================================================
# # Utilities
# # =====================================================
# def extract_phone(text):
#     digits = re.sub(r"\D", "", text)
#     match = re.search(r"\d{7,13}", digits)
#     return match.group() if match else None

# def is_valid_phone(phone):
#     return bool(re.fullmatch(r"[6-9]\d{9}", phone))

# def extract_name(text):
#     text = re.sub(r"\d{7,13}", "", text)
#     text = re.sub(r"[^a-zA-Z ]", "", text).strip()
#     return text.title() if text and len(text.split()) <= 3 else None

# # =====================================================
# # Chatbot Main Logic
# # =====================================================
# def chatbot_reply(user_id: str, user_message: str):
#     msg = user_message.lower().strip()

#     # Create session
#     if user_id not in SESSIONS:
#         SESSIONS[user_id] = {
#             "name": None,
#             "phone": None,
#             "lead_saved": False,
#             "course_selected": None,
#             "waiting_for_other_course": False
#         }

#     session = SESSIONS[user_id]

#     # =====================================================
#     # 1️⃣ OTHER COURSE FLOW (TOP PRIORITY)
#     # =====================================================
#     if session["waiting_for_other_course"]:
#         course = user_message.strip()

#         if len(course) < 3:
#             return {"reply": "Please type a valid course name (e.g. Web Development, AI, Cloud)."}

#         session["course_selected"] = course
#         session["waiting_for_other_course"] = False

#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             course=course,
#             source="Chatbot"
#         )

#         return {
#             "reply": (
#                 f"Thank you 🙏 We've noted your interest in *{course}*.\n\n"
#                 "Our counselor will contact you shortly with complete details 😊"
#             )
#         }

#     # =====================================================
#     # 2️⃣ GREETING
#     # =====================================================
#     if msg in ["hi", "hello", "hey"] and not session["lead_saved"]:
#         return {
#             "reply": (
#                 "Hi 👋 I’m *vormi*, your AI education assistant from *Vormirex*.\n\n"
#                 "👉 Please share your *Name* and *Phone Number* to continue."
#             )
#         }

#     # =====================================================
#     # 3️⃣ LEAD CAPTURE
#     # =====================================================
#     phone = extract_phone(user_message)
#     name = extract_name(user_message)

#     if name and not session["name"]:
#         session["name"] = name

#     if phone and is_valid_phone(phone) and not session["phone"]:
#         session["phone"] = phone

#     if not session["name"]:
#         return {"reply": "Thanks 😊 Please share your *Name*."}

#     if not session["phone"]:
#         return {"reply": f"Thanks *{session['name']}* 😊 Please share your *Phone Number*."}

#     # =====================================================
#     # 4️⃣ LEAD CAPTURED → SHOW COURSE BUTTONS
#     # =====================================================
#     if not session["lead_saved"]:
#         session["lead_saved"] = True
#         return {
#             "reply": f"Thank you *{session['name']}* 🙏 Which course are you interested in?",
#             "buttons": [
#                 {"id": "data_science", "label": "📘 Data Science"},
#                 {"id": "cyber_security", "label": "🔐 Cyber Security"},
#                 {"id": "other", "label": "❓ Other"}
#             ]
#         }

#     # =====================================================
#     # 5️⃣ COURSE SELECTION
#     # =====================================================
#     if msg in ["data science", "data_science"]:
#         session["course_selected"] = "Data Science"
#         save_lead(session["name"], session["phone"], "Data Science", "Chatbot")
#         return {
#             "reply": (
#                 "📘 *Data Science Course*\n\n"
#                 "✔ Python, ML, AI\n"
#                 "✔ Real-world projects\n"
#                 "✔ Interview preparation\n"
#                 "✔ Beginner friendly\n\n"
#                 "Ask me about syllabus, jobs, or learning style 😊"
#             )
#         }

#     if msg in ["cyber security", "cyber_security"]:
#         session["course_selected"] = "Cyber Security"
#         save_lead(session["name"], session["phone"], "Cyber Security", "Chatbot")
#         return {
#             "reply": (
#                 "🔐 *Cyber Security Course*\n\n"
#                 "✔ Ethical Hacking\n"
#                 "✔ Practical labs\n"
#                 "✔ Certification guidance\n"
#                 "✔ Interview preparation\n\n"
#                 "Ask me about scope or certifications 😊"
#             )
#         }

#     if msg == "other":
#         session["waiting_for_other_course"] = True
#         return {
#             "reply": (
#                 "Great choice 🎓\n\n"
#                 "Please type the *course name* you’re interested in.\n"
#                 "Example: Web Development, AI, Cloud Computing"
#             )
#         }

#     # =====================================================
#     # 6️⃣ FEES → HUMAN ONLY
#     # =====================================================
#     if any(k in msg for k in ["fee", "price", "cost", "payment", "emi", "discount"]):
#         return {
#             "reply": (
#                 "💰 Fee details are explained personally by our counselor.\n\n"
#                 f"📞 Please contact: *{CONTACT_NUMBER}*"
#             )
#         }

#     # =====================================================
#     # 7️⃣ LLM FALLBACK (UNKNOWN QUESTIONS)
#     # =====================================================
#     return {
#         "reply": llm_fallback(user_message)
#     }


# import re
# import difflib
# import requests
# from backend.google_sheets import save_lead
# from backend.config import CONTACT_NUMBER, OPENROUTER_API_KEY, OPENROUTER_MODEL

# # =====================================================
# # In-memory session storage
# # =====================================================
# SESSIONS = {}

# # =====================================================
# # OpenRouter LLM fallback (SAFE answers only)
# # =====================================================
# def llm_fallback(question: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://vormirex.ai",
#         "X-Title": "Vormirex Chatbot"
#     }

#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are vormi, an AI education assistant for Vormirex.\n"
#                     "Answer politely, clearly, and safely.\n"
#                     "Do NOT give fee details, discounts, or guarantees.\n"
#                     "Encourage speaking to a counselor when needed."
#                 )
#             },
#             {"role": "user", "content": question}
#         ],
#         "temperature": 0.3,
#         "max_tokens": 180
#     }

#     try:
#         r = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json=payload,
#             timeout=10
#         )
#         return r.json()["choices"][0]["message"]["content"]
#     except Exception:
#         return "That’s a great question 😊 Our counselor can explain this better. Please share your details or call us."

# # =====================================================
# # Utilities
# # =====================================================
# def extract_phone(text):
#     digits = re.sub(r"\D", "", text)
#     match = re.search(r"\d{7,13}", digits)
#     return match.group() if match else None

# def is_valid_phone(phone):
#     return bool(re.fullmatch(r"[6-9]\d{9}", phone))

# def extract_name(text):
#     text = re.sub(r"\d{7,13}", "", text)
#     text = re.sub(r"[^a-zA-Z ]", "", text).strip()
#     return text.title() if text and len(text.split()) <= 3 else None

# # =====================================================
# # Chatbot Main Logic
# # =====================================================
# def chatbot_reply(user_id: str, user_message: str):
#     msg = user_message.lower().strip()

#     # Create session
#     if user_id not in SESSIONS:
#         SESSIONS[user_id] = {
#             "name": None,
#             "phone": None,
#             "lead_saved": False,
#             "course_selected": None,
#             "waiting_for_other_course": False
#         }

#     session = SESSIONS[user_id]

#     # =====================================================
#     # 1️⃣ OTHER COURSE FLOW (TOP PRIORITY)
#     # =====================================================
#     if session["waiting_for_other_course"]:
#         course = user_message.strip()

#         if len(course) < 3:
#             return {"reply": "Please type a valid course name (e.g. Web Development, AI, Cloud)."}

#         session["course_selected"] = course
#         session["waiting_for_other_course"] = False

#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             source="Chatbot",
#             course=course
#         )

#         return {
#             "reply": (
#                 f"Thank you 🙏 We've noted your interest in *{course}*.\n\n"
#                 "Our counselor will contact you shortly with complete details 😊"
#             )
#         }

#     # =====================================================
#     # 2️⃣ GREETING
#     # =====================================================
#     if msg in ["hi", "hello", "hey"] and not session["lead_saved"]:
#         return {
#             "reply": (
#                 "Hi 👋 I’m *vormi*, your AI education assistant from *Vormirex*.\n\n"
#                 "👉 Please share your *Name* and *Phone Number* to continue."
#             )
#         }

#     # =====================================================
#     # 3️⃣ LEAD CAPTURE
#     # =====================================================
#     phone = extract_phone(user_message)
#     name = extract_name(user_message)

#     if name and not session["name"]:
#         session["name"] = name

#     if phone and is_valid_phone(phone) and not session["phone"]:
#         session["phone"] = phone

#     if not session["name"]:
#         return {"reply": "Thanks 😊 Please share your *Name*."}

#     if not session["phone"]:
#         return {"reply": f"Thanks *{session['name']}* 😊 Please share your *Phone Number*."}

#     # =====================================================
#     # 4️⃣ LEAD CAPTURED → SHOW COURSE BUTTONS
#     # =====================================================
#     if not session["lead_saved"]:
#         session["lead_saved"] = True
#         return {
#             "reply": f"Thank you *{session['name']}* 🙏 Which course are you interested in?",
#             "buttons": [
#                 {"id": "data_science", "label": "📘 Data Science"},
#                 {"id": "cyber_security", "label": "🔐 Cyber Security"},
#                 {"id": "other", "label": "❓ Other"}
#             ]
#         }

#     # =====================================================
#     # 5️⃣ COURSE SELECTION (✅ FIXED)
#     # =====================================================
#     if msg in ["data science", "data_science"]:
#         session["course_selected"] = "Data Science"
#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             source="Chatbot",
#             course="Data Science"
#         )
#         return {
#             "reply": (
#                 "📘 *Data Science Course*\n\n"
#                 "✔ Python, ML, AI\n"
#                 "✔ Real-world projects\n"
#                 "✔ Interview preparation\n"
#                 "✔ Beginner friendly\n\n"
#                 "Ask me about syllabus, jobs, or learning style 😊"
#             )
#         }

#     if msg in ["cyber security", "cyber_security"]:
#         session["course_selected"] = "Cyber Security"
#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             source="Chatbot",
#             course="Cyber Security"
#         )
#         return {
#             "reply": (
#                 "🔐 *Cyber Security Course*\n\n"
#                 "✔ Ethical Hacking\n"
#                 "✔ Practical labs\n"
#                 "✔ Certification guidance\n"
#                 "✔ Interview preparation\n\n"
#                 "Ask me about scope or certifications 😊"
#             )
#         }

#     if msg == "other":
#         session["waiting_for_other_course"] = True
#         return {
#             "reply": (
#                 "Great choice 🎓\n\n"
#                 "Please type the *course name* you’re interested in.\n"
#                 "Example: Web Development, AI, Cloud Computing"
#             )
#         }

#     # =====================================================
#     # 6️⃣ FEES → HUMAN ONLY
#     # =====================================================
#     if any(k in msg for k in ["fee", "price", "cost", "payment", "emi", "discount"]):
#         return {
#             "reply": (
#                 "💰 Fee details are explained personally by our counselor.\n\n"
#                 f"📞 Please contact: *{CONTACT_NUMBER}*"
#             )
#         }

#     # =====================================================
#     # 7️⃣ LLM FALLBACK
#     # =====================================================
#     return {
#         "reply": llm_fallback(user_message)
#     }

# import re
# import requests
# from backend.google_sheets import save_lead
# from backend.config import CONTACT_NUMBER, OPENROUTER_API_KEY, OPENROUTER_MODEL

# # =====================================================
# # In-memory session storage
# # =====================================================
# SESSIONS = {}

# # =====================================================
# # Verified Vormirex Facts (NO LLM)
# # =====================================================
# VORMIREX_FACTS = {
#     "company": "Vormirex",
#     "assistant": "Vormi",
#     "ceo": "Vishal Rathode",
#     "domain": "EdTech & AI Training"
# }

# # =====================================================
# # OpenRouter LLM (STRICT + SAFE)
# # =====================================================
# def llm_fallback(question: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://vormirex.ai",
#         "X-Title": "Vormirex Chatbot"
#     }

#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are vormi, an AI assistant for Vormirex.\n"
#                     "ONLY answer questions related to:\n"
#                     "- Data Science learning\n"
#                     "- Cyber Security learning\n"
#                     "- Teaching style\n"
#                     "- Career preparation (NO guarantees)\n\n"
#                     "NEVER answer:\n"
#                     "- Company leadership\n"
#                     "- Fees or payments\n"
#                     "- General knowledge\n\n"
#                     "If question is outside scope, politely redirect to counselor."
#                 )
#             },
#             {"role": "user", "content": question}
#         ],
#         "temperature": 0.2,
#         "max_tokens": 150
#     }

#     try:
#         r = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json=payload,
#             timeout=10
#         )
#         return r.json()["choices"][0]["message"]["content"]
#     except Exception:
#         return (
#             "That’s a great question 😊\n\n"
#             "Our counselor can guide you better. "
#             "Please share your name and phone number."
#         )

# # =====================================================
# # Utilities
# # =====================================================
# def extract_phone(text):
#     digits = re.sub(r"\D", "", text)
#     match = re.search(r"\d{10}", digits)
#     return match.group() if match else None

# def is_valid_phone(phone):
#     return bool(re.fullmatch(r"[6-9]\d{9}", phone))

# def extract_name(text):
#     text = re.sub(r"\d+", "", text)
#     text = re.sub(r"[^a-zA-Z ]", "", text).strip()
#     return text.title() if 1 <= len(text.split()) <= 3 else None

# # =====================================================
# # Main Chatbot Logic
# # =====================================================
# def chatbot_reply(user_id: str, user_message: str):
#     msg = user_message.lower().strip()

#     # Create session
#     if user_id not in SESSIONS:
#         SESSIONS[user_id] = {
#             "name": None,
#             "phone": None,
#             "lead_saved": False,
#             "course_selected": None,
#             "waiting_for_other_course": False
#         }

#     session = SESSIONS[user_id]

#     # =====================================================
#     # BUSINESS FACTS (NO HALLUCINATION)
#     # =====================================================
#     if any(k in msg for k in ["ceo", "founder", "owner"]):
#         return {
#             "reply": f"The CEO of *Vormirex* is *{VORMIREX_FACTS['ceo']}*."
#         }

#     if any(k in msg for k in ["who are you", "what is vormirex", "about vormirex"]):
#         return {
#             "reply": (
#                 "I’m *Vormi*, the AI education assistant of *Vormirex*.\n\n"
#                 "Vormirex provides industry-focused training in "
#                 "Data Science and Cyber Security."
#             )
#         }

#     # =====================================================
#     # GREETING
#     # =====================================================
#     if msg in ["hi", "hello", "hey"] and not session["lead_saved"]:
#         return {
#             "reply": (
#                 "Hi 👋 I’m *Vormi* from *Vormirex*.\n\n"
#                 "Please share your *Name* and *Phone Number* to continue."
#             )
#         }

#     # =====================================================
#     # LEAD CAPTURE
#     # =====================================================
#     phone = extract_phone(user_message)
#     name = extract_name(user_message)

#     if name and not session["name"]:
#         session["name"] = name

#     if phone and is_valid_phone(phone) and not session["phone"]:
#         session["phone"] = phone

#     if not session["name"]:
#         return {"reply": "Please share your *Name* 😊"}

#     if not session["phone"]:
#         return {"reply": f"Thanks *{session['name']}* 😊 Please share your *Phone Number*."}

#     # =====================================================
#     # SHOW COURSE BUTTONS
#     # =====================================================
#     if not session["lead_saved"]:
#         session["lead_saved"] = True
#         return {
#             "reply": f"Thank you *{session['name']}* 🙏 Which course are you interested in?",
#             "buttons": [
#                 {"id": "data_science", "label": "📘 Data Science"},
#                 {"id": "cyber_security", "label": "🔐 Cyber Security"},
#                 {"id": "other", "label": "❓ Other"}
#             ]
#         }

#     # =====================================================
#     # COURSE SELECTION
#     # =====================================================
#     if msg in ["data science", "data_science"]:
#         session["course_selected"] = "Data Science"
#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             source="Chatbot",
#             course="Data Science"
#         )
#         return {
#             "reply": (
#                 "📘 *Data Science Course*\n\n"
#                 "✔ Python, ML, AI\n"
#                 "✔ Real-world projects\n"
#                 "✔ Interview preparation\n\n"
#                 "Ask me about syllabus or learning style 😊"
#             )
#         }

#     if msg in ["cyber security", "cyber_security"]:
#         session["course_selected"] = "Cyber Security"
#         save_lead(
#             name=session["name"],
#             phone=session["phone"],
#             source="Chatbot",
#             course="Cyber Security"
#         )
#         return {
#             "reply": (
#                 "🔐 *Cyber Security Course*\n\n"
#                 "✔ Ethical Hacking\n"
#                 "✔ Practical labs\n"
#                 "✔ Certification guidance\n\n"
#                 "Ask me about scope or certifications 😊"
#             )
#         }

#     if msg == "other":
#         session["waiting_for_other_course"] = True
#         return {
#             "reply": (
#                 "Please type the *course name* you’re interested in.\n"
#                 "Example: Web Development, AI, Cloud Computing"
#             )
#         }

#     # =====================================================
#     # FEES → HUMAN ONLY
#     # =====================================================
#     if any(k in msg for k in ["fee", "price", "cost", "emi", "discount", "payment"]):
#         return {
#             "reply": (
#                 "💰 Fee details are explained personally by our counselor.\n\n"
#                 f"📞 Contact: *{CONTACT_NUMBER}*"
#             )
#         }

#     # =====================================================
#     # BLOCK GENERAL KNOWLEDGE
#     # =====================================================
#     BLOCKED = [
#         "politics", "movie", "actor", "cricket", "football",
#         "president", "prime minister", "capital", "weather",
#         "news", "science", "history"
#     ]

#     if any(k in msg for k in BLOCKED):
#         return {
#             "reply": (
#                 "I can help only with *Vormirex courses and learning guidance* 😊\n\n"
#                 "Please contact our counselor for other queries."
#             )
#         }

#     # =====================================================
#     # SAFE LLM (LIMITED)
#     # =====================================================
#     return {"reply": llm_fallback(user_message)}


import re
import requests
from datetime import datetime
from backend.google_sheets import save_lead
from backend.config import CONTACT_NUMBER, OPENROUTER_API_KEY, OPENROUTER_MODEL

# =====================================================
# In-memory session storage
# =====================================================
SESSIONS = {}

# =====================================================
# Verified Vormirex Facts (NO LLM)
# =====================================================
VORMIREX_FACTS = {
    "company": "Vormirex",
    "assistant": "Vormi",
    "ceo": "Vishal Rathode",
    "domain": "EdTech & AI Training"
}

# =====================================================
# OpenRouter LLM (STRICT + SAFE)
# =====================================================
def llm_fallback(question: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://vormirex.ai",
        "X-Title": "Vormirex Chatbot"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Vormi, an AI assistant for Vormirex.\n"
                    "ONLY answer questions related to:\n"
                    "- Data Science learning\n"
                    "- Cyber Security learning\n"
                    "- Teaching style\n"
                    "- Career preparation (NO guarantees)\n\n"
                    "NEVER answer:\n"
                    "- Company leadership\n"
                    "- Fees or payments\n"
                    "- General knowledge\n\n"
                    "If question is outside scope, politely redirect to counselor."
                )
            },
            {"role": "user", "content": question}
        ],
        "temperature": 0.2,
        "max_tokens": 150
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return (
            "That’s a great question 😊\n\n"
            "Our counselor can guide you better. "
            "Please share your name and phone number."
        )

# =====================================================
# Utilities
# =====================================================
def extract_phone(text):
    digits = re.sub(r"\D", "", text)
    match = re.search(r"\d{10}", digits)
    return match.group() if match else None

def is_valid_phone(phone):
    return bool(re.fullmatch(r"[6-9]\d{9}", phone))

def extract_name(text):
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-zA-Z ]", "", text).strip()
    return text.title() if 1 <= len(text.split()) <= 3 else None

# =====================================================
# Main Chatbot Logic
# =====================================================
def chatbot_reply(user_id: str, user_message: str):
    msg = user_message.lower().strip()

    # Create session
    if user_id not in SESSIONS:
        SESSIONS[user_id] = {
            "name": None,
            "phone": None,
            "lead_saved": False,
            "course_selected": None,
            "waiting_for_other_course": False
        }

    session = SESSIONS[user_id]

    # =====================================================
    # BUSINESS FACTS (NO HALLUCINATION)
    # =====================================================
    if any(k in msg for k in ["ceo", "founder", "owner"]):
        return {"reply": f"The CEO of *Vormirex* is *{VORMIREX_FACTS['ceo']}*."}

    if any(k in msg for k in ["who are you", "what is vormirex", "about vormirex"]):
        return {
            "reply": (
                "I’m *Vormi*, the AI education assistant of *Vormirex*.\n\n"
                "Vormirex provides industry-focused training in "
                "Data Science and Cyber Security."
            )
        }

    # =====================================================
    # GREETING
    # =====================================================
    if msg in ["hi", "hello", "hey"] and not session["lead_saved"]:
        return {
            "reply": (
                "Hi 🤖 I’m Vormi from Vormirex.\n\n"
                "Please share your [Name] and [Phone Number] to continue."
            )
        }

    # =====================================================
    # LEAD CAPTURE
    # =====================================================
    phone = extract_phone(user_message)
    name = extract_name(user_message)

    if name and not session["name"]:
        session["name"] = name

    if phone and is_valid_phone(phone) and not session["phone"]:
        session["phone"] = phone

    if not session["name"]:
        return {"reply": "Please share your *Name* 😊"}

    if not session["phone"]:
        return {"reply": f"Thanks *{session['name']}* 😊 Please share your *Phone Number*."}

    # =====================================================
    # SHOW COURSE BUTTONS
    # =====================================================
    if not session["lead_saved"]:
        session["lead_saved"] = True
        return {
            "reply": f"Thank you *{session['name']}* 🙏 Which course are you interested in?",
            "buttons": [
                {"id": "data_science", "label": "📘 Data Science"},
                {"id": "cyber_security", "label": "🔐 Cyber Security"},
                {"id": "other", "label": "❓ Other"}
            ]
        }

    # =====================================================
    # COURSE SELECTION
    # =====================================================
    if msg in ["data science", "data_science"]:
        session["course_selected"] = "Data Science"
        save_lead(
            name=session["name"],
            phone=session["phone"],
            source="Chatbot",
            course="Data Science"
        )
        return {
            "reply": (
                "📘 *Data Science Course*\n\n"
                "✔ Python, ML, AI\n"
                "✔ Real-world projects\n"
                "✔ Interview preparation\n\n"
                "Would you like a detailed course PDF?"
            ),
            "buttons": [
                {"id": "download_data_science", "label": "📥 Yes, Download PDF"},
                {"id": "no_pdf", "label": "❌ No"}
            ]
        }

    if msg in ["cyber security", "cyber_security"]:
        session["course_selected"] = "Cyber Security"
        save_lead(
            name=session["name"],
            phone=session["phone"],
            source="Chatbot",
            course="Cyber Security"
        )
        return {
            "reply": (
                "🔐 *Cyber Security Course*\n\n"
                "✔ Ethical Hacking\n"
                "✔ Practical labs\n"
                "✔ Certification guidance\n\n"
                "Would you like a detailed course PDF?"
            ),
            "buttons": [
                {"id": "download_cyber_security", "label": "📥 Yes, Download PDF"},
                {"id": "no_pdf", "label": "❌ No"}
            ]
        }

    if msg == "other":
        session["waiting_for_other_course"] = True
        return {
            "reply": (
                "Please type the *course name* you’re interested in.\n"
                "Example: Web Development, AI, Cloud Computing"
            )
        }

    # =====================================================
    # DOWNLOAD HANDLERS
    # =====================================================
    if msg == "download_data_science":
        return {
            "reply": "Here is your 📘 *Data Science Course PDF*",
            "download_url": "/static/brochures/data_science.pdf"
        }

    if msg == "download_cyber_security":
        return {
            "reply": "Here is your 🔐 *Cyber Security Course PDF*",
            "download_url": "/static/brochures/cyber_security.pdf"
        }

    if msg == "no_pdf":
        return {"reply": "No problem 😊 Ask me anything about the course."}

    # =====================================================
    # FEES → HUMAN ONLY
    # =====================================================
    if any(k in msg for k in ["fee", "price", "cost", "emi", "discount", "payment"]):
        return {
            "reply": (
                "💰 Fee details are explained personally by our counselor.\n\n"
                f"📞 Contact: *{CONTACT_NUMBER}*"
            )
        }

    # =====================================================
    # BLOCK GENERAL KNOWLEDGE
    # =====================================================
    BLOCKED = [
        "politics", "movie", "actor", "cricket", "football",
        "president", "prime minister", "capital", "weather",
        "news", "science", "history"
    ]

    if any(k in msg for k in BLOCKED):
        return {
            "reply": (
                "I can help only with *Vormirex courses and learning guidance* 😊\n\n"
                "Please contact our counselor for other queries."
            )
        }

    # =====================================================
    # SAFE LLM (LIMITED)
    # =====================================================
    return {"reply": llm_fallback(user_message)}
