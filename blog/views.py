from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# Create your views here.


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        print(tag)
        object_list = object_list.filter(tags__in=[tag])
        print([tag])
        paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  # get current page posts
    except PageNotAnInteger:
        posts = paginator.page(1)  # if page is not an integer deliver the first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # if page is out of range deliver last page of result
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    print(post.tags.all())
    post_tags_ids = post.tags.values_list('id', flat=True)
    print(post_tags_ids)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)
    print(similar_posts)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish').exclude(id=post.id)
    comments = post.comments.filter(active=True)  # List of active comments for this post
    commented = False
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            commented = True
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form,
                                                     'commented': commented, 'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')  # Retrieve post by id
    sent = False
    if request.method == 'POST':  # form is submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():  # form fields passed validation
            cd = form.cleaned_data
            # send_email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading {}' .format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {} \n \n{}\'s comments{}' .format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, '2388992177@qq.com', recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})

