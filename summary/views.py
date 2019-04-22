from django.shortcuts import render,redirect
from summary.forms import HomeForm
from summary import scrape_sum

# Create your views here.
def home(request):
	if request.method == 'POST':
		form = HomeForm(request.POST)
		if form.is_valid():
			form.save()
			url = form.cleaned_data.get('website')

			summary = scrape_sum.textSummarization(url)

			context = {"text" : summary, "url" : url}

			return render(request,'summary/ans.html', context)
	else:
		form = HomeForm()
	return render(request,'summary/home.html',{'form':form})


def ans(request):

	return render(request,'summary/ans.html')

