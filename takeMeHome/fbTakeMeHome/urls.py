from django.conf.urls import include, url
from .views import takeMeHomeView
from helpers.consts import URL_HEX_RAND

urlpatterns = [
    url(URL_HEX_RAND, takeMeHomeView.as_view())
]

