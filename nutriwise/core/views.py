from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import base64
from google import genai
from google.genai import types
from PIL import Image

gemini_key = 'AIzaSyDu_isGFBpm7EB_DoMjEI-Q25ihWgsuDtk'

client = genai.Client(api_key=gemini_key)

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(request=request))

def chatbot(request):
    return HttpResponse("Hello, chatbot. You're at the polls index.")

def scan(request):
    template = loader.get_template('scan.html')
    return HttpResponse(template.render(request=request))

def upload_image(request):
    print("uploading")

    if request.method == 'POST':
        data = json.loads(request.body)
        image_data_url = data.get('data').get('image')

        # Remove the prefix (data:image/png;base64,) from the data URL
        if image_data_url.startswith('data:image/png;base64,'):
            image_data = image_data_url.replace('data:image/png;base64,', '')
            image_data = base64.b64decode(image_data)

            # Save the image (you can modify this to save in your preferred location)
            image_name = 'captured_image.png'
            image_path = default_storage.save(image_name, ContentFile(image_data))

            user_rep = ""

            # For your user data
            for key, item in data.get('user').items():
                user_rep = f"{user_rep} {key}: {item}\n"

            #answer = agent_answer(image_path, user_rep)
            #print(answer)

            # Delete the image after processing
            default_storage.delete(image_path)

            #request.session['answer'] = answer

            return redirect('scan')
            # Return a JSON response with the answer
            

        return JsonResponse({'error': 'Invalid image data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


