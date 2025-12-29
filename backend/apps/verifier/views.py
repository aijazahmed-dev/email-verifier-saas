from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UploadCSVForm
import pandas as pd
from django.utils import timezone
from django.core.paginator import Paginator
from django_ratelimit.decorators import ratelimit
from .engine.verify_engine import verify, normalize_email, map_to_yes_no
from .models import EmailVerificationLog, Plan, UserPlan
from .utils_plans import reset_user_credits
from django.conf import settings
from django.http import FileResponse, Http404
import os
import uuid

# Create your views here.
@login_required
@ratelimit(key='user', rate='10/m', block=True)
def emails_check(request):
    user_plan, _ = UserPlan.objects.get_or_create(
    user=request.user,
    defaults={
        "plan": Plan.objects.get(name="Free"),
        "credits_remaining": 50,
    }
)
    
    today = timezone.now().date()

    # Reset daily + monthly credits
    reset_user_credits(user_plan)

    # Expiry check for Basic/Pro
    if user_plan.expiry_date and today > user_plan.expiry_date:
        return HttpResponse("Your plan has expired. Please buy a new package.", status=402)

    
    # Check credits
    if user_plan.credits_remaining <= 0:
        return HttpResponse("You have no credits left. Please buy more credits.", status=402)
    
    results = []
    emails_input = ""

    # Retrieve previous results from session (if any)
    results = request.session.pop('results', [])
    emails_input = request.session.pop('emails_input', "")

    page_obj = None

    if results:
        page_number = request.GET.get('page', 1)
        paginator = Paginator(results, 10)
        page_obj = paginator.get_page(page_number)
        
    if request.method == "POST":
        emails_input = request.POST.get("emails", "")
        
        # Split by comma, space, or new line
        emails = [normalize_email(e) for e in emails_input.replace(",", "\n").splitlines() if e.strip()]
        
        # Check daily limit for any plan with a limit
        if user_plan.plan.daily_limit > 0 and user_plan.daily_used + len(emails) > user_plan.plan.daily_limit:
            return HttpResponse("Daily limit reached.", status=429)
        
        # Check Montly limit
        if user_plan.plan.monthly_limit > 0 and user_plan.monthly_used + len(emails) > user_plan.plan.monthly_limit:
            return HttpResponse("Monthly limit reached.", status=429)
        
        # Check if user has enough credits
        if len(emails) > user_plan.credits_remaining:
            return HttpResponse("Not enough credits.", status=402)
        
        for email in emails:
            result = verify(email)
            results.append({
        "email": email,
        "syntax_valid": map_to_yes_no(result["syntax_valid"]),
        "has_mx": map_to_yes_no(result["has_mx"]),
        "is_disposable": map_to_yes_no(result["is_disposable"]),
        "is_role": map_to_yes_no(result["is_role"]),
        "deliverable": map_to_yes_no(result["deliverable"]),

        })

            
            # Save to logs
            EmailVerificationLog.objects.create(
                user=request.user,
                email=email,
                syntax_valid=result["syntax_valid"],
                has_mx=result["has_mx"],
                is_disposable=result["is_disposable"],
                is_role=result["is_role"],
                deliverable=result["deliverable"]
            )

        request.session['results'] = results
        request.session['emails_input'] = emails_input

        # Deduct credits after verifiying emails
        user_plan.credits_remaining -= len(emails)

        # Count daily usage 
        if user_plan.plan.daily_limit > 0:
            user_plan.daily_used += len(emails)

        # Count monthly usage
        if user_plan.plan.monthly_limit > 0:
            user_plan.monthly_used += len(emails)

        user_plan.save()

        return redirect('emails_check')

    return render(request, "verifier/emails_check.html", {
        "emails_input": emails_input,
        "page_obj": page_obj,
        "results": results
    })


