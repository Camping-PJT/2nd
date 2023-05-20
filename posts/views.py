from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, PostImage, Facility
from .forms import PostForm,  PostImageForm, DeleteImageForm, FacilityForm, DeleteFacilityForm
import os
from django.db.models import Q, Count
from utils.map import get_latlng_from_address
from django.http import JsonResponse
from reviews.models import Review
from django.db.models import Prefetch
from taggit.models import Tag
from django.core.paginator import Paginator
from .models import Priority
from django.contrib.auth import get_user_model
import json


def staff_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('main')
    return wrapper


def index(request):
    
    so = request.GET.get('sortKind', '최신순')
    region = request.GET.get('region', '') 

    posts = None

    if so == '최신순':
        posts = Post.objects.order_by('-pk')
    elif so == '인기순':
        posts = Post.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')
    elif so == '별점순':
        posts = Post.objects.order_by('-rating')
    elif so == '댓글순':
        posts = Post.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
    elif so == '방문자순':
        posts = Post.objects.annotate(num_visits=Count('visit_users')).order_by('-num_visits')

    if region:
        posts = posts.filter(city=region)

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
    REGION_CHOICES = [ 
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('경기', '경기'), ('강원', '강원'), ('충북', '충북'), ('충남', '충남'), ('전북', '전북'), ('전남', '전남'), ('경북', '경북'), ('경남', '경남'), ('세종특별자치시', '세종특별자치시'), ('제주특별자치도', '제주특별자치도'),
    ]

    context = {
        'posts': page_obj,
        'sortKind' : so,
        'postall' : posts,
        'region': region,
        'region_choices': REGION_CHOICES,
    }
    return render(request, 'posts/index.html', context)


def theme(request):
    categories = request.GET.getlist('category')
    natures = request.GET.getlist('nature')
    facilities = request.GET.getlist('facility')

    filter_args = Q()
    if categories:
        categories_q = Q()
        for category in categories:
            if category:
                categories_q |= Q(category=category)
        filter_args &= categories_q
    if natures:
        natures_q = Q()
        for nature in natures:
            if nature:
                natures_q |= Q(nature=nature)
        filter_args &= natures_q
    if facilities:
        facilities_q = Q()
        facility_objects = Facility.objects.filter(facility__in=facilities)
        for facility in facility_objects:
            if facility:
                facilities_q |= Q(facility=facility)
        filter_args &= facilities_q
        
    posts = Post.objects.filter(filter_args).distinct()

    post_images = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post, ''))

    context = {
        'posts': post_images,
        'facilities': facilities,
        'postall' : posts,
    }
    return render(request, 'posts/index_theme.html', context)


@login_required
def city(request):
    kakao_script_key = os.getenv('kakao_script_key')
    kakao_key = os.getenv('kakao_key')
    campsites = Post.objects.filter(Q(city__icontains=request.user.region)).order_by('-rating')
    print(campsites)
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


@staff_only
@login_required
def create(request):
    kakao_script_key = os.getenv('kakao_script_key')
    post_form = PostForm()
    image_form = PostImageForm()
    facility_form = FacilityForm()
    
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        files = request.FILES.getlist('image')
        tags = request.POST.get('tags').split(',')
        
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            address = request.POST.get('address')
            post.address = address
            # extra_address = request.POST.get('extra_address')
            # post.extra_address = extra_address
            post.city = address.split(' ')[0]
            post.save()

            for i in files:
                PostImage.objects.create(image=i, post=post)
            
            for tag in tags:
                post.tags.add(tag.strip())
            
            facility_form = FacilityForm(post=post, data=request.POST) 
            
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


@login_required
def detail(request, post_pk):
    kakao_script_key = os.getenv('kakao_script_key')
    kakao_key = os.getenv('kakao_key')
    post = Post.objects.get(pk=post_pk)
    title = post.title
    d_facilities = post.facility_set.all()
    address = post.address
    latitude, longitude = get_latlng_from_address(address)
    reviews = Review.objects.filter(post=post).order_by('-pk')
    page = request.GET.get('page', '1')
    per_page = 5
    paginator = Paginator(reviews, per_page)
    page_obj = paginator.get_page(page)

    context = {
        'kakao_script_key': kakao_script_key,
        'kakao_key': kakao_key,
        'post': post,
        'd_facilities': d_facilities,
        'latitude': latitude,
        'longitude': longitude,
        'reviews': page_obj,
        'paginator': paginator,
        'title': title,
    }
    return render(request, 'posts/detail.html', context)


@staff_only
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
        'post_id': post_pk,
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


@staff_only
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
        posts = Post.objects.filter(Q(title__icontains=query) | Q(address__icontains=query) | Q(tags__name__icontains=query)).distinct()
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
            'postall': posts,
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

        page = request.GET.get('page', '1')
        per_page = 10
        paginator = Paginator(post_images, per_page)
        page_obj = paginator.get_page(page)
    
    context = {
        'tag': tag, 
        'posts': page_obj,
        'postall':posts,
        }
    return render(request, 'posts/tagged_posts.html', context)


def update_priority_lists(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('userId')
        liked_posts = data.get('likedPosts')
        priority_posts = data.get('priorityPosts')

        if user_id and liked_posts and priority_posts:
            for post_id in liked_posts:
                post = Post.objects.get(pk=post_id)
                post.like_users.add(user_id)

            Priority.objects.filter(user_id=user_id).delete()    

            for index, post_data in enumerate(priority_posts):
                post_id = post_data.get('postId')
                Priority.objects.update_or_create(user_id=user_id, post_id=post_id, defaults={'priority': index + 1})
            data = {
                'message': 'Lists updated successfully.',
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'No data received.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def category(request, category):
    so = request.GET.get('sortKind', '최신순')
    region = request.GET.get('region', '') 

    if so == '최신순':
        posts = Post.objects.filter(category=category).order_by('-pk')
    elif so == '인기순':
        posts = Post.objects.filter(category=category).annotate(num_likes=Count('like_users')).order_by('-num_likes')
    elif so == '별점순':
        posts = Post.objects.filter(category=category).order_by('-rating')
    elif so == '댓글순':
        posts = Post.objects.filter(category=category).annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
    elif so == '방문자순':
        posts = Post.objects.filter(category=category).annotate(num_reviews=Count('reviews')).order_by('-num_reviews')   
    
    if region:
        posts = posts.filter(city=region)

    post_images = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post, ''))

    page = request.GET.get('page', '1')
    per_page = 10
    paginator = Paginator(post_images, per_page)
    page_obj = paginator.get_page(page)

    REGION_CHOICES = [ 
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('경기', '경기'), ('강원', '강원'), ('충북', '충북'), ('충남', '충남'), ('전북', '전북'), ('전남', '전남'), ('경북', '경북'), ('경남', '경남'), ('세종특별자치시', '세종특별자치시'), ('제주특별자치도', '제주특별자치도'),
    ]

    context = {
        'posts': page_obj,
        'category': category,
        'sortKind' : so,
        'postall' : posts,
        'region': region,
        'region_choices': REGION_CHOICES,
    }
    return render(request, 'posts/index.html', context)

