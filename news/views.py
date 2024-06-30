from rest_framework import viewsets, status, filters, pagination
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Article, Category, Rating
from .serializers import ArticleSerializer, CategorySerializer, RatingSerializer
from accounts.permissions import IsEditor
from accounts.models import CustomUser

class ArticlePagination(pagination.PageNumberPagination):
    page_size = 5  # items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__username', 'category__name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsEditor]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
     # custom query kortechi
    def get_queryset(self):
        queryset = super().get_queryset() # 7 no line ke niye aslam ba patient ke inherit korlam
        print(self.request.query_params)
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(author_id=user_id)
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def create(self, request, *args, **kwargs):  # use create instead of post
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        
        # Send email
        email_subject = "Your Review Submitted!"
        email_body = render_to_string('review_email.html', {'review': review})
        email = EmailMultiAlternatives(email_subject, '', to=[review.user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()
        return Response({"detail": "Check your email for Review Submitted"}, status=status.HTTP_201_CREATED)
        
    def get_queryset(self):
        queryset = super().get_queryset() # 7 no line ke niye aslam ba patient ke inherit korlam
        print(self.request.query_params)
       category_id = self.request.query_params.get('category_id')
        if user_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
