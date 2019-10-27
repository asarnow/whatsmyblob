from django import forms
from blobapp.models import MapFile

class MapFileForm(forms.ModelForm):
    class Meta:
        model = MapFile
        fields = ('name', 'map_file', )