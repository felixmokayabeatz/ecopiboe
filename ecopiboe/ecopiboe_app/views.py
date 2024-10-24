from django.http import HttpResponse
from django.template import loader
from django.db import OperationalError
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.db.utils import OperationalError
import csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
import os
import sys
from django.db.models import Q
from django.http import JsonResponse
import google.generativeai as genai
from .models import ChatBot
from .models import Userinfo
from django.http import HttpResponseRedirect, JsonResponse
import logging
from .models import EcoFootprintQuestion
from .models import EcoFootprintCategory, UserResponse
from django.utils import timezone
import requests
from .models import AIResult
import re
import base64
from datetime import date, timedelta
from django.utils import timezone
from calendar import monthrange
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import BookRecommendationForm
from .utils.ai_utils import get_book_summary

api_key=""
logger = logging.getLogger(__name__)

API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

# print(API_KEY)
# print(api_key)

@login_required(login_url='/login/')
def piano(request):
    octaves = [0, 1, 2]
    return render(request, 'piano/piano.html', {'octaves': octaves})

@login_required(login_url='/login/')
def menu_f(request):
    return render(request, 'ecopiboe_menu/menu_f.html')

@login_required(login_url='/login/')
def get_ai_responses(request):
    user = request.user
    user_responses = UserResponse.objects.filter(user=user)
    question_responses = []
    for response in user_responses:
        question = response.question.question_text
        response_text = response.response
        question_responses.append({"question": question, "response": response_text})
    user_data_str = "\n".join([f"Q: {qr['question']}\nA: {qr['response']}" for qr in question_responses])
    prompt = (
        "Based on the following user responses, calculate the user's eco-footprint, even if their is Insufficient data use whatever you got:\n"
        f"{user_data_str}\n\n"
        "Please provide a detailed score for each response and calculation and the final eco-footprint score. There are 20 questions, this is how you will give points:\n\n"

        "Category:Electricity Usage\n"
        "For \"How many hours per day do you typically leave lights on when not in use?\" give 5 points if 12 Hours and 0 Points if 0 Hours\n"
        "For \" Do you use energy-efficient appliances (e.g., LED light bulbs, ENERGY STAR-rated appliances)?\" 1 Points for Yes and 5 points for No\n"
        "For \" Do you use renewable energy sources (e.g., solar panels, wind turbines) to power your home?\" If Yes:1 Points and No:5 Points\n"
        "For \" How often do you adjust your thermostat to conserve energy (e.g., lowering it in winter, raising it in summer)?\" Always:1 points, Often:2 Point,Sometimes:3 Points, Rarely:4 Points, Never: 5 Points, I do not own a thermostat:0 Points\n"

        "Catergory:Transportation\n"
        "For \" How do you primarily commute to work or school (e.g., car, public transit, walking, biking)?\" Give a score point that you think is appropriate between 0 and 5 points, walking being the lowest and with 1 point\n"
        "For \" How often do you carpool or rideshare with others?\" Frequently:1, Sometimes:2, Rarely:3, Never: 4 \n"
        "For\" Do you own or use a fuel-efficient vehicle?\" If Yes:3 Points, If No: 1 Point\n"
        "For \" How often do you travel long distances by plane?\"  Frequently:4, Sometimes:3, Rarely:2, Never: 0\n"

        "Catergory:Waste Management\n"
        "For \" Do you recycle paper, plastic, glass, and metal materials?\" If Yes:0 points, If No: 4 Points\n"
        "For \" Do you compost food waste and yard debris?\" Yes:1 Point, No:3 Points\n"
        "For \" How often do you use single-use plastics (e.g., plastic bags, disposable utensils, water bottles)?\"Frequently:4, Sometimes:3, Rarely:2, Never: 1 \n"
        "For \" Do you participate in local recycling programs or waste reduction initiatives?\" No:3 Points, Yes:1 Point, Sometimes:2 Points\n"

        "Catergory:Water Usage\n"
        "For \" How long do you typically shower each day?\" if 5 Hours give 3 points, 5 minutes:1 Point, any other value in between do the math but do ot show the workings\n"
        "For \"Do you use water-efficient fixtures (e.g., low-flow showerheads, dual-flush toilets)? \"No: 4 Points, Yes:1 Point\n"
        "For \" Do you collect rainwater for outdoor use (e.g., watering plants, washing cars)?\" Yes:1 point, No:3 Points\n"
        "For \" How often do you run full loads of laundry and dishes to conserve water?\" Frequently:1, Sometimes:2, Rarely:3, Never: 4 \n"

        "Catergory:Diet\n"
        "For \"How often do you consume meat and dairy products?\" Always:3 Points, Frequently:2.5, Sometimes:2, Rarely:1.5, Never: 1 \n"
        "For \" Do you incorporate plant-based meals into your diet?\" Yes:1 point,No:3 Points, Sometimes: 2 Points \n"
        "For \" How often do you eat locally grown and seasonal foods?\" Frequently:1, Sometimes:2, Rarely:3, Never: 4 \n"
        "For \" Do you minimize food waste by planning meals, using leftovers, and avoiding over-purchasing groceries?\" No:3 Points, Yes:1 Point\n\n"

        "Please use the scale Above strictly and give the scored out the total total per question, category and total.\n\n"
        "STRICTLY RETURN LIKE IN THE FORMRT BELOW EXACTLY ALWAYS\n"

        "Use this formart:\n"
        "Electricity Usage:\n"
        "- Hours of lights left on per day:\n"
        "- Use of energy-efficient appliances:\n"
        "- Use of renewable energy sources:\n"
        "-Use and regulation of a thermostat\n"

        "Transportation:\n"
        "- Primary commute method:\n"
        "- Frequency of carpooling:\n"
        "- Ownership of fuel-efficient vehicle:\n"
        "- Frequency of long-distance air travel:\""

        "Waste Management:\n"
        "- Recycling:\n"
        "- Composting:\n"
        "- Frequency of using single-use plastics:\n"
        "- Participation in recycling programs:\n"

        "Water Usage:\n"
        "- Duration of daily showers:\n"
        "- Use of water-efficient fixtures:\n"
        "- Collection of rainwater:\n"
        "- Frequency of running full loads for laundry and dishes:\n"

        "Diet:\n"
        "- Frequency of meat and dairy consumption:\n"
        "- Incorporation of plant-based meals:\n"
        "- Frequency of consuming locally grown foods:\n"
        "- Minimization of food waste:\n"
        "- Score:(x/13)\n"
        "Total Eco-Footprint Score:\n"

        "Calculations and analysis per category:\n"

        "- Electricity Usage:(x/20)\n"
        "- Transportation:(x/16)\n"
        "- Waste Management:(x/14)\n"
        "- Water Usage:(x/14)\n"
        "- Diet: (x/13)\n"

        "Under no circumstances should points exceed the maximum points in each category and overall"

        "Maximum Possible Score:77 points(worst)"
        "Minimim possible score: 11 points(Best)"

        "- Total:(x/77)(Percentage)\n"

        "And during analysis adress the person directly like \"Your eco-footprint...\" \n"
        "Give recommendations to reduce eco-footprint afterwards."

        "In case you get empty responses always return only: \"No responses received!\""
    )
    try:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        ai_response = chat.send_message(prompt)
        eco_footprint_result = ai_response.text
        eco_footprint_result = eco_footprint_result.replace("**", "").replace("*", "").replace("##", "").replace("#", "")
        ai_result_instance = AIResult.objects.create(
            user=user,
            result=eco_footprint_result
        )
        ai_result_instance.save()
        context = {"eco_footprint_result": eco_footprint_result}
        return render(request, "eco_footprint_assessment/eco_footprint_result.html", context)
    except Exception as e:
        return redirect('/get_ai_responses_error/')

