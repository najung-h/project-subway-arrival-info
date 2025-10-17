from django import forms

class StationSearchForm(forms.Form):
    station = forms.CharField(
        label="역명",
        widget=forms.TextInput(attrs={"placeholder": "예) 신도림", "class": "input"})
    )
