from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
def darija_english_translation(input_text):
    # Load the pre-trained model and tokenizer
    model_name = 'echarif/mBART_for_darija_transaltion'
    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)

    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True)

    # Generate the translated output
    translated_tokens = model.generate(**inputs)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text