@login_required(login_url='/login/')
def get_ai_responses_error(request):
    return render(request, '500.html')

@login_required(login_url='/login/')
def eco_footprint_assessment(request):
    user = request.user
    now = timezone.now()
    today = now.date()
    last_response = None
    last_submission_date = None
    try:
        last_response = UserResponse.objects.filter(user=user).latest('date')
        last_submission_date = last_response.date.date()
    except UserResponse.DoesNotExist:
        last_submission_date = None
    recent_submission = last_submission_date == today
    if recent_submission:
        return render(request, 'eco_footprint_assessment/wait_24_hrs.html', {'recent_submission': recent_submission, 'last_submission_time': last_response.date, 'first_name': user.first_name})
    if request.method == 'POST':
        for question_id, response_text in request.POST.items():
            if question_id.startswith('response_'):
                if not response_text or response_text == "Select an option":
                    return HttpResponse("Please answer all questions before submitting.")
        for question_id, response_text in request.POST.items():
            if question_id.startswith('response_'):
                question_id = int(question_id.split('_')[1])
                question = EcoFootprintQuestion.objects.get(pk=question_id)
                UserResponse.objects.create(user=user, question=question, response=response_text, date=now)
        return redirect('assessment_complete')
    else:
        categories = EcoFootprintCategory.objects.all()
        return render(request, 'eco_footprint_assessment/assessment.html', {
            'categories': categories,
            'last_submission_time': last_response.date if last_response else None
        })

