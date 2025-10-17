from django import forms
class ProfileForm(forms.Form):
    default_station = forms.CharField(label="기본역", required=False)
