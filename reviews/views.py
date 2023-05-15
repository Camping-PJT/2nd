from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from posts.models import Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required
def create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    rating = request.POST.get('rating')
    if rating is None:
        rating = 5
    else:
        try:
            rating = int(rating)
        except ValueError:
            rating = 5
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.post = post
            review.rating = rating
            review.save()
            return redirect('posts:detail', post_pk)
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
        'post': post,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    rating = request.POST.get('rating')
    if rating is None:
        rating = 5
    else:
        try:
            rating = int(rating)
        except ValueError:
            rating = 5
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                review.rating = rating
                review_form.save()
                return redirect('reviews:detail', review.pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            'review_form': review_form,
            'review': review,
        }
        return render(request, 'reviews/update.html', context)
    else:
        return redirect('posts:detail', review.post.pk)


@login_required
def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
    return redirect('posts:detail', review.post.pk)


def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    context = {
        'review': review,
    }
    return render(request, 'reviews/detail.html', context)


# @login_required
# def emotes(request, review_pk, emotion):
#     review = Review.objects.get(pk=review_pk)
    
#     my_emote = Emote.objects.filter(review=review, user=request.user)
#     input_emote = Emote.objects.filter(review=review, user=request.user, emotion=emotion)

#     # 기존에 좋아요/싫어요 버튼을 누른 경우 지금 누른 버튼이라면 삭제, 다른 버튼이라면 동작하지 않도록!
#     alert = False
#     if my_emote.exists():
#         is_checked = False
#         if input_emote.exists():
#             input_emote.delete()
#         else:
#             alert = True
#     else:
#         Emote.objects.create(review=review, user=request.user, emotion=emotion)
#         is_checked = True
    
#     cnt = Emote.objects.filter(review=review, emotion=emotion).count()
#     context = {
#         'is_checked': is_checked,
#         'cnt': cnt,
#         'alert': alert,
#     }
#     return JsonResponse(context)

@login_required
def review_likes(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
        r_is_liked = False
    else:
        review.like_users.add(request.user)
        r_is_liked = True
    context = {
        'r_is_liked': r_is_liked,
        'review_likes_count': review.like_users.count(),
        'r_is_disliked': request.user in review.dislike_users.all(),
        'review_dislikes_count': review.dislike_users.count(),
    }
    return JsonResponse(context)

@login_required
def review_dislikes(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.dislike_users.all():
        review.dislike_users.remove(request.user)
        r_is_disliked = False
    else:
        review.dislike_users.add(request.user)
        r_is_disliked = True
    context = {
        'r_is_disliked': r_is_disliked,
        'review_dislikes_count': review.dislike_users.count(),
        'r_is_liked': request.user in review.like_users.all(),
        'review_likes_count': review.like_users.count(),
    }
    return JsonResponse(context)