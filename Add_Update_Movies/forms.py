from django import forms

class MovieForm(forms.Form):
    status_choices=(
    ('coming-up','coming-up'),
    ('starting','starting'),
    ('running','running'),
    ('finished','finished'),

)
    name = forms.CharField(label='Movie Name', max_length=100)
    protagonists=forms.CharField(label='Protagonists')
    release_date = forms.DateField(label='Release Date')
    status = forms.ChoiceField(label='Status', choices=status_choices)
    poster = forms.ImageField(label='Poster')
    trailer = forms.FileField(label='Trailer')