from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView

import api

class WifiView(TemplateView):
    template_name = "wifi.html"

    def get_context_data(self, **kwargs):
        context = super(WifiView, self).get_context_data(**kwargs)
        context['networks_str'] = api.networks_json()
        return context

class BatteryView(TemplateView):
    template_name = "battery.html"

    def get_context_data(self, **kwargs):
        context = super(BatteryView, self).get_context_data(**kwargs)
        context['battery_str'] = api.battery_json()
        return context

# API Views, to be used by AJAX update calls
class WifiJsonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(api.networks_json(),
            content_type="application/json")


class BatteryJsonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(api.battery_json(),
            content_type="application/json")