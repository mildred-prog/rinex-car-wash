from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("accounts:dashboard")

    return render(request, "accounts/login.html", {"form": form})

@login_required
def dashboard(request):
    bookings = request.user.bookings.all().order_by("-created_at")
    return render(request, "accounts/dashboard.html", {"bookings": bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(
        request.user.bookings,
        pk=pk
    )
    return render(request, "accounts/booking_detail.html", {"booking": booking})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(request.user.bookings, pk=pk)

    if request.method == "POST":
        booking.status = "cancelled"
        booking.save()
        return redirect("accounts:dashboard")

    return render(request, "accounts/cancel_booking.html", {"booking": booking})
