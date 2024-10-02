from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, timedelta
from .models import DateRange
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score, f1_score
import matplotlib.pyplot as plt
import os
import pickle
from django.conf import settings
from .predictionrgk import predict_prices
# Sample pulse data (you can replace this with a database query)
global from_date_main,to_date_main
# Create your views here.
def main(request):
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        # Store the dates in the session
        request.session['from_date'] = from_date
        request.session['to_date'] = to_date
        # Redirect to the new page (data will be retrieved from session)
        return redirect('show_dates')
    
    return render(request, "home/home.html")


def show_dates(request):
    # Retrieve the dates from the session
    from_date = request.session.get('from_date')
    to_date = request.session.get('to_date')
    if from_date and to_date:
        # Save the dates to the database
        date_range = DateRange(from_date=from_date, to_date=to_date)
        date_range.save()
    context = {
        'from_date': from_date,
        'to_date': to_date
    }

    # Optionally clear the session data after use
    request.session.pop('from_date', None)
    request.session.pop('to_date', None)

    return render(request, "home/show_dates.html", context)
# New view to handle AJAX request for pulse data
def get_pulse_data(request):
    pulse = request.GET.get('pulse')
    date_range = DateRange.objects.latest('created_at')
    fr_date=date_range.from_date
    tt_date=date_range.to_date
    df=predict_prices(fr_date,tt_date)
    PULSE_DATA={}
    PULSE_DATA = {}

    # Loop through columns (excluding 'date') and construct the dictionary
    for pulse in df.columns[1:]:
        PULSE_DATA[pulse] = {
            'name': pulse.replace('_', ' ').title(),
            'prices': df[pulse].tolist(),
            'dates': df['Date'].tolist()
        }    
    if pulse in PULSE_DATA:
        data = PULSE_DATA[pulse]
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid pulse selection'}, status=400)
