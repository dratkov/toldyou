from django.db import models
import datetime
from told.forms import PostForm

class ShortComment(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Mood(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text


class Post(models.Model):
    text = models.CharField(max_length=280)
    date = models.DateTimeField(default=datetime.datetime.now)
    agree_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    disagree_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    event_date = models.DateTimeField(null=True, blank=True)
    visible = models.SmallIntegerField(blank=True, default=0)
    category = models.OneToOneField(Category, blank=True, null=True)
    mood = models.ForeignKey(Mood, blank=True, null=True)
    fulfilled = models.BooleanField(blank=True)
    not_fulfilled = models.BooleanField(blank=True)

    def get_user_short_comments(self):
        return PostShortCommentsUser.objects.filter(post=self)

    def set_fulfilled(self, fulfilled):
        if(fulfilled == "True"):
            self.not_fulfilled = False
            self.fulfilled = True
        else:
            self.fulfilled = False

    def set_not_fulfilled(self, not_fulfilled):
        if(not_fulfilled == "True"):
            self.fulfilled = False
            self.not_fulfilled = True
        else:
            self.not_fulfilled = False

    def set_visible(self, visible):
        try:
            visible = int(visible)
            if visible >= 0 and visible <= 2:
                self.visible = visible
        except ValueError: pass

    def set_category(self, category_id):
        try:
            category_id = int(category_id)
            try:
                category = Category.objects.get(id=category_id)
                self.category = category
            except Category.DoesNotExist: pass
        except ValueError: pass

    def set_mood(self, mood_id):
        try:
            mood_id = int(mood_id)
            try:
                mood = Mood.objects.get(id=mood_id)
                self.mood = mood
            except Mood.DoesNotExist: pass
        except ValueError: pass


    def edit(self, post):
        if post.has_key('fulfilled'):
            self.set_fulfilled(post['fulfilled'])
        if post.has_key('not_fulfilled'):
            self.set_not_fulfilled(post['not_fulfilled'])
        if post.has_key('mood_id'):
            try:
                mood_id = int(post['mood_id'])
            except ValueError:
                mood_id = 0
            try:
                mood = Mood.objects.get(id=mood_id)
                self.mood = mood
            except Mood.DoesNotExist:
                pass
        if 'category_id' in post:
            self.set_category(post['category_id'])
        if 'visible' in post:
            self.set_visible(post['visible'])

    def add(self, post):
        if 'text' in post and len(post['text']) > 0:
            self.text = post['text']
        if 'event_date' in post and len(post['event_date']) > 0:
            self.event_date = post['event_date']
        if 'category_id' in post:
            self.set_category(post['category_id'])
        if 'visible' in post:
            self.set_visible(post['visible'])
        if 'mood_id' in post:
            self.set_mood(post['mood_id'])

    def __unicode__(self):
        return self.text


class PostShortComments(models.Model):
    count = models.SmallIntegerField()
    post = models.ForeignKey(Post)
    short_comment = models.ForeignKey(ShortComment)


class PostShortCommentsUser(models.Model):
    text = models.CharField(max_length=50)
    post = models.ForeignKey(Post)

