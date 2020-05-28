from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm

def post_list(request):
    object_list = Post.objects.filter(status='published')
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,        
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,)
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id,status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # ... Отправка электронной почты.
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {'post': post, 'form': form})