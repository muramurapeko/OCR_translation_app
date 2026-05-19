import ollama
import re

def translate_text(input_text, target_language="chinese", model_name="deepseek-r1:1.5b"):
    # Prompt the model to translate
    prompt = f"""You are a translator. Translate the following text from {target_language} to English:

{input_text}

Only output the translated English text, without any extra explanation or formatting."""

    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    full_output = response['message']['content'].strip()

    # Remove everything between <think> and </think>, including the tags
    cleaned_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL).strip()

    return cleaned_output

# Example usage
input_text = "你愿意继续学习人工智能吗？"
translated = translate_text(input_text, target_language="Chinese")
print("Traduction :", translated)
