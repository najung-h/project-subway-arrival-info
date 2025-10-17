from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

@login_required
def profile_view(request):
    prof, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            prof.default_station = form.cleaned_data["default_station"]
            prof.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(initial={"default_station": prof.default_station})
    return render(request, "arrivals/base.html", {
        "form": form,
        "content_for_profile": True,  # 간단히 base 템플릿 재사용
    })
