from django import forms
from .models import Booking
from services.models import Service, ServiceTier


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "full_name",
            "phone",
            "email",
            "service",
            "tier",
            "property_or_vehicle",
            "postcode",
            "preferred_date",
            "message",
        ]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limit services to active only
        self.fields["service"].queryset = Service.objects.filter(is_active=True)

        # Tier is optional (because not every service will have tiers)
        self.fields["tier"].required = False
        self.fields["tier"].help_text = "Optional – select size/type if applicable"

        # By default show no tiers until a service is chosen
        self.fields["tier"].queryset = ServiceTier.objects.none()

        # If service is set (POST), filter tiers to that service
        if "service" in self.data:
            try:
                service_id = int(self.data.get("service"))
                self.fields["tier"].queryset = ServiceTier.objects.filter(service_id=service_id)
            except (TypeError, ValueError):
                pass
        # If service is set (initial), filter tiers too
        elif self.initial.get("service"):
            service_id = self.initial.get("service")
            self.fields["tier"].queryset = ServiceTier.objects.filter(service_id=service_id)

        # Basic bootstrap styling + small UX improvements
        for field_name, field in self.fields.items():
            css_class = "form-control"
            if field.widget.__class__.__name__ in ["Select", "SelectMultiple"]:
                css_class = "form-select"

            field.widget.attrs.update({"class": css_class})

            # Phone UX (mobile numeric keypad)
            if field_name == "phone":
                field.widget.attrs.update({
                    "placeholder": "e.g. 07956 450596",
                    "type": "tel",
                })

            # Postcode hint
            if field_name == "postcode":
                field.widget.attrs.update({
                    "placeholder": "e.g. SE1 2AB",
                })

            # Optional: make preferred date clearer
            if field_name == "preferred_date":
                field.widget.attrs.update({
                    "placeholder": "Select a date",
                })
