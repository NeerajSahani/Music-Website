from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class Home(generic.ListView):
    template_name = 'music/HomeView.html'
    context_object_name = 'album'

    def get_queryset(self):
        return models.Album.objects.all()


class AlbumView(generic.DetailView):
    template_name = 'music/DetailView.html'
    model = models.Album


class AlbumAddView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    login_url = '/user login'
    template_name = 'music/UploadAlbum.html'
    context_object_name = 'form'
    model = models.Album
    fields = ['name', 'artist', 'genre', 'released', 'image']

    success_message = 'Album Added successfully '


class AlbumUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = '/user login'
    template_name = 'music/UploadAlbum.html'
    context_object_name = 'form'
    model = models.Album
    fields = ['name', 'artist', 'genre', 'released', 'image']
    success_message = 'Album Updated'


class AlbumDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    login_url = '/user login'
    template_name = 'music/UploadAlbum.html'
    context_object_name = 'form'
    model = models.Album
    success_message = 'Album deleted'
    success_url = reverse_lazy('music:HomeView')


class SongAddView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    login_url = '/user login'
    template_name = 'music/UploadAlbum.html'
    context_object_name = 'form'
    model = models.Song
    fields = ['song_name', 'song_artist', 'duration', 'rating', 'song', 'like']
    success_message = 'Song added'

    def dispatch(self, request, *args, **kwargs):
        self.album_id = self.kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        a = models.Album.objects.get(pk=self.album_id)
        form.instance.album = a
        return super(SongAddView, self).form_valid(form)


class SongDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    login_url = '/user login'
    template_name = 'music/UploadAlbum.html'
    context_object_name = 'form'
    model = models.Song
    success_message = 'Song deleted'
    success_url = reverse_lazy('music:HomeView')


class SongUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = '/user login'
    template_name = 'music/UploadAlbum.html'
    context_object_name = 'form'
    model = models.Song
    fields = ['song_name', 'song_artist', 'duration', 'rating', 'song', 'like']
    success_message = 'Song Updated'


class Login(generic.View):

    def get(self, request):
        return render(request, 'music/UploadAlbum.html', {'form': forms.LogForm()})

    def post(self, request):
        form = forms.LogForm(None or request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            passw = form.cleaned_data.get('password')
            val = authenticate(username=user, password=passw)
            nextpage = self.request.GET.get('next')
            if val:
                login(request, val)
                messages.success(request, 'Logged in')
                if nextpage:
                    return redirect(nextpage)
                else:
                    return redirect('music:HomeView')
            else:
                return redirect('music:login')

        return render(request, 'music/UploadAlbum.html', {'form': form})


class Register(generic.View):

    def get(self, request):
        return render(request, 'music/UploadAlbum.html', {'form': forms.UserForm})

    def post(self, request):
        form = forms.UserForm(request.POST)
        if form.is_valid():
            userobj = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            p1 = form.cleaned_data.get('retype_password')
            if password == p1:
                if not authenticate(username=username, password=password):
                    userobj.set_password(password)
                    userobj.is_staff = True
                    userobj.save()
                    messages.success(request, 'Registered')
                    return redirect('music:HomeView')
                else:
                    return redirect('music:register')
        return render(request, 'music/UploadAlbum.html', {'form': form})


class Registration(generic.CreateView, SuccessMessageMixin):
    form_class = forms.RegistrationForm
    model = User
    context_object_name = 'form'
    success_url = '/user login'
    template_name = 'music/signup.html'
    success_message = 'Thanks for registration'


def Logout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('music:HomeView')


def like(request, pk):
    new_like, created = models.LikeSong.objects.get_or_create(user=request.user, song=pk)
    if not created:
        messages.success(request, 'Already Liked')
    else:
        messages.success(request, 'Thanks for like')