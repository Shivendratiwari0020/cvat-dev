
# Copyright (C) 2018-2021 Intel Corporation
#
# SPDX-License-Identifier: MIT

from django.urls import path, include
from . import views
from . import additional_views
from rest_framework import routers

from django.views.generic import RedirectView
from django.conf import settings
from cvat.apps.restrictions.views import RestrictionsViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter(trailing_slash=False)
router.register('projects', views.ProjectViewSet)
router.register('tasks', views.TaskViewSet)
router.register('jobs', views.JobViewSet)
router.register('users', views.UserViewSet)
router.register('server', views.ServerViewSet, basename='server')
router.register('issues', views.IssueViewSet)
router.register('comments', views.CommentViewSet)
router.register('restrictions', RestrictionsViewSet, basename='restrictions')
router.register('cloudstorages', views.CloudStorageViewSet)
router.register('cat',views.CatlogViewSet)
router.register('project-additional-info',additional_views.ProjectExtraViewSet)
router.register('project-type-info',additional_views.GetProjectMode)
router.register('save-tracked-bulk-update',additional_views.BulkUpdate,basename='tasksjobs')

# router.register('save-tracked-bulk-update',additional_views.BulkUpdate,basename='tasksjobs')
# router.register('project-additional-info',additional_views.ProjectExtraViewSet)
router.register('get-tracked-frame-info',additional_views.GetCroppedImages,basename='tasksjobsframes')
router.register('save-label-corrector-attribute',additional_views.LabelCorrectorAttrSave ,basename='tasksjobsframessummary')
router.register('save-sr-invisible-frame-info',additional_views.SaveSRVisibleData,basename='taskssrinvisbleframes')
router.register('get-tracked-frame-summary',additional_views.JobTrackSummary,basename='tasksjobsframessummary')
router.register('get-track-ids',additional_views.GetTrackIds ,basename='trackids')
# router.register('im',views.CatViewSet)

urlpatterns = [
    # Entry point for a client
    path('', RedirectView.as_view(url=settings.UI_URL, permanent=True,
         query_string=True)),

    # documentation for API
    path('api/schema/', SpectacularAPIView.as_view(api_version='2.0'), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # entry point for API
    path('api/', include('cvat.apps.iam.urls')),
    path('api/', include('cvat.apps.organizations.urls')),
    path('api/', include(router.urls)),
    # path('api/viewcatlog',views.viewcatlog),
    # path('api/cat/',views.CatlogAPIView.as_view() ),
    # path('api/projects/data/',views.data)
]
