"""coordinates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from coordinatesapi.views import WeddingView, GuestView, ReceptionTableView, check_user, register_user, PlannerView, GroupView, GuestListView, UnseatedGuestView, WeddingListView

router=routers.DefaultRouter(trailing_slash=False)
router.register(r'weddings', WeddingView, 'wedding')
router.register(r'guests', GuestView, 'guest')
router.register(r'reception_tables', ReceptionTableView, 'reception_table')
router.register(r'planners', PlannerView, 'planner')
router.register(r'groups', GroupView, 'group')
router.register(r'guest_list', GuestListView, 'guest_list')
router.register(r'unseated', UnseatedGuestView, 'unseated')
router.register(r'wedding_list', WeddingListView, 'wedding_list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user),
]
