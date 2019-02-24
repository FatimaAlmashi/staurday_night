"""saturday_night URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies import views
from api.views import (
    MovieList,
    MovieDetail,
    MovieCreate,
    MovieUpdate,
    MovieDelete,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', views.movie_list, name='movie-list'),
    path('<int:movie_id>/', views.movie_detail, name='movie-detail'),

    path('add/', views.add_movie, name='add-movie'),
    path('<int:movie_id>/update/', views.update_movie, name='update-movie'),
    path('<int:movie_id>/delete/', views.delete_movie, name='delete-movie'),

    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

	path('pizza/<int:movie_id>/', views.favorite, name='favorite'),

	path('tvshows/', views.tv_show_search, name='tv-show-api'),


    path('api/', MovieList.as_view(), name='api-list'),
    path('api/<int:movie_id>/', MovieDetail.as_view(), name='api-detail'),
    path('api/add/', MovieCreate.as_view(), name='api-create'),
    path('api/<int:movie_id>/update/', MovieUpdate.as_view(), name='api-update'),
    path('api/<int:movie_id>/delete/', MovieDelete.as_view(), name='api-delete'),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)