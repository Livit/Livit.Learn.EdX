from django.conf.urls import patterns, url, include

# from rest_framework.urlpatterns import format_suffix_patterns

from labster.api.views import APIRoot
from labster.api.views import CreateSave, CreateError, CreateDevice
from labster.api.views import LabProxyView, AnswerProblem, Wiki, ArticleSlug
from labster.api.views import UserAuth, PlayLab, FinishLab, LabSettings
from labster.api.views import UnityPlayLab, CreateLog, CreateUnityLog
from labster.api.views import ArticleLinks, SendGraphData

from labster_search.api_views import Search


urlpatterns = patterns('',  # nopep8

    url('^$', APIRoot.as_view(), name='root'),

    url('^collect-response/(?P<action>\w+)/$', 'labster.api.views.collect_response'),

    url('auth/$', UserAuth.as_view(), name='auth'),
    url('^users/', include('labster.api.users.urls')),

    url('^labs/(?P<lab_id>\d+)/questions/$', LabProxyView.as_view(), name='questions'),
    url('^labs/(?P<lab_id>\d+)/answer/$', AnswerProblem.as_view(), name='answer'),
    url('^labs/(?P<lab_id>\d+)/save/$', CreateSave.as_view(), name='save'),
    url('^labs/(?P<lab_id>\d+)/play/$', UnityPlayLab.as_view(), name='play'),
    url('^labs/(?P<lab_id>\d+)/log/(?P<log_type>\w+)/$', CreateLog.as_view(), name='create-log'),
    url('^labs/(?P<lab_id>\d+)/log-unity/$', CreateUnityLog.as_view(), name='create-unity-log'),

    # since article can have children it might conflict with course-wiki, so I add keyword article in the end
    url('^wiki/article/(?P<article_slug>.+/|)$', ArticleSlug.as_view(), name='wiki-article'),
    url('^wiki/article-links/(?P<article_slug>.+)/$', ArticleLinks.as_view(), name='wiki-article-links'),
    url('^wiki/(?P<course_id>[^/]+/[^/]+/[^/]+)/?$', Wiki.as_view(), name='wiki'),

    url('^search/$', Search.as_view(), name='search'),

    url('^send_graph_data/$', SendGraphData.as_view(), name='graph_data'),

    # unused
    url('^labs/(?P<lab_id>\d+)/log/error/$', CreateError.as_view(), name='log-error'),
    url('^labs/(?P<lab_id>\d+)/log/device/$', CreateDevice.as_view(), name='log-device'),
    url('^labs/(?P<lab_id>\d+)/settings/$', LabSettings.as_view(), name='lab-proxy-settings'),
    url('^labs/(?P<lab_id>\d+)/play-lab/$', PlayLab.as_view(), name='play-lab'),
    url('^labs/(?P<lab_id>\d+)/finish-lab/$', FinishLab.as_view(), name='finish-lab'),
)


# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['xml', 'json', 'html'])