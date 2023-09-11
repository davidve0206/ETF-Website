from django.contrib import messages

acceptable_terms = ["short", "mid", "long"]
acceptable_objectives = ["growth", "safeguard"]
acceptable_absortions = ["low", "mid", "high"]

def get_risk_rating(*, term, obj, absortion):
    """ Get the risk rating of the person (from 0-2) depedinding on their
        investment term, objectives and loss absortion capacity"""
    
    # Raise an error if the values of the keyword arguments are not appropriate
    if (term not in acceptable_terms) | (obj not in acceptable_objectives) | (absortion not in acceptable_absortions):
        raise ValueError("You used an invalid input")
    
    if term == "short":
        if (obj == "growth") & (absortion == "high"):
            return 1
        else:
            return 0
    elif term == "mid":
        if obj == "safeguard":
            if absortion == "high":
                return 1
            else:
                return 0
        else:
            if absortion == "high":
                return 2
            elif absortion == "mid":
                return 1
            else:
                return 0
    else:
        if obj == "safeguard":
            if absortion == "low":
                return 0
            else:
                return 1
        else:
            if absortion == "low":
                return 1
            else:
                return 2


