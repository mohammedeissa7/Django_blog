from django.urls import path
from . import views
from .views import PostListView, PostUpdateView, PostDetailView, PostDeleteView, PostCreateView




urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('detail/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post-update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('new/', PostCreateView.as_view(), name='post-create'),  
    path('about/', views.about, name='blog-about'),   
]
