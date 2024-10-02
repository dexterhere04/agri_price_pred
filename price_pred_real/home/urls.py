from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('show_dates/', views.show_dates, name='show_dates'),
    path('get_pulse_data/', views.get_pulse_data, name='get_pulse_data'),  # New route for fetching pulse data
]
