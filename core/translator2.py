import ollama

def translate_text(input_text, target_language="chinese", model_name="deepseek-r1:1.5b"):
    # Construct prompt for translation
    prompt = f"""You are a translator. Translate the following text from {target_language} to English:

{input_text}

Only output the translated English text, without any extra explanation."""

    # Call Ollama chat API
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a live translator you should only give the translation."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract translation
    translated_text = response['message']['content'].strip()
    return translated_text

# Example usage
input_text = "我喜欢学习人工智能。"
translated = translate_text(input_text, target_language="Chinese")
print("Traduction :", translated)
