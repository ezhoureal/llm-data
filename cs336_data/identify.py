import fasttext
_model = None

def get_model():
    global _model
    if _model is None:
        _model = fasttext.load_model("lid.176.bin")
    return _model

def identify_language(text: str) -> tuple[str, float]:
    text = text.replace('\n', ' ')
    model = get_model()
    predictions = model.predict(text)
    label = predictions[0][0].replace("__label__", "")
    predictions = ((label,), predictions[1])
    return predictions[0][0], predictions[1][0]

def identify_email(text: str) -> tuple[str, int]:
    import re
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    new_text = re.sub(email_pattern, "|||EMAIL_ADDRESS|||", text)
    return new_text, len(emails)

def identify_phone_number(text: str) -> tuple[str, int]:
    import re
    phone_pattern = r'(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}'
    phones = re.findall(phone_pattern, text)
    text = re.sub(phone_pattern, "|||PHONE_NUMBER|||", text)
    return text, len(phones)

def identify_ip(text: str) -> tuple[str, int]:
    import re
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = re.findall(ip_pattern, text)
    text = re.sub(ip_pattern, "|||IP_ADDRESS|||", text)
    return text, len(ips)