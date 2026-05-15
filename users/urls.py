from django.urls import path
from .views import signup_view, CustomLoginView, logout_view, dashboard_view
from .views import user_api
from django.urls import path
from .views import (
    home_view,
    signup_view,
    CustomLoginView,
    logout_view,
    dashboard_view,
    profile_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),

    path('api/users/', user_api, name='user_api'),
    path('profile/', profile_view, name='profile'),
]