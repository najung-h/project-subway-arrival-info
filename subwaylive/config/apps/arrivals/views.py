from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StationSearchForm
from .services import fetch_realtime_arrivals_by_station

def index(request):
    form = StationSearchForm(request.GET or None)
    # 로그인 사용자 기본역 자동 채움
    if request.user.is_authenticated and not form.is_bound:
        default_station = getattr(getattr(request.user, "profile", None), "default_station", "")
        if default_station:
            form = StationSearchForm(initial={"station": default_station})
    return render(request, "arrivals/index.html", {"form": form})

def arrival_info(request):
    if request.method == "GET":
        form = StationSearchForm(request.GET)
        if form.is_valid():
            station = form.cleaned_data["station"]
            result = fetch_realtime_arrivals_by_station(station)
            return render(request, "arrivals/arrival_info.html", {"result": result, "station": station})
    return redirect("arrivals:index")
