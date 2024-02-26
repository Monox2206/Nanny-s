from django.contrib import admin
from django.urls import path
from tienda import views
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = "tienda"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home, name='inicio' ),

    path("login/", views.login, name="login"),

    path("logout/", views.logout, name="logout"),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

