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