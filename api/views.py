from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.gemini import ask_gemini
from django.shortcuts import redirect
from django.shortcuts import render

def risk_score(request):
    profile = request.session.get('profile')

    if not profile:
        return redirect('questionnaire')

    # Sample scoring logic (customize as needed)
    score = 0

    if profile['income'] == 'above_150':
        score += 2
    elif profile['income'] == '80_150':
        score += 1

    if profile['experience'] == 'intermediate':
        score += 1
    elif profile['experience'] == 'expert':
        score += 2

    if profile['risk'] == 'medium':
        score += 1
    elif profile['risk'] == 'high':
        score += 2

    if profile['goal'] == 'long-term':
        score += 1
    elif profile['goal'] == 'retirement':
        score += 2

    # Normalize score
    risk_level = "Low"
    if score >= 6:
        risk_level = "High"
    elif score >= 3:
        risk_level = "Moderate"

    return render(request, 'risk_score.html', {
        'score': score,
        'risk_level': risk_level,
        'profile': profile
    })

def index(request):
    return render(request, 'index.html')


@api_view(['POST'])
def chat_with_gemini(request):
    user_message = request.data.get("message", "")
    context = request.data.get("context", "")

    if not user_message:
        return Response({"error": "No message provided"}, status=400)

    reply = ask_gemini(user_message, context)
    return Response({"reply": reply})


def questionnaire(request):
    return render(request, 'questionnaire.html')

@csrf_exempt
def submit_profile(request):
    if request.method == 'POST':
        profile_data = {
            'age': request.POST.get('age'),
            'income': request.POST.get('income'),
            'experience': request.POST.get('experience'),
            'risk': request.POST.get('risk'),
            'goal': request.POST.get('goal'),
        }
        request.session['profile'] = profile_data  # store for risk score / chat context
        # return redirect('/chat/')  # or redirect to /risk-score/
        return redirect('/risk-score/')  # Redirect to risk score page

    return redirect('/')



def risk_score(request):
    profile = request.session.get('profile')

    if not profile:
        return redirect('questionnaire')

    # Sample scoring logic (customize as needed)
    score = 0

    if profile['income'] == 'above_150':
        score += 2
    elif profile['income'] == '80_150':
        score += 1

    if profile['experience'] == 'intermediate':
        score += 1
    elif profile['experience'] == 'expert':
        score += 2

    if profile['risk'] == 'medium':
        score += 1
    elif profile['risk'] == 'high':
        score += 2

    if profile['goal'] == 'long-term':
        score += 1
    elif profile['goal'] == 'retirement':
        score += 2

    # Normalize score
    risk_level = "Low"
    if score >= 6:
        risk_level = "High"
    elif score >= 3:
        risk_level = "Moderate"

    return render(request, 'risk_score.html', {
        'score': score,
        'risk_level': risk_level,
        'profile': profile
    })
