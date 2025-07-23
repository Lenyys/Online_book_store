from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import path, include

# Vlastní view funkce
from accounts.views import user_logout, SignUpView
from eshop.views import (
    home,
    CategoryListView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage
    path('', home, name='home'),

    # Eshop aplikace (napojení na další urls.py, pokud používáš)
    path('eshop/', include(('eshop.urls', 'eshop'), namespace='eshop')),


        # Uživatelské účty
    path('accounts/login/', LoginView.as_view(template_name='form.html'), name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='form.html'), name='password_change'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Pro servírování mediálních souborů v režimu DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
