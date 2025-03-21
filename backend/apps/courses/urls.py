from django.urls import path, include
from courses.views import (
    CourseCreateView,
    CourseRetrieveView,
    CourseUpdateView,
    CourseDeleteView,
    CourseListView
)

app_name = 'courses'

v1_urlpatterns = [
    path('', CourseListView.as_view(), name='list_courses'),
    path('create/', CourseCreateView.as_view(), name='create_course'),
    path(
        '<str:course_token>/',
        CourseRetrieveView.as_view(),
        name='retrieve_course'
    ),
    path(
        '<str:course_token>/update/',
        CourseUpdateView.as_view(),
        name='update_course'
    ),
    path(
        '<str:course_token>/delete/',
        CourseDeleteView.as_view(),
        name='delete_course'
    ),
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
