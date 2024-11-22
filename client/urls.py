from django.urls import path
from . import views

urlpatterns = [
    # LOGIN
    path("", views.login, name="index"),
    # USER
    path("user/<str:user_id>/", views.user, name="user"),
    path("user/register", views.user_register, name="user-register"),
    path("user/<str:user_id>/contents", views.user_content, name="user-content"),
    path("user/<str:user_id>/questions", views.user_questions, name="user-questions"),
    path(
        "user/<str:user_id>/topic/<str:topic_id>/",
        views.topic_detail,
        name="topic_detail",
    ),
    path(
        "user/<str:user_id>/topic/<str:topic_id>/subtopic/<str:subtopic_id>/type/<str:type>",
        views.subtopic_details,
        name="subtopic_details",
    ),
    path(
        "user/<str:user_id>/topic/<str:topic_id>/subtopic/<str:subtopic_id>/type/<str:type>/title/<str:title_id>",
        views.question_details,
        name="questions",
    ),
    # ADMIN
    path("admins/<str:user_id>/", views.admin, name="admin"),
    path("admins/register", views.admin_register, name="admin-register"),
    path("admins/<str:user_id>/new/content", views.new_content, name="new-content"),
    path(
        "admins/<str:user_id>/new/content/<str:topic_id>/subtopics",
        views.new_subtopic,
        name="new_subtopic",
    ),
    path("admins/<str:user_id>/edit/content", views.edit_content, name="edit-content"),
    path("admins/<str:user_id>/new/subadmin", views.new_subadmin, name="new-subadmin"),
    path(
        "admins/<str:user_id>/view/subadmin", views.view_subadmin, name="view-subadmin"
    ),
    path(
        "admins/<str:user_id>/allocate/subadmin",
        views.allocate_subadmin,
        name="allocate_subadmin",
    ),
    path(
        "admins/<str:user_id>/allocate/users", views.allocate_user, name="allocate_user"
    ),
    path("admins/<str:user_id>/profile", views.admin_profile, name="admin-profile"),
    path(
        "admins/<str:user_id>/setting", views.admin_setting, name="admadmin-settingin"
    ),
    # SUBADMIN
    path("subadmin/<str:user_id>/", views.sub_admin, name="subadmin"),
    # UTILS
    path("store-session/", views.store_session, name="store_session"),
    path("invalid/", views.invalid, name="invalid"),
]
