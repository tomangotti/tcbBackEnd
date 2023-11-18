
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("ususers.urls")),
    path('recipes/', include("recipes.urls")),
    path('render/', include("render.urls")),
    path('websocket_app/', include("websocket_app.urls")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)