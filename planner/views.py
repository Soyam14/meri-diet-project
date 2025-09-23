from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DietPlan, PreMadePlan
from django.utils import timezone
from datetime import timedelta # Import timedelta for date calculations

# home_view, chatbot_view, save_chatbot_plan_view, etc. remain the same.
# We are only updating dashboard_view and adding delete_plan_view.

@login_required
def dashboard_view(request):
    # --- Auto-Deletion Logic ---
    # Get all 7-Day plans for the current user
    seven_day_plans = DietPlan.objects.filter(
        user=request.user, 
        title__icontains='7-Day'
    )
    
    for plan in seven_day_plans:
        # Calculate when the plan should expire
        expiration_date = plan.date_created + timedelta(days=7)
        if timezone.now() > expiration_date:
            plan.delete() # Delete the plan if it has expired

    # --- Notification & Display Logic ---
    my_plans = DietPlan.objects.filter(user=request.user).order_by('-date_created')
    notifications = []
    
    for plan in my_plans:
        # Check if a plan is a 7-Day plan and is about to expire
        if '7-Day' in plan.title:
            expiration_date = plan.date_created + timedelta(days=7)
            one_day_before_expiration = expiration_date - timedelta(days=1)
            
            # If the current time is after the 1-day warning mark but before expiration
            if one_day_before_expiration < timezone.now() < expiration_date:
                time_left = expiration_date - timezone.now()
                hours_left = time_left.total_seconds() // 3600
                notifications.append(
                    f"Heads up! Your '{plan.title}' plan will be automatically deleted in approximately {int(hours_left)} hours."
                )

    context = {
        'my_plans': my_plans,
        'notifications': notifications
    }
    return render(request, 'planner/dashboard.html', context)

@login_required
def delete_plan_view(request, plan_id):
    # Ensure the request is a POST for security
    if request.method == 'POST':
        # Get the plan, ensuring it exists and belongs to the logged-in user
        plan = get_object_or_404(DietPlan, id=plan_id, user=request.user)
        plan.delete()
    return redirect('dashboard')

# --- All other views (home_view, chatbot_view, save_chatbot_plan_view, etc.) remain unchanged ---

def home_view(request):
    return render(request, 'planner/home.html')

@login_required
def chatbot_view(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        goal = request.POST.get('goal')
        preference = request.POST.get('preference')
        conditions = request.POST.getlist('conditions')

        plan_details = f"**Personalized Diet Plan for {request.user.username}**\n"
        plan_details += f"- **Goal:** {goal.replace('_', ' ').title()}\n"
        plan_details += f"- **Health Conditions:** {', '.join(conditions).title() if conditions else 'None'}\n"
        plan_details += "----------------------------------------\n\n"

        if goal == 'loss':
            plan_details += "**Breakfast:** Poha or Oatmeal with minimal sugar.\n"
            plan_details += "**Lunch:** 2 Roti, 1 bowl of Dal, Green Salad.\n"
            if preference == 'veg': plan_details += "**Dinner:** Paneer Tikka (grilled) with sauteed vegetables.\n"
            else: plan_details += "**Dinner:** Grilled Chicken Breast (100g) with green salad.\n"
        elif goal == 'gain':
            plan_details += "**Breakfast:** 2 Banana Shakes with Nuts and 4 boiled eggs (2 whole).\n"
            plan_details += "**Lunch:** 1 large bowl of Rice, 2 bowls of Dal, Curd, and Sabzi.\n"
            if preference == 'veg': plan_details += "**Dinner:** 3 Roti with Paneer Bhurji and a glass of milk.\n"
            else: plan_details += "**Dinner:** 3 Roti with Chicken Curry (2-3 pieces) and a glass of milk.\n"
        else:
            plan_details += "**Breakfast:** 2 Idli with Sambar or a bowl of Sprouts.\n"
            plan_details += "**Lunch:** A balanced meal of Roti/Rice, Dal, Sabzi, Salad, and Curd.\n"
            if preference == 'veg': plan_details += "**Dinner:** 2 Roti with Mixed Vegetable Curry.\n"
            
            else: plan_details += "**Dinner:** 2 Roti with Fish Curry (1-2 pieces).\n"
        
        plan_modifications = "\n**Important Recommendations based on your health:**\n"
        modified = False
        if 'diabetes' in conditions:
            plan_modifications += "- **Diabetes:** Avoid sugary fruits, white rice, and juices. Focus on millets and whole grains.\n"
            modified = True
        if 'bp' in conditions:
            plan_modifications += "- **High BP:** Strictly limit salt intake. Avoid pickles, papad, and processed foods.\n"
            modified = True
        if 'thyroid' in conditions:
            plan_modifications += "- **Thyroid:** Avoid soybean, cauliflower, and cabbage. Include iodine-rich foods.\n"
            modified = True
        if 'cholesterol' in conditions:
            plan_modifications += "- **High Cholesterol:** Reduce saturated fats (butter, ghee) and fried foods. Focus on oats and nuts.\n"
            modified = True
        if 'pcos' in conditions:
            plan_modifications += "- **PCOS/PCOD:** Focus on a low-glycemic diet. Avoid sugar and processed carbs. Include more whole grains.\n"
            modified = True
        if 'kidney' in conditions:
            plan_modifications += "- **Kidney Issues:** Limit protein and sodium. Avoid high-potassium foods. **Please consult a nephrologist before starting any diet.**\n"
            modified = True
        
        if modified:
            plan_details += plan_modifications

        context = {
            'plan_details': plan_details,
            'today_date': timezone.now().strftime("%d-%m-%Y")
        }
        return render(request, 'planner/chatbot_result.html', context)
    
    return render(request, 'planner/chatbot.html')

@login_required
def save_chatbot_plan_view(request):
    if request.method == 'POST':
        title = request.POST.get('plan_title')
        details = request.POST.get('plan_details')
        DietPlan.objects.create(user=request.user, title=title, plan_details=details)
    return redirect('dashboard')

@login_required
def plans_list_view(request):
    premade_plans = PreMadePlan.objects.all()
    return render(request, 'planner/plans_list.html', {'premade_plans': premade_plans})

@login_required
def add_premade_plan_view(request, plan_id):
    if request.method == 'POST':
        premade_plan = PreMadePlan.objects.get(id=plan_id)
        DietPlan.objects.create(
            user=request.user,
            title=premade_plan.title,
            plan_details=premade_plan.details
        )
    return redirect('dashboard')

def terms_and_conditions_view(request):
    return render(request, 'planner/terms_and_conditions.html')

def privacy_policy_view(request):
    return render(request, 'planner/privacy_policy.html')

def support_view(request):
    return render(request, 'planner/support.html')

def debug_view(request):
    headers = {key: value for key, value in request.headers.items()}
    return JsonResponse(headers)