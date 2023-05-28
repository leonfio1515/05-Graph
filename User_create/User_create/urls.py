from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *
####################################################################

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreate.as_view(), name='register'),
    path('user_activate/<str:uidb64>/<str:token>/',UserActivate.as_view(), name='user_activate'),
    path('', IndexView.as_view(), name='home'),
    path('success_register/', SuccessRegister.as_view(), name='success_register'),

    path('client_register/', ClientRegister.as_view(), name='client_register'),
    path('client_list/', ClientList.as_view(), name='client_list'),

    path('user_edit/<int:pk>/', UserEdit.as_view(), name='user_edit'),
    path('password_edit/<int:pk>/', PasswordEdit.as_view(), name='password_edit'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
