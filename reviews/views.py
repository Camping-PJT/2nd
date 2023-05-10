from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm, ReviewImageForm
from posts.models import Post, ReviewImage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required
def create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        review_image_form = ReviewImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.post = Post.objects.get(pk=post_pk)
            review.save()

            for file in files:
                ReviewImage.objects.create(review=review, image=file)
            
            return redirect('posts:detail', post_pk)
    else:
        review_form = ReviewForm()
        review_image_form = ReviewImageForm()
    context = {
        'review_form': review_form,
        'review_image_form': review_image_form,
        'post': post,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, instance=review)
            files = request.FILES.getlist('image')
            if review_form.is_valid():
                review_form.save()
                review_images = ReviewImage.objects.filter(review=review)
                for review_image in review_images:
                    review_image.delete()
                for file in files:
                    ReviewImage.objects.create(review=review, image=file)
                return redirect('posts:detail', review.post.pk)
        else:
            review_form = ReviewForm(instance=review)
            review_image_form = ReviewImageForm()
        context = {
            'review_form': review_form,
            'review_image_form': review_image_form,
            'review': review,
        }
        return render(request, 'reviews/update.html', context)
    else:
        return redirect('posts:detail', review.post.pk)


@login_required
def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    review_images = review.reviewimage_set.all()
    if review.user == request.user:
        for review_image in review_images:
            review_image.delete()
        review.delete()
    return redirect('posts:detail', review.post.pk)