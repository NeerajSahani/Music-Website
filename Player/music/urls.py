from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
    path('', views.Home.as_view(), name='HomeView'),
    path('<int:pk>/', views.AlbumView.as_view(), name='AlbumView'),
    path('add album/', views.AlbumAddView.as_view(), name='AddAlbum'),
    path('<int:pk>/update/', views.AlbumUpdateView.as_view(), name='UpdateAlbum'),
    path('del/<int:pk>/', views.AlbumDeleteView.as_view(), name='DeleteAlbum'),
    path('<int:pk>/add song/', views.SongAddView.as_view(), name='AddSong'),
    path('album/<int:pk>/delete', views.SongDeleteView.as_view(), name='DeleteSong'),
    path('album/<int:pk>/update/', views.SongUpdateView.as_view(), name='UpdateSong'),
    path('user login/', views.Login.as_view(), name='login'),
    path('user logout/', views.Logout, name='logout'),
    path('user creation/', views.Registration.as_view(), name='registration'),
]
