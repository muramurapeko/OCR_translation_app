import torch
from transformers import pipeline
from accelerate import Accelerator
# Chemin vers ton modèle local Llama
model_id = "C:\\Users\\victo\\.cache\\huggingface\\Llama-3.2-1B-Instruct"
#model_id = "C:\\Users\\victo\\.cache\\huggingface\\Llama-3.2-3B-Instruct"
# Création du pipeline pour génération de texte avec Llama-3.2


accelerator = Accelerator()
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.float16,
    device_map="auto",
)

# Fonction pour effectuer la traduction
def translate_text(input_text, target_language="chinese"):
    # Messages formatés pour le modèle
    messages = [
        {"role": "system", "content": f"You are a translator translating {target_language} to English. you will be provided {target_language} content and will output only the translation"},
        {"role": "user", "content": input_text},
    ]

    # Génération du texte avec les prompts
    outputs = pipe(
        messages,
        max_new_tokens=256,
    )
    
    # Extraction de la traduction du texte généré
    translated_text = outputs[0]["generated_text"]
    translated_text = translated_text[-1]["content"]
    print(translated_text)
    return translated_text

# Exemple de traduction
input_text = "this is a text"
translated_output = translate_text(input_text)
print(f"Traduction : {translated_output}")