@login_required(login_url='/login/')
def assessment_complete(request):
    return render(request, 'eco_footprint_assessment/assessment_complete.html')

logger = logging.getLogger(__name__)

# def test404(request):
#     return render(request, '404.html')

def ask_question(request):
    if request.method == "POST":
        if 'message_count' not in request.session:
            request.session['message_count'] = 0

        if request.session['message_count'] >= 5:
            response_d = "You have reached the maximum number of 5 messages for this session. Log In to continue to acces unlimited prompts and cool AI features"
            return JsonResponse({"data": {"text": response_d}})
            # return JsonResponse({"error": "You have reached the maximum number of 5 messages for this session. Log In to continue"}, status=400)

        text = request.POST.get("text")
        if not text:
            return JsonResponse({"error": "Text must not be empty"}, status=400)

        directive_to_gemini = (
            "In consice manner greet the user with one or two words then in (Less than 12 words) confirm to the user that AI connection to you is active they can proceed to EcoPiBoE Website.Tell them all is good they can proceed AI is working and then Answer their Question(if it there any) in less than 12 words in a new paragraph. Direct them to proceed here 'EcoPiBoE' always "
        )
        prompt = f"{directive_to_gemini}\n{text}\n\n"

        try:
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(prompt)

            request.session['message_count'] += 1

            if hasattr(response, 'image_url'):
                return JsonResponse({"data": {"image_url": response.image_url}})
            else:
                return JsonResponse({"data": {"text": response.text}})
        except Exception as e:
            logger.error(f"Error while getting AI response: {e}")
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
    else:
        return HttpResponseRedirect(reverse("ask_question"))


from datetime import datetime


logger = logging.getLogger(__name__)

def get_user_context_folder(user_id):
    base_dir = 'context'
    user_dir = os.path.join(base_dir, f"user_{user_id}")
    
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    return user_dir

def get_daily_context(user_id, date_str):
    user_context_folder = get_user_context_folder(user_id)
    daily_context_path = os.path.join(user_context_folder, f"{date_str}.txt")
    
    if os.path.exists(daily_context_path):
        with open(daily_context_path, 'r') as file:
            return file.read()
    return ""

def save_daily_context(user_id, date_str, context):
    user_context_folder = get_user_context_folder(user_id)
    daily_context_path = os.path.join(user_context_folder, f"{date_str}.txt")
    
    with open(daily_context_path, 'a') as file:
        file.write(context + "\n")

def save_master_context(request, context):
    user_id = request.user.id
    user_name = request.user.first_name.capitalize()
    user_context_folder = get_user_context_folder(user_id)
    year = datetime.now().strftime("%Y")
    month_name = datetime.now().strftime("%B").upper()
    master_context_path = os.path.join(user_context_folder, f'{month_name} {year} {user_name} Context.txt')
    
    with open(master_context_path, 'a') as file:
        file.write(context + "\n")

def chatbot(request):
    if request.method == "POST":
        text = request.POST.get("text")
        user_id = request.user.id
        last_name = request.user.last_name
        
        if not text:
            return JsonResponse({"error": "Text must not be empty"}, status=400)
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        daily_context = get_daily_context(user_id, today_str)
        
        directive = "Here answer this text as you are having a normal conversation like a human with another human. Short reply unless the user wants otherwise. This is a directive DON'T address it at all. I reapeat don't address this directive in the response AT ALL. Context from previous conversation will be included "
        prompt = f"{daily_context}\n{directive}\n\n{text}\n\n"
        
        try:
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(prompt)
            
            daily_message = "\n" + last_name + " : "+ text + "\n" + "AI : " + (response.text if hasattr(response, 'text') else "")
            save_daily_context(user_id, today_str, daily_message)
            save_master_context(request, daily_message)
            
            if hasattr(response, 'image_url'):
                return JsonResponse({"data": {"image_url": response.image_url}})
            else:
                return JsonResponse({"data": {"text": response.text}})
        except Exception as e:
            logger.error(f"Error while getting AI response: {e}")
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
    else:
        return render(request, "geminiAPI/chat_bot.html")



