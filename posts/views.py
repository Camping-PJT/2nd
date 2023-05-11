from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostImage, Facility
from .forms import PostForm,  PostImageForm, DeleteImageForm, FacilityForm
import os
from utils.map import get_latlng_from_address
from reviews.models import Review, Emote
from django.db.models import Prefetch


def index(request):
    posts = Post.objects.order_by('-pk')
    post_images = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post,''))
    context = {
        'post_images': post_images,
    }
    return render(request, 'posts/index.html', context)


def create(request):
    kakao_script_key = os.getenv('kakao_script_key')
    post_form = PostForm()
    image_form = PostImageForm()
    facility_form = FacilityForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        facility_form = FacilityForm(request.POST)
        files = request.FILES.getlist('image')
        tags = request.POST.get('tags').split(',')
        if post_form.is_valid() and facility_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user

            address = request.POST.get('address')
            post.address = address

            # city = request.POST.get('id_city')

            post.city = address.split(' ')[0]

            post.save()

            for tag in tags:
                post.tags.add(tag.strip())

            for i in files:
                PostImage.objects.create(image=i, post=post)

            facility_data = facility_form.cleaned_data['facilities']
            for facility_code in facility_data:
                Facility.objects.create(post=post, facility=facility_code)

            return redirect('posts:detail', post.pk)
    context = {
        'kakao_script_key': kakao_script_key,
        'post_form': post_form,
        'image_form': image_form,
        'facility_form': facility_form
    }
    return render(request, 'posts/create.html', context)


def detail(request, post_pk):
    kakao_script_key = os.getenv('kakao_script_key')
    post = Post.objects.get(pk=post_pk)
    facilities = Facility.objects.filter(post=post)
    address = post.address
    latitude, longitude = get_latlng_from_address(address)

    if request.user.is_authenticated:
        reviews = Review.objects.filter(post=post).prefetch_related(
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=1), to_attr='likes'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=1, user=request.user), to_attr='like_exist'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=2), to_attr='dislikes'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=2, user=request.user), to_attr='dislike_exist')
        ).order_by('-pk')
    else:
        reviews = Review.objects.filter(post=post).prefetch_related(
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=1), to_attr='likes'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=2), to_attr='dislikes'),
        ).order_by('-pk')

    context = {
        'kakao_script_key': kakao_script_key,
        'post': post,
        'facilities': facilities,
        'latitude': latitude,
        'longitude': longitude,
        'reviews': reviews
    }
    return render(request, 'posts/detail.html', context)