from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
import regex as re

NAME_REGEX = re.compile(r"^[\p{L}'][\p{L} '-]*[\p{L}']$", re.UNICODE)

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(
        label=_("first name"),
        required=True,
        min_length=1,
        max_length=150,
        help_text=_("Letters, apostrophes, hyphens and spaces only")
    )
    last_name = serializers.CharField(
        label=_("last name"),
        required=True,
        min_length=1,
        max_length=150,
        help_text=_("Letters, apostrophes, hyphens and spaces only")
    )

    def validate(self, data):
        data = super().validate(data)
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        error_msg = _("Allowed: letters, apostrophes ('), hyphens (-), spaces")
        
        if not NAME_REGEX.fullmatch(first_name):
            raise serializers.ValidationError({
                "first_name": [error_msg]
            })

        if not NAME_REGEX.fullmatch(last_name):
            raise serializers.ValidationError({
                "last_name": [error_msg]
            })

        return data

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            "first_name": self.validated_data.get("first_name"),
            "last_name": self.validated_data.get("last_name")
        })
        return data
