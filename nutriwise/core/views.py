from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.files.base import ContentFile
import json
import base64
from google import genai
from google.genai import types
from PIL import Image
import uuid
from django.shortcuts     import redirect, render
from django.core.files.base   import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from core.LLM_request.user import User
from django.contrib import messages

gemini_key = 'AIzaSyDu_isGFBpm7EB_DoMjEI-Q25ihWgsuDtk'

client = genai.Client(api_key=gemini_key)

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(request=request))

def chatbot(request):
    return HttpResponse("Hello, chatbot. You're at the polls index.")

def profile(request):
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(request=request))

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

            user = User("20", "Male", "70Kg", "170cm", "Gain muscle and get buffed", "intolerant to gluten", "diabetis")

            answer = user.agent_answer(f"media/{image_path}", usepaddle=False)

            print(answer)

            # Delete the image after processing
            #default_storage.delete(image_path)

            #request.session['answer'] = answer

            return redirect('scan')
            # Return a JSON response with the answer
            

        return JsonResponse({'error': 'Invalid image data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def profile(request):
    user = request.user

    if request.method == 'POST':
        # grab the new height (and any other fields)
        new_height = request.POST.get('height')
        new_weight = request.POST.get('weight')
        new_age = request.POST.get('age')
        new_sex = request.POST.get('sex')
        new_objective = request.POST.get('objective')
        new_restrictions = request.POST.get('restrictions')

        if not new_height:
            new_height = 175
        if not new_weight:
            new_weight = 70
        if not new_age:
            new_age = 25
        if not new_sex:
            new_sex = "Male"
        if new_objective:
            new_objective = "Perder peso"
        if new_restrictions:
            new_restrictions = "intolerant to lactose"

        user = User(new_age, new_sex, new_weight, new_height, new_objective, new_restrictions, " ")

        #user.save()  
        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect('profile')  # PRG pattern

    # GET → just render the form pre-filled
    return render(request, 'profile.html', {
        'user': user,
    })