@login_required(login_url='/login/')
def piano_ask(request):
    if request.method == "POST":
        text = request.POST.get("text")
        user_id = request.user.id
        last_name = request.user.last_name

        if not text:
            return JsonResponse({"error": "Text must not be empty"}, status=400)

        today_str = datetime.now().strftime("%Y-%m-%d")
        daily_context = get_daily_piano_context(user_id, today_str)
        directive = "Answer this in less than 40 words unless and otherwise directed by the user to give long explanation or it is necessary in the given topic. This is a directive, do NOT address it at all."
        prompt = f"\n{directive}{daily_context} {text}\n\n"

        try:
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(prompt)
            response_text = response.text.replace('*', '').replace('**', '')

            daily_message = f"\n{last_name}: {text}\nAI: {response_text}"
            save_daily_context(user_id, today_str, daily_message)

            if hasattr(response, 'image_url'):
                return JsonResponse({"data": {"image_url": response.image_url}})
            else:
                return JsonResponse({"data": {"text": response_text}})
        except Exception as e:
            logger.error(f"Error while getting AI response: {e}")
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
    else:
        return HttpResponseRedirect(reverse('chat'))

def get_piano_context_folder(user_id):
    base_dir = 'piano_context'
    user_dir = os.path.join(base_dir, f"user_{user_id}")

    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    return user_dir

def get_daily_piano_context(user_id, date_str):
    user_context_folder = get_piano_context_folder(user_id)
    daily_context_path = os.path.join(user_context_folder, f"{date_str}.txt")

    if os.path.exists(daily_context_path):
        with open(daily_context_path, 'r') as file:
            return file.read()
    return ""

def save_daily_context(user_id, date_str, context):
    user_context_folder = get_piano_context_folder(user_id)
    daily_context_path = os.path.join(user_context_folder, f"{date_str}.txt")

    with open(daily_context_path, 'a') as file:
        file.write(context + "\n")



logger = logging.getLogger(__name__)

