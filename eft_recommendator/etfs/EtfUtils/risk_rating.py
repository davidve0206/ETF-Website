acceptable_terms = ["short", "mid", "long"]
acceptable_objectives = ["growth", "safeguard"]
acceptable_absortions = ["low", "mid", "high"]

risk_rating_dict = {
    "low": 0,
    "mid": 1,
    "high": 2
}

def get_risk_rating(*, term, obj, absortion):
    """ Get the risk rating of the person (from 0-2) depedinding on their
        investment term, objectives and loss absortion capacity"""
    
    # Raise an error if the values of the keyword arguments are not appropriate
    if (term not in acceptable_terms) | (obj not in acceptable_objectives) | (absortion not in acceptable_absortions):
        raise ValueError("You used an invalid input")
    
    if term == "short":
        if (obj == "growth") & (absortion == "high"):
            return risk_rating_dict["mid"]
        else:
            return risk_rating_dict["low"]
    elif term == "mid":
        if obj == "safeguard":
            if absortion == "high":
                return risk_rating_dict["mid"]
            else:
                return risk_rating_dict["low"]
        else:
            if absortion == "high":
                return risk_rating_dict["high"]
            elif absortion == "mid":
                return risk_rating_dict["mid"]
            else:
                return risk_rating_dict["low"]
    else:
        if obj == "safeguard":
            if absortion == "low":
                return risk_rating_dict["low"]
            else:
                return risk_rating_dict["mid"]
        else:
            if absortion == "low":
                return risk_rating_dict["mid"]
            else:
                return risk_rating_dict["high"]


