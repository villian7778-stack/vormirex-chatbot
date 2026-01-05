def detect_intent(text: str):
    t = text.lower()

    if any(x in t for x in ["fee", "price", "cost", "charges"]):
        return "FEES"

    if any(x in t for x in ["explain", "define", "what is", "how does"]):
        return "CONTENT"

    if any(x in t for x in ["join", "enroll", "admission"]):
        return "LEAD"

    if any(x in t for x in ["course", "program", "learning"]):
        return "INFO"

    return "GENERAL"
