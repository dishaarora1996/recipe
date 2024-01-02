from django.urls import path
from . import views

urlpatterns =[
    path('api/login/', views.UserLoginView.as_view(),name='login'),
    # path('api/token/refresh/',views.CustomTokenRefreshView.as_view(),name ='token-refresh'),
    path('api/change-password/',views.ChangePassword.as_view(),name ='change-password'),
    path('api/authenticated_testview/',views.AuthorizedOnly.as_view(),name="authorized_space"),
    path('api/send-reset-password-email/', views.SendPasswordResetEmailView.as_view(), name="send-reset-password-email"),
    path('api/reset-password/<uid>/<token>/', views.UserPasswordResetView.as_view(), name="reset-password"),
]