@csrf_exempt
def analyze_note(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note = data.get('note')

            if not note:
                return JsonResponse({"error": "No note received"}, status=400)

            directive = (
                "In less than ( 90 words).Give brief infomation on the given note, list the notes that make up the major and minor chords from the given root note. Ignore note numbers (e.g., F2, F3).Tell the users what otes to press to produce that chord, Exaplain in the most simplest way."
            )
            prompt = f"{directive}\n{note}\n\n"

            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(prompt)

            cleaned_text = response.text.replace('*', '' ).replace('**', '')
            response_data = {"text": cleaned_text}
            if hasattr(response, 'image_url'):
                response_data["image_url"] = response.image_url

            return JsonResponse({"data": response_data})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            # print(f"Error: {e}")
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required(login_url='/login/')
def chat(request):
    if request.user.is_authenticated:
        user = request.user
        chats = ChatBot.objects.filter(user=user)
    else:
        return HttpResponseRedirect('/login/')
    # context = {'chats': chats, 'CONVERSATION_HISTORY_FILE': CONVERSATION_HISTORY_FILE}
    # return render(request, "chat_bot.html", context)

def video_page(request):
    return render(request, 'sample_beats/videos.html')


def felix_about(request):
    file_path = os.path.join(settings.BASE_DIR, 'static', 'texts/about_Felix.txt')
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    file_path_1 = os.path.join(settings.BASE_DIR, 'static', 'texts/quotes.txt')
    lines_1 = []
    with open(file_path_1, 'r') as file_1:
        for line_1 in file_1:
            lines_1.append(line_1.strip())
    images = [
        'felix_photos/felix(1).jpg',
        'felix_photos/felix(2).png',
        'felix_photos/felix(3).png',
        'felix_photos/felix(4).png',
        ]
    context = {
        'lines': lines,
        'lines_1':lines_1,
        'images':images,
    }
    return render(request, 'about/felix_about.html', context)



def home(request):
    template = loader.get_template('ecopiboe_home/home.html')
    return HttpResponse(template.render())


def landing_page(request):
    file_path = os.path.join(settings.BASE_DIR, 'static/texts/land_page.txt')
    with open(file_path, 'r') as file:
        content = file.read()

    context = {
        'content': content,
    }
    return render(request, 'land_page/landing_page.html', context)



@login_required(login_url='/login/')
def login_success(request):
    template = loader.get_template('login/login_success.html')
    return HttpResponse(template.render())


from allauth.socialaccount.models import SocialAccount, SocialApp

def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
            has_social_account = SocialAccount.objects.filter(user=user, provider='google').exists()
        except User.DoesNotExist:
            user = None
            has_social_account = False

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/login_success/')
        else:
            if has_social_account:
                messages.error(request, 'The account is registered with a google account. Log in with your google account instead.')
            else:
                messages.error(request, 'Invalid Username or Email, or Password. Try Logging in with your google account')
            return redirect('/login/')


    try:
        social_app = SocialApp.objects.get(provider='google')
    except SocialApp.DoesNotExist:
        social_app = None

    return render(request, 'login/login.html', {'social_app': social_app})


def signup_success(request):
    template = loader.get_template('registration/signup_success.html')
    return HttpResponse(template.render())


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')

        if User.objects.filter(Q(email=email) | Q(username=username)).exists():
            error_message = 'Email or Username already exists.'
            return render(request, 'registration/signup.html', {'error_message': error_message})

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )

        return redirect('signup_success')

    social_app = SocialApp.objects.filter(provider='google').first()

    return render(request, 'registration/signup.html', {'social_app': social_app})



@login_required(login_url='/admin/login/')
def testing(request):
    try:
        db_is_connected = True
    except OperationalError:
        db_is_connected = False
    return render(request, 'test_db_connection/testing.html', {'db_is_connected': db_is_connected})

