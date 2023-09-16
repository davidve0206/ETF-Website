from django import forms
from .models import BasicUser

class BasicUserForm(forms.ModelForm):
    
    class Meta():
        model = BasicUser
        fields = ("email", "name", "inv_term", "inv_objective", "loss_absortion")
        labels = {
            "email": "Please enter your email",
            "name": "What's your name?",
            "inv_term": "How long do you plan to hold your investment?",
            "inv_objective": "What is your priority for this investment?",
            "loss_absortion": "How much can you afford to lose if things don't go as planned?"}