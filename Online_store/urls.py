from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import path, include
from accounts.views import custom_login_view, SignUpView,user_logout
from eshop.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('eshop/', include('eshop.urls')),
    #path('accounts/login/', LoginView.as_view(template_name='form.html'), name='login'),
    path('accounts/', include('accounts.urls')),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='form.html'), name='password_change'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
