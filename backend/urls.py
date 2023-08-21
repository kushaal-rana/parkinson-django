from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('execute-script/', ExecutionScriptAPI.as_view()),
    path('get-csv/<str:filename>', GetCsv.as_view()),
]
