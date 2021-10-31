from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('process_reg', views.process_reg),
    path('process_login', views.process_login),
    path('movies', views.display_home),
    path('upload_movie', views.upload_movie),
    path('logout', views.logout),
    path('delete_movie/<int:this_movie_id>', views.delete_movie),
    path('display_movie/<int:this_movie_id>', views.render_display_movie),
    path('update_movie/<int:this_movie_id>', views.update_movie),
    path('add_to_likes/<int:this_movie_id>', views.add_to_likes),
    path('remove_from_likes/<int:this_movie_id>', views.remove_from_likes)
    # path('add_movie', views.add_movie)
]
