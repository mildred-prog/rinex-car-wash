from django.shortcuts import render, redirect
from urllib.parse import quote
from .forms import BookingForm

WHATSAPP_NUMBER = "447956450596"


def booking(request):
    """
    MVP conversion flow:
    - Customer fills form
    - Save booking in DB
    - Redirect to WhatsApp with pre-filled booking message
    """
    initial = {}
    service_id = request.GET.get("service")
    if service_id:
        initial["service"] = service_id

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_obj = form.save()

            tier_text = booking_obj.tier.label if booking_obj.tier else "Not specified"
            date_text = booking_obj.preferred_date.strftime("%Y-%m-%d") if booking_obj.preferred_date else "Not specified"
            email_text = booking_obj.email if booking_obj.email else "Not provided"
            pov_text = booking_obj.property_or_vehicle if booking_obj.property_or_vehicle else "Not specified"
            notes_text = booking_obj.message if booking_obj.message else "None"

            message = (
                "Hello Rinex Shine, I would like to book a service.\n\n"
                f"Name: {booking_obj.full_name}\n"
                f"Phone: {booking_obj.phone}\n"
                f"Email: {email_text}\n"
                f"Service: {booking_obj.service.name}\n"
                f"Option: {tier_text}\n"
                f"Vehicle/Property: {pov_text}\n"
                f"Postcode: {booking_obj.postcode}\n"
                f"Preferred date: {date_text}\n"
                f"Notes: {notes_text}"
            )

            whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"
            return redirect(whatsapp_url)
    else:
        form = BookingForm(initial=initial)

    return render(request, "bookings/booking.html", {"form": form})
