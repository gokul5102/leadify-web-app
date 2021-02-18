from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path,include
from leads.views import landing_page,LandingPageView,SignupView
from django.contrib import admin
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,
PasswordResetCompleteView)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LandingPageView.as_view(),name='landing-page'),
    path('leads/',include('leads.urls',namespace='leads')),
    path('agents/',include('agents.urls',namespace='agents')),
    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('logout/',LogoutView.as_view(),name='logout'),
    
    path('reset_password/',PasswordResetView.as_view(template_name="leads/password_reset_form.html"),name="reset_password"),
    path('reset_password_done/',PasswordResetDoneView.as_view(template_name="leads/password_reset_done.html"),name="password_reset_done"),
    path('reset_password_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="leads/password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/',PasswordResetCompleteView.as_view(template_name="leads/password_reset_complete.html"),name="password_reset_complete"),

    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view
    # (template_name="leads/password_reset_done.html"),name="password_reset_complete"),
]

if settings.DEBUG:    # for deployment
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)