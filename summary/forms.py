from django import forms
from summary.models import Post

class HomeForm(forms.ModelForm):
	website = forms.CharField(widget = forms.TextInput(
		attrs = {
			'class':'form-control',
		}

		))

	class Meta:
		model = Post
		fields = ('website',)