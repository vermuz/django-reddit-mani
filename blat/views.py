from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Blat

# Create your views here.
# Using helper render
#def home(request):
	# Render template blat.html
	#return render(request, 'blat/home.html', {'message': 'Rapid Django'})

# Inherits from ListView
class IndexView(generic.ListView):
	template_name = 'blat/home.html'
	context_object_name = 'blat_list'

    # DB query to fetch data
    # - (newest first)
	def get_queryset(self):
		#return Blat.objects.order_by('-created_on')[:20]
		# to decrease number of queries on the page
		return Blat.objects.select_related('created_by').order_by('-created_on')[:20]

class DetailView(generic.DetailView):
	model = Blat
	template_name = 'blat/detail.html'
	context_object_name = 'blat'

class MyView(IndexView):

	def get_queryset(self):
		return Blat.objects.filter(created_by=self.request.user.id) \
		.order_by('-created_on')[:20]

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MyView, self).dispatch(*args, **kwargs)

class NewBlatView(generic.edit.CreateView):
	model = Blat
	fields = ['text', 'via']
	success_url = "/my/"
     
    # This properly sets the created by property
	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(NewBlatView, self).form_valid(form)

class EditBlatView(generic.edit.UpdateView):
	model = Blat
	fields = ['text', 'via']
	success_url = "/my/"

	#To ensure you can only edit your own blat
	def get_queryset(self):
		base_qs = super(EditBlatView, self).get_queryset()
		return base_qs.filter(created_by=self.request.user)