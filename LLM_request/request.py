import toml
from google import genai
from google.genai import types
from PIL import Image
import os

#Get config.toml which holds the apikey for gemini
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config.toml")


#Load the key from file
config = toml.load(config_path)
api_key1 = config["api_key1"]

#Setup client 
client = genai.Client(api_key=api_key1)
MODEL = "gemini-2.0-flash-exp"
TEMP = 0 #Change later

chat = client.chats.create(
        model=MODEL,
        history=[
        ],
        config=types.GenerateContentConfig(response_modalities=['Text'], temperature = TEMP),
    )

def create_prompt(prompt: str, image_path: str = None, system_prompt: str = 'You are one of the best professional nutriotinists. Analyse the following recipe, and restrictions, and output a recipe IN THE SAME FORMAT as the original that matches the users restrictions.', few_shot_prompt: str = None):
    if system_prompt is None:
        final_prompt = prompt
    else: 
        final_prompt = system_prompt + "\n---\n" + prompt
    if few_shot_prompt is not None:
        final_prompt = final_prompt + "\n---\n" + few_shot_prompt
    if image_path is not None:
        img = Image.open(image_path)
        return [final_prompt, img]
    return final_prompt

def chat_google_model(prompt:str = None, image_path:str = None, system_prompt:str = None, few_shot_prompt:str = None):
    """
    This function abstracts interaction with gemini
    inputs: prompts and image model
    output: response text
    """
    
    final_prompt = create_prompt(prompt, image_path=image_path, system_prompt=system_prompt, few_shot_prompt=few_shot_prompt)
    response = chat.send_message(message=final_prompt)
    return response.text

def analyse_product(system_prompt, user_prompt, paddle_prompt, img_path):
    """
    Asks LLM to analyze product and returns response based on given prompts
    (Used in user.py)
    """
    ultimate_prompt = f'''[PT] Prompt de Sistema:{system_prompt}\n----\nVais começar por receber as informações do utilizador. Garante que a tua resposta vai de acordo aos objetivos e dados da pessoa, ESPECIALMENTE A SATISFAÇÃO DAS RESTRIÇÕES/DOENÇAS DO UTILISADOR:{user_prompt}\n----\nVais por fim receber tanto o resultado OCR da imagem, como a própria imagem (para esclarecer qualquer dúvida):{paddle_prompt}'''

    image = Image.open(img_path)

    response = client.models.generate_content(
        model="models/gemini-2.5-pro-exp-03-25", #"models/gemini-2.5-pro-exp-03-25" #"models/gemini-2.0-flash-exp"
        contents=[ultimate_prompt, image],
        config=types.GenerateContentConfig(response_modalities=['Text'], temperature = 1.4)
    )

    return response.text

if __name__ == "__main__":
    # code to run when the script is executed directly
    system_prompt = "You are one of the best professional nutriotinists. Analyse the following recipe, and restrictions, and output a complete nutritional analysis"
    prompt = input("Write a prompt for the bot: ")
    image_path = os.path.join(base_dir, "fanta.jpg")
    text = chat_google_model(prompt=prompt, system_prompt=system_prompt, image_path=image_path)
    print(text)
