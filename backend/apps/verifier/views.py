from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UploadCSVForm
import pandas as pd
from django.core.paginator import Paginator
from django_ratelimit.decorators import ratelimit
from .engine.verify_engine import verify, normalize_email, map_to_yes_no
from .models import EmailVerificationLog, UserPlan
from .utils_plans import reset_user_credits

# Create your views here.
@login_required
@ratelimit(key='user', rate='10/m', block=True)
def emails_check(request):
    user_plan = UserPlan.objects.get(user=request.user)
    
    # Reset daily + monthly credits
    reset_user_credits(user_plan)

    # If free plan, check daily limit
    if user_plan.plan.is_monthly:
        if user_plan.daily_used >= user_plan.plan.daily_limit:
            return HttpResponse("Daily limit reached. Try tomorrow.", status=429)
    
    # Check credits
    if user_plan.credits_remaining <= 0:
        return HttpResponse("You have no credits left. Please buy more credits.", status=402)
    
    results = []
    emails_input = ""

    if request.method == "POST":
        emails_input = request.POST.get("emails", "")
        # Split by comma, space, or new line
        emails = [normalize_email(e) for e in emails_input.replace(",", "\n").splitlines() if e.strip()]
        
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

        # Deduct credits after verifiying emails
        user_plan.credits_remaining -= len(emails)

        # Count daily usage (only free plan)
        if user_plan.plan.is_monthly:
            user_plan.daily_used += len(emails)

        user_plan.save()

    return render(request, "verifier/emails_check.html", {
        "emails_input": emails_input,
        "results": results
    })


# Bulk email check with CSV upload/download
@login_required
@ratelimit(key='user', rate='6/m', block=True)
def bulk_csv_check_view(request):
    user_plan = UserPlan.objects.get(user=request.user)
    
    # Reset daily + monthly credits
    reset_user_credits(user_plan)

    # If free plan, check daily limit
    if user_plan.plan.is_monthly:
        if user_plan.daily_used >= user_plan.plan.daily_limit:
            return HttpResponse("Daily limit reached. Try tomorrow.", status=429)
    
    # Check credits
    if user_plan.credits_remaining <= 0:
        return HttpResponse("You have no credits left. Please buy more credits.", status=402)
    

    results = []
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
                email=email,
                syntax_valid=result["syntax_valid"],
                has_mx=result["has_mx"],
                is_disposable=result["is_disposable"],
                is_role=result["is_role"],
                deliverable=result["deliverable"]
            )
            
        # Save results for download
        df_result = pd.DataFrame(data)
        request.session['bulk_results'] = df_result.to_json()  # store temporarily in session
        results = data

        # Deduct credits after verifiying emails
        user_plan.credits_remaining -= len(emails)

        # Count daily usage (only free plan)
        if user_plan.plan.is_monthly:
            user_plan.daily_used += len(emails)

        user_plan.save()

    return render(request, "verifier/bulk_csv_check.html", {
        "form": form,
        "results": results
    })


# Download processed CSV
def download_bulk_results(request):
    json_data = request.session.get('bulk_results')
    if not json_data:
        return HttpResponse("No results to download.", status=400)
    
    df = pd.read_json(json_data)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="email_verification_results.csv"'
    df.to_csv(path_or_buf=response, index=False)
    return response

# View to list the logs for the logged-in user
@login_required
def verification_history(request):
    logs_list = EmailVerificationLog.objects.filter(user=request.user).order_by('-timestamp')
    
    paginator = Paginator(logs_list, 20)  # Show 20 logs per page
    page_number = request.GET.get('page')  # Get page number from URL
    page_obj = paginator.get_page(page_number)  # Get logs for the requested page

    return render(request, "verifier/history.html", {"page_obj": page_obj})
