from django.shortcuts import render, redirect
from .models import AvailableTime, ScheduleHubGroup
from django.contrib.auth import authenticate, login, logout
from .forms import registerForm, getStartAndEndDatesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic

# Create your views here.

def index(request):
    """
    View for welcome page of website
    """
    return render(request, 'index.html')

class AvailabilityListView(LoginRequiredMixin, generic.ListView):
    """
    View for showing user availability
    Requires auth
    """
    model =  AvailableTime
    template_name = 'available_time.html'
    paginate_by = 10

    # methods
    def get_queryset(self):
        # get all instances that relate to the user who made the request
        return AvailableTime.objects.filter(user=self.request.user)


@login_required
def getAvailableTime(request):
    """
    Gets available time from form and saves it
    """
    if request.method == 'POST':
        form = getStartAndEndDatesForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('startTime')
            end = form.cleaned_data.get('endTime')
            AvailableTime.objects.create(startTime=start, endTime=end, user=request.user)
            return redirect(AvailabilityListView.as_view())
        else:
            return render(request, 'add_availability.html', {'form': getStartAndEndDatesForm()})
    else:
        return render(request, 'add_availability.html', {'form': getStartAndEndDatesForm()})


def registerUser(request):
    """
    View for registering new users
    """
    if request.method == 'POST':
        # if good, set up user form and get data
        form = registerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('my-time')
        else:
            return render(request, 'register.html', {'form': registerForm()})
    else:
        # else, set up user form and try again
        return render(request, 'register.html', {'form': registerForm()})


def loginUser(request):
    """
    View for logging users in
    """


def logoutUser(request):
    """
    View for logging users out
    """
    logout(request)
    # return a success logout page
