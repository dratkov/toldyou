__author__ = 'dim'
from django import template
import datetime
import time
from told.models import Mood, PostShortComments

register = template.Library()

@register.simple_tag
def percent_event_date(date_start, date_end, percent_flag=0):
    start_timestamp = time.mktime(datetime.datetime(*[int(i) for i in date_start.split(' ')[0].split('-') + date_start.split(' ')[1].split(':')]).timetuple())
    end_timestamp = time.mktime(datetime.datetime(*[int(i) for i in date_end.split(' ')[0].split('-') + date_end.split(' ')[1].split(':')]).timetuple())
    now_timestamp = time.mktime(datetime.datetime.now().timetuple())
    percent = 100
    if end_timestamp > now_timestamp:
        percent = int((now_timestamp - start_timestamp) * 100 / (end_timestamp - start_timestamp))
    if percent_flag == 1:
        return percent
    else:
        if percent <= 33:
            return "success"
        elif percent <= 66:
            return "warning"
        else:
            return "danger"

@register.inclusion_tag('tags/mood_select.html')
def mood_list(mood_id=0):
    return { 'mood_list': Mood.objects.all(), 'mood_id': mood_id }

@register.inclusion_tag('tags/post_short_comments.html')
def post_short_comments(post, short_comments, min_opacity=20):
    post_short_comments = PostShortComments.objects.filter(post=post)
    max_count = 0
    for p in post_short_comments:
        if p.count > max_count:
            max_count = p.count
    for s_c in short_comments:
        s_c.opacity = round(float(min_opacity) / 100.0, 2)
    for s_c in short_comments:
        for p_s in post_short_comments:
            if p_s.short_comment.id == s_c.id and p_s.count > 0:
                s_c.opacity = round(float((100 - min_opacity) * p_s.count / max_count + min_opacity) / 100.0, 2)

    return {'post_short_comments': post_short_comments, 'short_comments': short_comments, 'post': post}