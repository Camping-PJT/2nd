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
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.post = Post.objects.get(pk=post_pk)
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
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect('posts:detail', review.post.pk)
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