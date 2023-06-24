from django.shortcuts import render, redirect, get_object_or_404
from .models import Post,  Message, Topic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import PostForm
from django.core.paginator import Paginator
from django.http import HttpResponse
# Create your views here.


def adminApproval(request):
    posts = Post.objects.all()
    context = {'posts': posts}

    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            posts.update(approved=False)
            for x in id_list:
                Post.objects.filter(id=str(x)).update(approved=True)
            return redirect('posts')
        return render(request, 'blog/admin_approval.html', context)
    else:
        return HttpResponse('You are not allowed here')


def posts(request):
    q = request.GET.get('q') if request.GET.get("q") != None else ''
    posts = Post.objects.filter(Q(title__icontains=q) | Q(
        description__icontains=q) | Q(topic__name__icontains=q)).exclude(approved=False)
    page = Paginator(posts, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {'posts': posts, 'page': page}
    return render(request, 'blog/posts.html', context)


def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all()
    context = {'post': post, 'post_messages': post_messages}
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='login')
def postCreate(request):
    page = 'create'
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Post.objects.create(
            author=request.user,
            topic=topic,
            featured_image=request.FILES.get('featured_image'),
            title=request.POST.get('title'),
            description=request.POST.get('description')
        )

        return redirect('posts')
    context = {'form': form, 'topics': topics, 'page': page}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url='login')
def postUpdate(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.user != post.author:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        post.title = request.POST.get('title')
        post.topic = topic
        post.featured_image = request.FILES.get('featured_image')
        post.description = request.POST.get('description')
        post.save()
        return redirect('posts')
    context = {'form': form, 'post': post}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url='login')
def postDelete(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'obj': post}
    return render(request, 'blog/delete.html', context)


@login_required(login_url='login')
def messageDelete(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.user == message.user:
        message.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('You are not allowed here')


def adminDelete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('admin_approval')


@login_required(login_url='login')
def postLike(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id):
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def createComment(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        body = request.POST.get('body')
        user = request.user
        new_comment = Message(post=post, user=user, body=body)
        new_comment.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def replyComment(request, post_id, message_id):
    parent_comment = Message.objects.get(id=message_id)
    if request.method == 'POST':
        body = request.POST.get('body')
        user = request.user
        post = Post.objects.get(id=post_id)
        new_comment = Message(post=post,
                              user=user, body=body, parent=parent_comment)
        new_comment.save()
    return redirect(request.META.get('HTTP_REFERER'))
