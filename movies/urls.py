from django.urls import path,include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'viewset-movies', views.MovieViewSet)

urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('api-view', views.MovieApiView.as_view(), name='api-view'),
    path('<int:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    # path('modelmoview/',views.MovieViewSet,name="modelmoview")
    path("router/",include(router.urls))
]