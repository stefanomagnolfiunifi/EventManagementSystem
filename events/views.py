from django.shortcuts import render
from .models import Event 
from django.contrib.auth.decorators import login_required
from .forms import EventForm

# Create your views here.

@login_required
def event_list(request):
    events = Event.objects.all()
    participated_events = events.filter(registrations=request.user)
    organized_events = events.filter(organizer=request.user)
    return render(request, 'events/event_list.html', {'events': events, 'participated_events' : participated_events, 'organized_events': organized_events})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            print("Event created successfully")
            return render(request, 'events/create_event.html', {'form': form, 'success': True})
        else:
            print("Form is not valid")
            print(form.errors)
            return render(request, 'events/create_event.html', {'form': form, 'success': False})
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form, 'success': False})