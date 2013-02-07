# -*- coding: utf-8 -*-
from annoying.decorators import render_to, ajax_request
from django.utils import simplejson
from django.http import HttpResponseRedirect
from told.forms import PostForm
from told.models import *
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, date
from django.template.loader import render_to_string
import datetime

@render_to("index.html")
def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.add(request.POST)
            post.save()
            return HttpResponseRedirect("/")
    else:
        form = PostForm()
    posts = Post.objects.filter().order_by('-date')
    event_date_arr = []
    today = date.today()
    event_date_arr.append({'key': 'сегодня', 'value': today + timedelta(days = 1)})
    event_date_arr.append({'key': 'завтра', 'value': today + timedelta(days = 2)})
    event_date_arr.append({'key': 'послезавтра', 'value': today + timedelta(days = 3)})
    event_date_arr.append({'key': 'на этой неделе', 'value': today + timedelta(days = 7 - today.isoweekday())})
    if today.month == 12:
        next_month = date(int(today.year) + 1, 1, 1)
    else:
        next_month = date(today.year, int(today.month) + 1, 1)
    event_date_arr.append({'key': 'в этом месяце', 'value': next_month})
    event_date_arr.append({'key': 'в этом году', 'value': date(int(today.year) + 1, 1, 1)})

    short_comments = ShortComment.objects.all()

    post_short_comments = PostShortComments.objects.filter(post__in=posts)

    return {'event_date_arr': event_date_arr, 'form': form, 'posts': posts, 'category': Category.objects.all(),
            'short_comments': short_comments, 'now': datetime.datetime.now(), 'post_short_comments': post_short_comments}

@csrf_exempt
def ajax_post_agree(request):
    try:
        try:
            post_id = int(request.POST['post_id'])
        except ValueError:
            post_id = 0
        post = Post.objects.get(id=post_id)
        if request.POST['agree'] == "true":
            post.agree_count = post.agree_count + 1
        else:
            post.disagree_count = post.disagree_count + 1
        post.save()
        return HttpResponse(simplejson.dumps({'success': True, 'agree_count': post.agree_count,\
                                              'disagree_count': post.disagree_count}), content_type="application/json")
    except Post.DoesNotExist: pass
    return HttpResponse(simplejson.dumps({'success': False}), content_type="application/json")

@csrf_exempt
def ajax_add_short_comments_post(request):
    if 'post_id' in request.POST and 'short_comment_id' in request.POST:
        try:
            try:
                post_id = int(request.POST['post_id'])
            except ValueError:
                post_id = 0
            post = Post.objects.get(id=post_id)
            try:
                try:
                    short_comment_id = int(request.POST['short_comment_id'])
                except ValueError:
                    short_comment_id = 0
                short_comment = ShortComment.objects.get(id=short_comment_id)
                try:
                    post_short_comments = PostShortComments.objects.get(short_comment = short_comment, post = post)
                    post_short_comments.count = post_short_comments.count + 1
                except PostShortComments.DoesNotExist:
                    post_short_comments = PostShortComments(count = 1, post = post, short_comment = short_comment)
                post_short_comments.save()
                return HttpResponse(simplejson.dumps({'success': True,\
                        'short_comment_count': post_short_comments.count}), content_type="application/json")
            except ShortComment.DoesNotExist: pass
        except Post.DoesNotExist: pass
    return HttpResponse(simplejson.dumps({'success': False}), content_type="application/json")


@csrf_exempt
@ajax_request
def ajax_add_user_post_short_comment(request):
    key_text = 'user_post_short_comment'
    if 'post_id' in request.POST and key_text in request.POST and len(request.POST[key_text]) > 0:
        try:
            post_id = int(request.POST['post_id'])
        except ValueError:
            post_id = 0
        try:
            post = Post.objects.get(id=post_id)
            post_comment = PostShortCommentsUser(text = request.POST[key_text], post = post)
            post_comment.save()
            return {'success': True, 'text': post_comment.text}
        except Post.DoesNotExist: pass
    return {'success': False}

@csrf_exempt
@render_to("post_edit.html")
def post_edit(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound(render_to_string('404.html'))
    if request.method == "POST":
        post.edit(request.POST)
        post.save()
    return {'post': post, 'category': Category.objects.all()}