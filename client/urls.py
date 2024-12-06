from django.urls import path
from . import views

urlpatterns = [
    # LOGIN
    path("", views.login, name="index"),
    # USER
    path("<str:role>/3/<str:user_id>/", views.user, name="user"),
    path("<str:role>/3/register", views.user_register, name="user-register"),
    path(
        "<str:role>/3/<str:user_id>/contents", views.user_content, name="user-content"
    ),
    path(
        "<str:role>/3/<str:user_id>/questions",
        views.user_questions,
        name="user-questions",
    ),
    path(
        "<str:role>/3/<str:user_id>/topic/<str:topic_id>/",
        views.topic_detail,
        name="topic_detail",
    ),
    path(
        "<str:role>/3/<str:user_id>/topic/<str:topic_id>/subtopic/<str:subtopic_id>/type/<str:type>",
        views.subtopic_details,
        name="subtopic_details",
    ),
    path(
        "<str:role>/3/<str:user_id>/topic/<str:topic_id>/subtopic/<str:subtopic_id>/type/<str:type>/title/<str:title_id>",
        views.question_details,
        name="questions",
    ),
    # ADMIN
    path("<str:role>/1/<str:user_id>/", views.admin, name="admin"),
    path("<str:role>/1/register", views.admin_register, name="admin-register"),
    path(
        "<str:role>/1/<str:user_id>/new/content", views.new_content, name="new-content"
    ),
    path(
        "<str:role>/1/<str:user_id>/new/content/<str:topic_id>/subtopics",
        views.new_subtopic,
        name="new_subtopic",
    ),
    path(
        "<str:role>/1/<str:user_id>/edit/content/<str:topic_id>/subtopics",
        views.edit_subtopic,
        name="new_subtopic",
    ),
    path(
        "<str:role>/1/<str:user_id>/new/content/<str:topic_id>/subtopics/<str:subtopic_id>",
        views.new_title,
        name="new_title",
    ),
    path(
        "<str:role>/1/<str:user_id>/edit/content/<str:topic_id>/subtopics/<str:subtopic_id>",
        views.edit_title,
        name="edit_title",
    ),
    path(
        "<str:role>/1/<str:user_id>/new/content/<str:topic_id>/subtopics/<str:subtopic_id>/<str:type>/<str:title_id>",
        views.new_questions,
        name="new_questions",
    ),
    path(
        "<str:role>/1/<str:user_id>/edit/content/<str:topic_id>/subtopics/<str:subtopic_id>/<str:type>/<str:title_id>",
        views.edit_questions,
        name="edit_questions",
    ),
    path(
        "<str:role>/1/<str:user_id>/new/content/<str:topic_id>/subtopics/<str:subtopic_id>/<str:type>/<str:title_id>/import",
        views.new_questions_import,
        name="new_questions_import",
    ),
    path(
        "<str:role>/1/<str:user_id>/edit/content",
        views.edit_content,
        name="edit-content",
    ),
    path(
        "<str:role>/1/<str:user_id>/new/subadmin",
        views.new_subadmin,
        name="new-subadmin",
    ),
    path(
        "<str:role>/1/<str:user_id>/edit/subadmin",
        views.edit_subadmin,
        name="edit-subadmin",
    ),
    path(
        "<str:role>/1/<str:user_id>/allocate/subadmin",
        views.allocate_subadmin,
        name="allocate_subadmin",
    ),
    path(
        "<str:role>/1/<str:user_id>/allocate/users",
        views.allocate_user,
        name="allocate_user",
    ),
    path(
        "<str:role>/1/<str:user_id>/setting",
        views.admin_setting,
        name="admadmin-settingin",
    ),
    # --------------------------------------------
    # SUBADMIN
    path("<str:role>/2/<str:user_id>/", views.sub_admin, name="subadmin"),
    path(
        "<str:role>/2/<str:user_id>/new/content",
        views.sub_new_content,
        name="new-content",
    ),
    path(
        "<str:role>/2/<str:user_id>/new/content/<str:topic_id>/subtopics",
        views.sub_new_subtopic,
        name="new_subtopic",
    ),
    path(
        "<str:role>/2/<str:user_id>/edit/content/<str:topic_id>/subtopics",
        views.sub_edit_subtopic,
        name="new_subtopic",
    ),
    path(
        "<str:role>/2/<str:user_id>/new/content/<str:topic_id>/subtopics/<str:subtopic_id>",
        views.sub_new_title,
        name="new_title",
    ),
    path(
        "<str:role>/2/<str:user_id>/edit/content/<str:topic_id>/subtopics/<str:subtopic_id>",
        views.sub_edit_title,
        name="edit_title",
    ),
    path(
        "<str:role>/2/<str:user_id>/new/content/<str:topic_id>/subtopics/<str:subtopic_id>/<str:type>/<str:title_id>",
        views.sub_new_questions,
        name="new_questions",
    ),
    path(
        "<str:role>/2/<str:user_id>/edit/content/<str:topic_id>/subtopics/<str:subtopic_id>/<str:type>/<str:title_id>",
        views.sub_edit_questions,
        name="edit_questions",
    ),
    path(
        "<str:role>/2/<str:user_id>/new/content/<str:topic_id>/subtopics/<str:subtopic_id>/<str:type>/<str:title_id>/import",
        views.sub_new_questions_import,
        name="new_questions_import",
    ),
    path(
        "<str:role>/2/<str:user_id>/edit/content",
        views.sub_edit_content,
        name="edit-content",
    ),
    path(
        "<str:role>/2/<str:user_id>/new/subadmin",
        views.sub_new_subadmin,
        name="new-subadmin",
    ),
    path(
        "<str:role>/2/<str:user_id>/edit/subadmin",
        views.sub_edit_subadmin,
        name="edit-subadmin",
    ),
    path(
        "<str:role>/2/<str:user_id>/allocate/subadmin",
        views.sub_allocate_subadmin,
        name="allocate_subadmin",
    ),
    path(
        "<str:role>/2/<str:user_id>/allocate/users",
        views.sub_allocate_user,
        name="allocate_user",
    ),
    path(
        "<str:role>/2/<str:user_id>/setting",
        views.sub_admin_setting,
        name="admadmin-settingin",
    ),
    # UTILS
    path("store-session/", views.store_session, name="store_session"),
    path("invalid/", views.invalid, name="invalid"),
]
