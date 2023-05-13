from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostImage, Facility
from .forms import PostForm,  PostImageForm, DeleteImageForm, FacilityForm, DeleteFacilityForm
import os
from django.db.models import Q
from utils.map import get_latlng_from_address
from django.http import JsonResponse
from reviews.models import Review, Emote
from django.db.models import Prefetch
from taggit.models import Tag
from django.core.paginator import Paginator



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


def city(request):
    kakao_script_key = os.getenv('kakao_script_key')
    kakao_key = os.getenv('kakao_key')
    campsites = Post.objects.filter(city = request.user.region)
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
        'kakao_script_key': kakao_script_key,
        'kakao_key': kakao_key,
        'campsites': campsites,
    }
    if request.is_ajax():
        return JsonResponse(context)
    return render(request, 'posts/index_city.html', context)


@login_required
def create(request):
    kakao_script_key = os.getenv('kakao_script_key')
    post_form = PostForm()
    image_form = PostImageForm()
    facility_form = FacilityForm()  # Initialize without a post object
    
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        files = request.FILES.getlist('image')
        tags = request.POST.get('tags').split(',')
        
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            address = request.POST.get('address')
            post.address = address
            post.city = address.split(' ')[0]
            post.save()
            
            for tag in tags:
                post.tags.add(tag.strip())
            
            facility_form = FacilityForm(post=post, data=request.POST)  # Pass the post object during initialization
            
            if facility_form.is_valid():
                facility_data = facility_form.cleaned_data['facilities']
                for facility_code in facility_data:
                    Facility.objects.create(post=post, facility=facility_code)
                
                return redirect('posts:detail', post.pk)
    else:
        facility_form = FacilityForm()  # Initialize without a post object
    
    context = {
        'kakao_script_key': kakao_script_key,
        'post_form': post_form,
        'image_form': image_form,
        'facility_form': facility_form,
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


@login_required
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
    return redirect('posts:index')


@login_required
def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'likes_count': post.like_users.count(),
        }
    return JsonResponse(context)


@login_required
def visits(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.visit_users.all():
        post.visit_users.remove(request.user)
        is_visited = False
    else:
        post.visit_users.add(request.user)
        is_visited = True
    context = {
        'is_visited': is_visited,
        'visits_count': post.visit_users.count(),
        }
    return JsonResponse(context)



@login_required
def update(request, post_pk):
    kakao_script_key = os.getenv('kakao_script_key')
    post = Post.objects.get(pk=post_pk)
    facility_form = FacilityForm(post=post)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        facility_form = FacilityForm(post=post, data=request.POST)
        files = request.FILES.getlist('image')
        delete_ids = request.POST.getlist('delete_images')
        delete_form = DeleteImageForm(post=post, data=request.POST)
        delete_facility_form = DeleteFacilityForm(post=post, data=request.POST)
        if post_form.is_valid() and delete_form.is_valid() and facility_form.is_valid() and delete_facility_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            address = request.POST.get('address')
            post.address = address
            post.city = address.split(' ')[0]
            post.save()
            post.tags.clear()
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                stripped_tag = tag.strip().strip('"')
                post.tags.add(stripped_tag)
            post.postimage_set.filter(pk__in=delete_ids).delete()
            for i in files:
                PostImage.objects.create(image=i, post=post)
            facility_data = facility_form.cleaned_data['facilities']
            Facility.objects.filter(post=post).exclude(facility__in=facility_data).delete()
            for facility_code in facility_data:
                Facility.objects.update_or_create(post=post, facility=facility_code)
            
            unchecked_facilities = set(Facility.FACILITY_CHOICES) - set(facility_data)

            delete_f_ids = delete_facility_form.cleaned_data.get('delete_facilities')
            if delete_f_ids:
                Facility.objects.filter(post=post, facility__in=unchecked_facilities).delete()
            return redirect('posts:detail', post.pk)
    else:
        post_form = PostForm(instance=post)
        delete_form = DeleteImageForm(post=post)
        facility_form = FacilityForm(post=post)
        delete_facility_form = DeleteFacilityForm(post=post)
    if post.postimage_set.exists():
        image_form = PostImageForm(instance=post.postimage_set.first())
    else:
        image_form = PostImageForm()
    context = {
        'kakao_script_key': kakao_script_key,
        'post': post,
        'post_form': post_form,
        'image_form': image_form,
        'delete_form': delete_form,
        'facility_form': facility_form,
        'delete_facility_form': delete_facility_form,
    }
    return render(request, 'posts/update.html', context)


def search(request):
    query = request.GET.get('q')

    if query:
        posts = Post.objects.filter( Q(title__icontains=query) | Q(address__icontains=query) )
        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))

        page = request.GET.get('page', '1')
        per_page = 10
        paginator = Paginator(post_images, per_page)
        page_obj = paginator.get_page(page)
    
        context = {
            'query': query,
            'posts': page_obj,
        }
    else:
        context = {}

    return render(request, 'posts/search.html', context)


def tagged_posts(request, tag_pk):
    tag = Tag.objects.get(pk=tag_pk)
    posts = Post.objects.filter(tags=tag)

    post_images = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post,''))


    context = {
        'tag': tag, 
        'posts': posts,
        }
    return render(request, 'posts/tagged_posts.html', context)