from django.contrib import admin
from django.urls import path, re_path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/users$', views.UserView.as_view()),
    re_path(r'^api/users/(?P<id>\d+)?',views.UserView.as_view()),
]
