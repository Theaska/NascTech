from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Func API',
        default_version='v1',
        contact=openapi.Contact(email="tach.pu@gmail.com"),
        license=openapi.License(name="Theaska BSD"),
    ),
    public=True
)

urlpatterns = [
    path('', schema_view.with_ui()),
    path('start/', include('main.urls', namespace='main')),
    path('admin/', admin.site.urls),
]
