from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',  include('user.urls')),
    path('library/', include('library.urls')),
    path('auth/', include('auth.urls')),
    path('search/', include('elastic_app.urls')),
    path('auth/', include('auth.urls')),
    path('map/',  include('map.urls')),
    path('management/',  include('management.urls'))
]
