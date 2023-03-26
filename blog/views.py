from django.shortcuts import render
from blog.models import Comment, Post, Tag


def serialize_post(post):

    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': serialize_tag(post),
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_count,
    }


def move_number_posts(most_popular_posts, most_popular_tags):

    for most_popular_post in zip(most_popular_posts, most_popular_tags):

        most_popular_post[0].posts_count = most_popular_post[1].posts_count
        most_popular_post[0].title = most_popular_post[1].title


def index(request):
    most_popular_posts = Post.objects.popular()[:5].loading_db_queries().fetch_with_comments_count()
    most_popular_tags = Tag.objects.popular()[:5].fetch_with_posts_count()
    move_number_posts(most_popular_posts, most_popular_tags)

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post(post) for post in most_popular_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    serialized_comments = []

    most_popular_posts = Post.objects.popular()[:5].loading_db_queries().fetch_with_comments_count()
    most_popular_tags = Tag.objects.popular()[:5].fetch_with_posts_count()
    move_number_posts(most_popular_posts, most_popular_tags)

    post = Post.objects.get(slug=slug)
    comments = Comment.objects.prefetch_related('author').filter(post=post)

    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes.count(),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in most_popular_posts],
    }

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    most_popular_posts = Post.objects.popular()[:20].loading_db_queries().fetch_with_comments_count()
    most_popular_tags = Tag.objects.popular()[:20].fetch_with_posts_count()

    move_number_posts(most_popular_posts, most_popular_tags)

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags[:5]],
        'posts': [serialize_post(post) for post in most_popular_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts[:5]
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
