from django.shortcuts import render
from .engine.verify_engine import verify, normalize_email, map_to_yes_no
from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
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
