from django.shortcuts import render, redirect
from .models import Event 
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib import messages
from .forms import EventForm

# Create your views here.

class EventListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    permission_required = ['users.can_view_events', 'users.can_view_own_registrations']
    ordering = ['date']
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['participated_events'] = self.get_queryset().filter(registrations=user)
        context['organized_events'] = self.get_queryset().filter(organizer=user)
        
        return context


@login_required
@permission_required('users.can_create_event', raise_exception=True)
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
@permission_required('users.can_register_himself', raise_exception=True)
def register_to_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.user in event.registrations.all():
        messages.warning(request, 'You are already booked for this event.')
    else:
        event.registrations.add(request.user)
        messages.success(request, "You booked the event.")

    return redirect('events:event_list')

@login_required
@permission_required('users.can_unregister_himself', raise_exception=True)
def unregister_from_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.user not in event.registrations.all():
        messages.warning(request, 'You are not registered for this event.')
    else:
        event.registrations.remove(request.user)
        messages.success(request, "You unregistered from the event.")

    return redirect('events:event_list')

@login_required
@permission_required('users.can_edit_own_event', raise_exception=True)
def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Event updated successfully.")
            return redirect('events:event_list')
        else:
            print(form.errors)
            messages.error(request, "Error updating event.")
            return render(request, 'events/manage_event.html', {'form': form, 'success': False, 'update': True})

    return render(request, 'events/manage_event.html', {'form': EventForm(instance=event), 'event': event, 'update': True})

@login_required
@permission_required('users.can_delete_own_event', raise_exception=True)
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if event:
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('events:event_list')

    return redirect('events:event_list')