from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin_/', admin.site.urls),
    path('', include('store.urls')),  # Keep
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

import os
from django.views.static import serve
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'static'),
        }
    ),
]