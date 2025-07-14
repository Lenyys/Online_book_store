"""
URL configuration for Online_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import path, include

from accounts.views import user_logout, SignUpView
from eshop.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('eshop/', include('eshop.urls')),

    path('accounts/login/', LoginView.as_view(template_name='form.html'), name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/password_change/',
         PasswordChangeView.as_view(template_name='form.html'),
         name='password_change'),
    # ostatní defaultní cesty
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    # path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)