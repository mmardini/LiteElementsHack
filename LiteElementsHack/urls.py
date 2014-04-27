from django.conf.urls import patterns, include, url

import BatteryWifiMonitor.views

urlpatterns = patterns('',
    url(r'^wifi$', BatteryWifiMonitor.views.WifiView.as_view(),
        name='wifi-html'),
    url(r'^battery$', BatteryWifiMonitor.views.BatteryView.as_view(),
        name='battery-html'),

    # API URLs, to be used by AJAX update calls
    url(r'^json/wifi$', BatteryWifiMonitor.views.WifiJsonView.as_view(),
        name='wifi-json'),
    url(r'^json/battery$', BatteryWifiMonitor.views.BatteryJsonView.as_view(),
        name='battery-json'),
)
