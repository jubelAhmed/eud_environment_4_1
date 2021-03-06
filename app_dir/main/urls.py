from . import views
from .views import ActuatorListApiView
from django.urls import path, include
from rest_framework import routers
from app_dir.main import app_creator, post_functions, save_composition

# from app_dir.main import generated_functions

router = routers.DefaultRouter()
router.register('actuators', views.ActuatorAPI)
router.register('sensors', views.SensorAPI)
router.register('service_registry', views.ServiceRegistryAPI)
router.register('mail_box', views.MailBoxAPI)
router.register('api', views.APInterfaceAPI)
router.register('save_composition', views.SaveCompositionAPI)
router.register('interactive', views.InteractiveAPI)

app_name = "main"

urlpatterns = [
    path('', views.register, name='register'),
    path('home/', views.home, name='home_url'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('save_composition/', views.save_composition, name='save_composition'),

    path('api/', include(router.urls)),
    path('Label/', post_functions.Label, name='Label'),
    path('Read/', post_functions.Read, name='Read'),
    path('Search/', post_functions.Search, name='Search'),

    path('news/', post_functions.news, name='news'),
    path('doctor/', post_functions.doctor, name='doctor'),
    path('cricket/', post_functions.cricket, name='cricket'),
    path('recipe_puppy/', post_functions.recipe_puppy, name='recipe_puppy'),
    path('newspaper_headlines/', post_functions.newspaper_headlines, name='newspaper_headlines'),
    path('Send/', post_functions.Send, name='Send'),
    path('weather_info/', post_functions.weather_info, name='weather_info'),
    path('app_creator/', app_creator.create_app, name='app_creator'),
    path('save_composition/',save_composition.save_com, name='save_composition'),
    path('eud_code/', views.eud_code, name='status'),
    path('actuators/', ActuatorListApiView.as_view(), name="actuator_filter"),
    path('app/', views.NewApp, name="new_app"),
    path('ajax_live_data/', views.get_live_data, name="live_data_update"),
]
