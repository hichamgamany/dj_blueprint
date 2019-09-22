from django.conf.urls import url
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('signup/', user_views.sign_up, name='sign_up'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_views.activate, name='activate'),
    path('registration/confirmation/', user_views.registration_confirmation, name='registration_confirm'),
    path('activation/done/', user_views.activation_done, name='activation_done'),
    path('activation/failed/', user_views.activation_failed, name='activation_failed'),
    path('login/', user_views.UserLoginView.as_view(), name='sign_in'),
    path('logout/', user_views.UserLogoutView.as_view(), name='logout'),
    path('password-reset/', user_views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', user_views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', user_views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', user_views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', user_views.profile_view, name='profile'),
]
