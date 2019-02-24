from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)
from movies.models import Movie
from .serializers import(
	MovieListSerializer,
	MovieDetailSerializer,
	MovieCreateUpdateSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsNoob
from rest_framework.filters import SearchFilter, OrderingFilter

class MovieList(ListAPIView):
	queryset = Movie.objects.all()
	serializer_class = MovieListSerializer
	permission_classes = [AllowAny,]
	filter_backends = [SearchFilter, OrderingFilter,]
	search_fields = ['title', 'description',]

class MovieDetail(RetrieveAPIView):
	queryset = Movie.objects.all()
	serializer_class = MovieDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'movie_id'
	permission_classes = [AllowAny,]

class MovieCreate(CreateAPIView):
	serializer_class = MovieCreateUpdateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(added_by=self.request.user)

class MovieUpdate(RetrieveUpdateAPIView):
	queryset = Movie.objects.all()
	serializer_class = MovieCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'movie_id'
	permission_classes = [IsNoob,]

class MovieDelete(DestroyAPIView):
	queryset = Movie.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'movie_id'
	permission_classes = [IsNoob,]
