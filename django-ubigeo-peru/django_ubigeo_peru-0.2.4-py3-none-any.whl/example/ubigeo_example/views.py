# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from .forms import IncidentForm
from .models import Incident


def home(request):
    incidents = Incident.objects.all()

    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save()
            return redirect(
                reverse('incident_detail',
                        kwargs={'incident_id': incident.pk, }))
        else:
            return render(request,
                          'index.html',
                          context={'form': form,
                           'incidents': incidents}
                          )
    else:
        form = IncidentForm()
        return render(request,
                      'index.html',
                      context={'form': form,
                       'incidents': incidents}
                      )


def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, pk=incident_id)
    form = IncidentForm(instance=incident)
    incidents = Incident.objects.all()
    context = {
        'form': form,
        'incidents': incidents
    }
    return render(request, 'index.html', context=context)


def remove_incident(request, incident_id):
    incident = get_object_or_404(Incident, pk=incident_id)
    incident.delete()
    return redirect(reverse('home'))
