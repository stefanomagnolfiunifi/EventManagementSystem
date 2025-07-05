from django.shortcuts import render, redirect
from .models import Event 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            messages.success(request, "Event created successfully.")
            return render(request, 'events/manage_event.html', {'form': EventForm(), 'success': True, 'update': False})
        else:
            messages.error(request, "Error creating event.")
            return render(request, 'events/manage_event.html', {'form': form, 'success': False, 'update': False})
    else:
        form = EventForm()

    return render(request, 'events/manage_event.html', {'form': form, 'success': False, 'update': False})

@login_required
def register_to_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.user in event.registrations.all():
        messages.warning(request, 'You are already booked for this event.')
    else:
        event.registrations.add(request.user)
        messages.success(request, "You booked the event.")

    return redirect('events:event_list')

@login_required
def unregister_from_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.user not in event.registrations.all():
        messages.warning(request, 'You are not registered for this event.')
    else:
        event.registrations.remove(request.user)
        messages.success(request, "You unregistered from the event.")

    return redirect('events:event_list')

@login_required
def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Event updated successfully.")
            return redirect('events:event_list')
        else:
            messages.error(request, "Error updating event.")

    return render(request, 'events/manage_event.html', {'form': EventForm(instance=event), 'event': event, 'update': True})

@login_required
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if event:
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('events:event_list')

    return redirect('events:event_list')