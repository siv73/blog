from django.urls import path
from . import views
urlpatterns = [
    path('',views.post_list,name="posts"),
    path('tag/<str:tag_slug>',views.post_list,name="posts"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',views.post_detail,name="detail"),
    path('share/<int:id>',views.send_email_view,name="send")
    
]
