from django.shortcuts import render, redirect
from django.contrib import messages
from urllib.parse import quote
from .forms import BookingForm

WHATSAPP_NUMBER = "447956450596"


def booking(request):
    initial = {}
    service_id = request.GET.get("service")
    if service_id:
        initial["service"] = service_id

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_obj = form.save(commit=False)

            if request.user.is_authenticated:
                booking_obj.user = request.user

            booking_obj.save()

            tier_text = booking_obj.tier.label if booking_obj.tier else "Not specified"
            date_text = booking_obj.preferred_date.strftime("%Y-%m-%d") if booking_obj.preferred_date else "Not specified"
            email_text = booking_obj.email if booking_obj.email else "Not provided"
            pov_text = booking_obj.property_or_vehicle if booking_obj.property_or_vehicle else "Not specified"
            notes_text = booking_obj.message if booking_obj.message else "None"

            message_text = (
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

            whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message_text)}"

            # Flash success message for user reassurance
            messages.success(request, "Booking received. We’ll contact you shortly to confirm availability.")

            # Render a success page with a WhatsApp button (no forced redirect)
            return render(request, "bookings/booking_success.html", {
                "booking": booking_obj,
                "whatsapp_url": whatsapp_url
            })
    else:
        form = BookingForm(initial=initial)

    return render(request, "bookings/booking.html", {"form": form})
