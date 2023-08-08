from django.urls import include, path


urlpatterns = [
    path('auth/signup/', sign_up_user),
    path('auth/token/', get_jwt_token),
    path('', include(router.urls)),
]