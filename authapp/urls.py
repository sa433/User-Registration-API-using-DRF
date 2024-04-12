from django.urls import path
from authapp.views import UserRegistrationView, UserLoginView, ProfileView, ReferralLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user-details/', UserLoginView.as_view(), name='user-details'),
    path('referral-details/', ReferralLoginView.as_view(), name='referral-details'),
    path('profile-view', ProfileView.as_view(), name='profile'),
    # path('referral-view', ReferralView.as_view(), name='referral')
]