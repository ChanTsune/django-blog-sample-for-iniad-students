from django.urls import path
from . import views

urlpatterns = [
    # name は テンプレート内で{% url 'name' %}のように使う
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("article/all/", views.article_all, name="article_all"),
    path("article/<int:pk>/", views.view_article, name="view_article"),
    path("article/<int:pk>/edit/", views.edit, name="edit"),
    path("article/<int:pk>/delete/", views.delete, name="delete"),
    path("article/<int:pk>/like/", views.like, name="like"),
    path("api/like/<int:pk>/", views.api_like, name="api_like"),
    # <int> で数字にマッチするURLを受け付ける.
    # <int:pk> の pk は views.py の関数で受け取る第二引数の名前と合わせる
]