def forgot_password(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')
            send_password_reset_email(user.first_name, user.last_name, user.email, reset_link)
            return redirect('/reset_link_sent/')
        else:
          error_message = 'No user found with that email address. Please verify your email and try again.'
    return render(request, 'password_reset/forgot_password.html', {'error_message': error_message})


def send_password_reset_email(first_name, last_name, email, reset_link):
    subject = 'Reset Your Password'
    html_message = f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border: 3px solid #e0e0e0; border-radius: 10px;">
            <h2 style="color: #333333; font-weight: bold;">Hello {first_name} {last_name},</h2>
            <p style="font-weight: bold;">You have requested to reset your password.</p>
            <p style="font-weight: bold;">If you did not, please ignore this email.</p>
            <p style="font-weight: bold;">Report to us if you suspect your account is being compromised.</p>
            <p style="font-weight: bold;">Otherwise, click the link below to reset your password:</p>
            <p>
                <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #007bff; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Reset Your Password
                </a>
            </p>
            <p style="font-weight: bold;">If the button above does not work, copy and paste the following link into your browser:</p>
            <p><a href="{reset_link}" style="color: #007bff; font-weight: bold;">{reset_link}</a></p>
            <p style="font-weight: bold;">Reply to this email for support and technical assistance.</p>
            <p style="font-weight: bold;">Best Regards,</p>
            <p style="font-weight: bold;">EcoPiBoE Team</p>
        </div>
    </body>
    </html>
    """
    send_mail(subject, '', settings.EMAIL_HOST_USER, [email], html_message=html_message)




def reset_link_sent(request):
    return render(request, 'password_reset/reset_link_sent.html')


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
            return redirect('/password_reset_success/')
        return render(request, 'password_reset/reset_password.html')
    else:
        return redirect('/login/')

def password_reset_success(request):
    return render(request, 'password_reset/password_reset_success.html')

@login_required(login_url='/login/')
def visualize_ai_results(request):
    user = request.user
    current_date = timezone.localdate()
    user_results = AIResult.objects.filter(user=user)

    if not user_results:
        return JsonResponse({"error": "No AI results found for the current user."}, safe=False)
    category_scores = {
        "Electricity Usage": [],
        "Transportation": [],
        "Waste Management": [],
        "Water Usage": [],
        "Diet": [],
    }
    total_scores = []
    date_scores = {}
    for result in user_results:
        text = result.result
        pattern = r"\b\d+\b"
        matches = re.findall(pattern, text)
        selected_numbers_by_index = [matches[i] if i < len(matches) else 0 for i in [5, 11, 17, 24, 30]]

        scores = [int(match) for match in selected_numbers_by_index]
        category_keys = list(category_scores.keys())
        min_length = min(len(category_keys), len(scores))
        for i in range(min_length):
            category = category_keys[i]
            category_scores[category].append(scores[i])
        total_score = sum(scores)
        total_scores.append(total_score)
        created_date = result.date.day
        date_scores[created_date] = date_scores.get(created_date, 0) + total_score
    if len(total_scores) == 0:
        return JsonResponse({"error": "Error occurred. Cannot divide by zero."}, safe=False)
    average_scores = {category: sum(scores) / len(scores) for category, scores in category_scores.items()}
    total_score = sum(total_scores)
    current_month = current_date.month
    current_year = current_date.year
    days_in_month = monthrange(current_year, current_month)[1]
    month_scores = [score for date, score in date_scores.items() if current_date.month == current_month]
    average_month_score = sum(month_scores) / len(month_scores) if month_scores else 0
    year_scores = [score for date, score in date_scores.items() if current_date.year == current_year]
    average_year_score = sum(year_scores) / len(year_scores) if year_scores else 0
    categories = list(average_scores.keys())
    scores = list(average_scores.values())
    current_month_name = current_date.strftime('%B')
    today = current_date.day
    for day in range(1, today + 1):
        date_scores.setdefault(day, 0)
    context = {
        'categories': categories,
        'scores': scores,
        'total_score': total_score,
        'date_scores': date_scores,
        'average_month_score': average_month_score,
        'average_year_score': average_year_score,
        'current_day': today,
        'days_in_month': days_in_month,
        'current_month': current_month_name,
        'current_year': current_year,
        'current_day_name': current_date.strftime('%A'),
    }
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(date_scores)
    return render(request, 'eco_footprint_assessment/visualize_ai_results.html', context)



nltk_logger = logging.getLogger('nltk')
nltk_logger.setLevel(logging.ERROR)

@login_required(login_url='/login/')
def recommend_books(request):
    try:
        if request.method == 'POST':
            form = BookRecommendationForm(request.POST)
            if form.is_valid():
                search_params = {}
                title = form.cleaned_data.get('title')
                if title:
                    search_params['title'] = title
                author = form.cleaned_data.get('author')
                if author:
                    search_params['author'] = author
                publish_date = form.cleaned_data.get('publishDate')
                if publish_date:
                    search_params['publish_date'] = publish_date
                description = form.cleaned_data.get('description')
                if description:
                    search_params['first_sentence'] = description
                search_params['limit'] = 10

                if search_params:
                    search_response = requests.get('https://openlibrary.org/search.json', params=search_params)
                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        num_found = search_data.get('num_found', 0)
                        if num_found > 0:
                            books_data = search_data.get('docs', [])[:10]
                            recommended_books_list = []
                            for book in books_data:
                                book_info = {
                                    'title': book.get('title', ''),
                                    'author': book.get('author_name', ''),
                                    'publishDate': ', '.join(book.get('publish_date', [])),
                                    'description': book.get('first_sentence', ''),
                                    'link': f"https://openlibrary.org{book.get('key', '')}",
                                }
                                recommended_books_list.append(book_info)
                            return JsonResponse({
                                'success': True,
                                'message': 'Books found based on the given criteria',
                                'totalBooksFound': num_found,
                                'data': recommended_books_list,
                            })
                        else:
                            return JsonResponse({'success': True, 'message': 'No books found based on the given criteria'})
                    else:
                        return JsonResponse({'success': False, 'message': f'Unable to fetch data from Open Library API.'})
                else:
                    return JsonResponse({'success': True, 'message': 'No search parameters provided.'})
            else:
                return JsonResponse({'success': False, 'message': 'Form is not valid.'})
        else:
            form = BookRecommendationForm()
            return render(request, 'book_recommender/book_recommender.html', {'form': form})
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return JsonResponse({'success': False})

@login_required(login_url='/login/')
@csrf_exempt
def summarize_book(request):
    if request.method == 'POST':
        try:
            book_data = json.loads(request.body)
            summary = get_book_summary(book_data)
            return JsonResponse({'success': True, 'summary': summary})

        except Exception as e:

            return JsonResponse({'success': False, 'message': 'An error occurred while summarizing the book, or you are trying to access restricted or explicit content'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

logger = logging.getLogger(__name__)
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

@login_required(login_url='/login/')
def send_email(request):
    if request.method == 'POST':
        try:
            to = request.POST['to']
            subject = request.POST['subject']
            message_text = request.POST['message']

            token_dir = os.path.join(settings.BASE_DIR, 'user_tokens')
            if not os.path.exists(token_dir):
                os.makedirs(token_dir)

            user_id = request.user.id
            token_path = os.path.join(token_dir, f'{user_id}_token.json')

            creds = None
            if os.path.exists(token_path):
                try:
                    with open(token_path, 'r') as token_file:
                        creds_data = json.load(token_file)
                        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
                        if not creds.refresh_token:
                            os.remove(token_path)
                            return JsonResponse({'success': False, 'auth_url': reverse('google_reauthorize')})
                except ValueError:
                    os.remove(token_path)
                    return JsonResponse({'success': False, 'auth_url': reverse('google_reauthorize')})
                except Exception as e:
                    return JsonResponse({'success': False, 'auth_url': reverse('google_reauthorize'), 'message': f'Unexpected error: {str(e)}. Please try again.'})

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except RefreshError:
                        os.remove(token_path)
                        return JsonResponse({'success': False, 'auth_url': reverse('google_reauthorize')})
                    except Exception as error:
                        return JsonResponse({'success': False, 'auth_url': reverse('google_reauthorize'), 'message': f'Unexpected error: {str(error)}. Please try again.'})
                else:
                    return JsonResponse({'success': False, 'auth_url': reverse('google_reauthorize')})

            try:
                service = build('gmail', 'v1', credentials=creds)
                message = MIMEText(message_text)
                message['to'] = to
                message['subject'] = subject

                raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
                message = {'raw': raw}
                service.users().messages().send(userId="me", body=message).execute()

                return JsonResponse({'success': True, 'message': 'Email sent successfully!'})

            except Exception as error:
                return JsonResponse({'success': False, 'auth_url': reverse('google_reauthorize')})

        except Exception as error:
            return JsonResponse({'success': False, 'message': 'An unexpected error occurred. Please try again later.'})

    return render(request, 'email/send_email.html', {'user_name': request.user.get_full_name() or request.user.username, 'user_email': request.user.email})


from google_auth_oauthlib.flow import Flow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

@login_required(login_url='/login/')
def google_reauthorize(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS,
        scopes=SCOPES,
        redirect_uri='https://www.ecopiboe.com/oauth2callback/'
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    request.session['state'] = state
    return redirect(authorization_url)

def oauth2callback(request):
    state = request.session.get('state')
    if not state:
        return JsonResponse({'success': False, 'message': 'State not found in session.'})

    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS,
        scopes=SCOPES,
        state=state,
        redirect_uri='https://www.ecopiboe.com/oauth2callback/'
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials
    user_id = request.user.id
    token_dir = os.path.join(settings.BASE_DIR, 'user_tokens')
    if not os.path.exists(token_dir):
        os.makedirs(token_dir)

    token_path = os.path.join(token_dir, f'{user_id}_token.json')
    with open(token_path, 'w') as token_file:
        token_file.write(creds.to_json())

    return redirect('send_email')


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def improve_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subject = data.get("subject")
            message = data.get("message")

            if not subject or not message:
                return JsonResponse({"error": "Subject and message must not be empty"}, status=400)

            directive = "Improve the following email content for clarity and professionalism. Don't include the regards and [Your name] part at the end, it is populated post."
            prompt = f"{directive}\nSubject: {subject}\n\n{message}\n\n"

            try:
                model = genai.GenerativeModel("gemini-pro")
                chat = model.start_chat()
                response = chat.send_message(prompt)
                improved_message = response.text

                return JsonResponse({"success": True, "improved_message": improved_message})
            except Exception as e:
                logger.error(f"Error while getting AI response: {e}")
                return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
