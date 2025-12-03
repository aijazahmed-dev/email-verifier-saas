from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UploadCSVForm
import pandas as pd
from .engine.verify_engine import verify, normalize_email, map_to_yes_no
from django_ratelimit.decorators import ratelimit

# Create your views here.
@login_required
@ratelimit(key='user', rate='10/m', block=True)
def emails_check(request):
    results = []
    emails_input = ""

    if request.method == "POST":
        emails_input = request.POST.get("emails", "")
        # Split by comma, space, or new line
        emails = [normalize_email(e) for e in emails_input.replace(",", "\n").splitlines() if e.strip()]
        
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

    return render(request, "verifier/emails_check.html", {
        "emails_input": emails_input,
        "results": results
    })


# Bulk email check with CSV upload/download
@login_required
@ratelimit(key='user', rate='6/m', block=True)
def bulk_csv_check_view(request):
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
            
            # Save results for download
            df_result = pd.DataFrame(data)
            request.session['bulk_results'] = df_result.to_json()  # store temporarily in session
            results = data

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
