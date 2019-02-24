from rest_framework import serializers
from movies.models import Movie, Genre, Favorite
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email']


class FavoriteSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Favorite
		fields = ['user']


class GenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = ['id', 'title']


class MovieListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
			view_name = 'api-detail',
			lookup_field = 'id',
			lookup_url_kwarg = 'movie_id',
		)
	class Meta:
		model = Movie
		fields = ['id', 'title', 'detail']


class MovieDetailSerializer(serializers.ModelSerializer):
	added_by = UserSerializer()
	genres = GenreSerializer(many=True)
	favorites = FavoriteSerializer(many=True)
	favorite_count = serializers.SerializerMethodField()
	class Meta:
		model = Movie
		fields = '__all__'

	def get_favorite_count(self, obj):
		return obj.favorites.count()


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		exclude = ['added_by',]
