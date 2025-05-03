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
import markdown

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

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    payload = json.loads(request.body)
    image_data_url = payload.get('data', {}).get('image')
    if not image_data_url or not image_data_url.startswith('data:image/png;base64,'):
        return JsonResponse({'error': 'Invalid image data'}, status=400)

    b64 = image_data_url.split(',',1)[1]
    img_bytes = base64.b64decode(b64)
    image_path = default_storage.save('captured_image.png', ContentFile(img_bytes))

    user = User("20", "Male", "70Kg", "170cm", "Gain muscle and get buffed", "intolerant to gluten", "Diabetes")
    answer = user.agent_answer(f"media/{image_path}", usepaddle=False)

    formatted_answer = markdown.markdown(answer.strip())
    answer = formatted_answer

    print(answer)

    #request.session['scan_answer'] = answer
    return JsonResponse({'answer': answer})

    return redirect('scan')

def scan(request):
    # Pull the answer out (and remove it so it only shows once)
    answer = request.session.pop('scan_answer', None)
    return render(request, 'scan.html', {
        'answer': answer
    })


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
