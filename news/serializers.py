from rest_framework import serializers
from .models import Article, Category, Rating 

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'category', 'publishing_time', 'author', 'image', 'average_rating']

    def update(self, instance, validated_data):
        # Update instance fields selectively based on validated_data
        instance.title = validated_data.get('title', instance.title)
        # ... update other fields as needed
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

