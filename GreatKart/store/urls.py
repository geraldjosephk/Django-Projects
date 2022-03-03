from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),  # registering home page
    # register categories in store,
    path('<slug:category_slug>/', views.store, name='products_by_category')
]
