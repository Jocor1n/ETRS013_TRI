from django import forms

class Calculer (forms.Form):
    DistanceKM = forms.IntegerField()
    DistanceMetre = forms.IntegerField()
    vitesse = forms.IntegerField()
    autonomie = forms.IntegerField()
    TempsDeChargementHeures =forms.IntegerField()
    TempsDeChargementMinutes = forms.IntegerField()
    
class Trajet (forms.Form):
    VilleDepart = forms.CharField()
    VilleArrivee = forms.CharField()
    Autonomie = forms.IntegerField()
    TempsDeRechargement = forms.IntegerField()
    TempsDeRechargement2 = forms.IntegerField()
