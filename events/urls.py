from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/register/', views.register_to_event, name='register_to_event'),
    path('<int:event_id>/unregister/', views.unregister_from_event, name='unregister_to_event'),
    path('<int:event_id>/update/', views.update_event, name='update_event'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
]    