# Bulk email check with CSV upload/download
@login_required
@ratelimit(key='user', rate='6/m', block=True)
def bulk_csv_check_view(request):
    user_plan, _ = UserPlan.objects.get_or_create(
    user=request.user,
    defaults={
        "plan": Plan.objects.get(name="Free"),
        "credits_remaining": 50,
    }
)
    
    bulk_result_file = request.session.get('bulk_result_file', None)

    today = timezone.now().date()
    
    # Reset daily + monthly credits
    reset_user_credits(user_plan)

    form = UploadCSVForm()
    
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            
            # Read CSV
            try:
                df = pd.read_csv(csv_file)
            except Exception:
                return HttpResponse("Invalid CSV file", status=400)
            
            # Assume email column named 'email' or first column
            if 'email' in df.columns:
                emails = df['email'].dropna().tolist()
            else:
                emails = df.iloc[:,0].dropna().tolist()

            # Check plan expiry
            if user_plan.expiry_date and today > user_plan.expiry_date:
                return HttpResponse("Your plan has expired. Please buy a new package.", status=402)
        
            # Check daily limit
            if user_plan.plan.daily_limit > 0 and user_plan.daily_used + len(emails) > user_plan.plan.daily_limit:
                return HttpResponse("Daily limit reached.", status=429)
            
            # Check Montly limit
            if user_plan.plan.monthly_limit > 0 and user_plan.monthly_used + len(emails) > user_plan.plan.monthly_limit:
                return HttpResponse("Monthly limit reached.", status=429)
            
            # Check if user has enough credits
            if len(emails) > user_plan.credits_remaining:
                return HttpResponse("Not enough credits.", status=402)
            
            # Process emails
            data = []
            for email in emails:
                email_norm = normalize_email(str(email))
                result = verify(email_norm)
                data.append({
                    "email": email_norm,
                    "syntax_valid": map_to_yes_no(result["syntax_valid"]),
                    "has_mx": map_to_yes_no(result["has_mx"]),
                    "is_disposable": map_to_yes_no(result["is_disposable"]),
                    "is_role": map_to_yes_no(result["is_role"]),
                    "deliverable": map_to_yes_no(result["deliverable"]),
                })

                # Save to logs
                EmailVerificationLog.objects.create(
                user=request.user,
                email=email_norm,
                syntax_valid=result["syntax_valid"],
                has_mx=result["has_mx"],
                is_disposable=result["is_disposable"],
                is_role=result["is_role"],
                deliverable=result["deliverable"]
                )
            
            # Save results
            df_result = pd.DataFrame(data)

            filename = f"bulk_results_{request.user.id}_{uuid.uuid4().hex}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, "bulk_results", filename)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df_result.to_csv(file_path, index=False)

            # store file path for download
            request.session['bulk_result_file'] = filename

            # Deduct credits after verifiying emails
            user_plan.credits_remaining -= len(emails)

            # Count daily usage (only free plan)
            if user_plan.plan.daily_limit > 0:
                user_plan.daily_used += len(emails)

            # Count monthly usage
            if user_plan.plan.monthly_limit > 0:
                user_plan.monthly_used += len(emails)

            user_plan.save()

            return redirect('bulk_csv_check')

    return render(request, "verifier/bulk_csv_check.html", {
        "form": form,
        "bulk_result_file": bulk_result_file,
    })


# Download processed CSV
@login_required
def download_bulk_results(request):
    filename = request.session.get('bulk_result_file')
    if not filename:
        return HttpResponse("No file to download.", status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, "bulk_results", filename)

    if not os.path.exists(file_path):
        raise Http404("File not found.")

    response = FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=filename
    )

    request.session.pop('bulk_result_file', None)

    return response

# View to list the logs for the logged-in user
@login_required
def verification_history(request):
    logs_list = EmailVerificationLog.objects.filter(user=request.user).order_by('-timestamp')
    
    paginator = Paginator(logs_list, 20)  # Show 20 logs per page
    page_number = request.GET.get('page')  # Get page number from URL
    page_obj = paginator.get_page(page_number)  # Get logs for the requested page

    return render(request, "verifier/history.html", {"page_obj": page_obj})
