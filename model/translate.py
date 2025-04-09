from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("darija_to_french_model")
model = AutoModelForSeq2SeqLM.from_pretrained("darija_to_french_model")

def translate_darija_to_french(darija_input: str) -> str:

    """
    Translate the input from Moroccan Darija to French using Custom Helsiniki model.
    """

    # Tokenize the input
    inputs = tokenizer(darija_input, return_tensors="pt", max_length=256, truncation=True)

    # Generate translation
    outputs = model.generate(**inputs, max_length=256, num_beams=4, early_stopping=True)

    # Decode and return the output
    french_translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return french_translation
