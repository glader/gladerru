# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views.admin import *
from views.content import *
from views.redirects import *
from views.ugc import *
from feeds import *
from django.contrib.auth.views import password_reset
from django.views.generic.simple import redirect_to


urlpatterns = patterns('',
    url(r'^content/([^/]+)\.htm$', article, name='article'),
    url(r'^rubric/([^/]+)$', rubric, name='rubric'),
    url(r'^tags/(.+)$', tag, name='tags'),
    url(r'^tags', tags, name='tags_all'),
    url(r'^mountains/([^/]+)$', mountain, name='mountain'),
    url(r'^mountains$', mountains, name='mountains'),
    url(r'^terms/([^/]+)$', dictionary_word, name='dictionary_word'),
    url(r'^terms', dictionary, name='dictionary'),
    url(r'^skills/([^/]+)$', skill, name='skill'),
    url(r'^skills', skills, name='skills'),
    url(r'^tricks/([^/]+)$', trick, name='trick'),
    url(r'^tricks', tricks, name='tricks'),
    url(r'^studies/([^/]+)$', studio, name='studio'),
    url(r'^studies', studies, name='studies'),
    url(r'^movies/teasers', teasers, name='teasers'),
    url(r'^movies/soundtracks', soundtracks, name='soundtracks'),
    url(r'^movies/([^/]+)$', movie, name='movie'),
    url(r'^movies', movies, name='movies'),
    url(r'^people/([^/]+)/photos$', man_photos, name='man_photos'),
    url(r'^people/([^/]+)/author_photos$', man_author_photos, name='man_author_photos'),
    url(r'^people/([^/]+)$', man, name='man'),
    url(r'^people', people, name='people'),
    url(r'^regions/(\d+)$', region, name='region'),
    url(r'^search', search, name='search'),
    url(r'^feedback', feedback, name='feedback'),
    url(r'^discounts/(\d+)/edit', discount_edit, name='discount_edit'),
    url(r'^discounts/(\d+)/delete', discount_delete, name='discount_delete'),
    url(r'^discounts/new', discount_new, name='discount_new'),
    url(r'^discounts', discounts, name='discounts'),

    url(r'^auth/login$', login, name='login'),
    url(r'^auth/registration$', registration, name='registration'),
    url(r'^auth/logout$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^auth/reset$', password_reset,         name='password_reset'),
    url(r'^auth/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^auth/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^auth/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    url(r'^reports/memcache$', memcache_report, name='reports_memcache'),
    url(r'^reports/404', observe_404),
    url(r'^reports/timing', timing_report, name='reports_timing'),
    url(r'^reports$', reports, name='reports'),

    url(r'^messages/compose/$', messages_compose, name='messages_compose'),
    (r'^messages/', include('messages.urls')),

    #UGC
    url(r'^all$', all, name='all'),
    url(r'^top/comments$', top_discussed, name='top_discussed'),
    url(r'^top/best$', top_rating, name='top_rating'),
    url(r'^rating/users/best$', users_best, name='users_best'),
    url(r'^rating/users/new$', users_new, name='users_new'),
    url(r'^faq$', faq, name='faq'),
    url(r'^users/(?P<username>[\w\.-]+)/?$', user_profile, name='profile'),
    url(r'^users/(?P<username>[\w\.-]+)/friends?$', user_friends, name='user_friends'),
    url(r'^users/(?P<username>[\w\.-]+)/posts/?$', user_posts, name='user_posts'),
    url(r'^users/(?P<username>[\w\.-]+)/(?P<section>[\w]+)/?$', user_staff, name='user_staff'),
    url(r'^users/(?P<username>[\w\.-]+)/(?P<section>[\w]+)/(?P<item_id>[\d]+)/?$', user_item, name='user_item'),
    url(r'^schedule/(?P<year>\d+)/(?P<month>\d+)$', schedule, name='schedule_month'),
    url(r'^schedule', schedule, name='schedule'),

    url(r'^my$', my_profile, name='my_profile'),
    url(r'^my/friends$', my_friends, name='friends'),
    url(r'^my/news$', my_news, name='news'),
    url(r'^my/drafts$', drafts, name='drafts'),
    url(r'^my/settings$', my_settings, name='settings'),
    url(r'^my/commented$', commented, name='commented'),

    #Ajax
    url(r'^ajax/add_comment$', add_comment, name='add_comment'),
    url(r'^ajax/add_post_vote$', add_post_vote, name='add_post_vote'),
    url(r'^ajax/add_photo$', add_photo, name='add_photo'),
    url(r'^ajax/best_answer$', best_answer, name='best_answer'),
    url(r'^ajax/add_friend$', add_friend, name='add_friend'),
    url(r'^ajax/cancel_friend$', cancel_friend, name='cancel_friend'),
    url(r'^ajax/set_name$', set_name, name='set_name'),
    url(r'^ajax/set_news$', set_news, name='set_news'),
    url(r'^crossdomain.xml$', crossdomain, name='crossdomain'),
    url(r'^ajax/tags_suggest', tags_suggest),
    url(r'^ajax/add_vk_comment', vk_comment),
    url(r'^ajax/picturebox', picturebox),

    #Feeds
    (r'^feeds/best$', BestPosts()),
    (r'^feeds/all', AllPosts()),
    (r'^feeds/comments', NewComments()),
    (r'^feeds/tags/(?P<tag_name>.+)$', Tags()),

    #Editing
    url(r'^post/new$', new_post, name='new_post'),
    url(r'^post/edit/(\d+)$', edit_post, name='edit_post'),
    url(r'^photo/edit/(\d+)$', edit_photo, name='edit_photo'),
    url(r'^editprofile$', editprofile, name='editprofile'),
    url(r'^editpassword$', editpassword, name='editpassword'),
    url(r'^editavatar$', editavatar, name='editavatar'),
    url(r'^post/offer_movie$', offer_movie, name='offer_movie'),
    url(r'^post/offer_moviemaker$', offer_moviemaker, name='offer_moviemaker'),
    url(r'^post/offer_rider$', offer_rider, name='offer_rider'),

    url(r'^$', index, name='index'),

    #Create new elements
    url(r'^create/rider$', create_rider, name='create_rider'),
    url(r'^create/tag_replace$', tag_replace, name='tag_replace'),
    url(r'^create/teaser_announce$', create_teaser_announce, name='create_teaser_announce'),
    url(r'^create/fullmovie_announce$', create_fullmovie_announce, name='create_fullmovie_announce'),
    url(r'^create/tracklist_announce$', create_tracklist_announce, name='create_tracklist_announce'),

    url(r'^hidden$', hidden, name='hidden'),

    #DEBUG
    url(r'^change_user', change_user),

    #Old urls
    url(r'^my/posts$', old_my_posts),
    url(r'^posts/(\d+)$', old_user_post),
    url(r'^pic/(\d+)$', old_pic),
    url(r'^cat/([\w\d_-]+)$', old_post_category),
    url(r'^blog/[^/]+/(\d+)$', old_blog_post),
    url(r'^forum/profile', old_forum_profile),
    url(r'^forum', redirect_to, {'url': 'http://glader.ru/users/glader/posts/410'}, name='forum'),
    url(r'^index.pl-item=(?P<name>.+)\.htm$', redirect_to, {'url': '/content/%(name)s.htm'}),
    url(r'^studio/(?P<name>[^/]+)', redirect_to, {'url': '/studies/%(name)s'}),
    url(r'^best', old_best),
)
