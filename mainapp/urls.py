
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.stockpicker, name='stockpicker'),

    path('stocktracker', views.stocktracker, name='stocktracker'),

    path('postlist', views.post_list, name='postlist'),
    
    path('post-create', views.post_create, name='post-create'),
    
    path('post-detail/<int:id>/', views.post_detail, name='post-detail'),
    
    path('post-update/<int:id>', views.post_update, name='post-update'),
    
    path('post-delete/<int:id>/', views.post_delete, name='post-delete'),
]
