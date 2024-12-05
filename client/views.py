from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .decorators import validate_session


# Create your views here.
def login(request):
    """Render the main template."""
    return render(request, "login.html")


# ADMIN


def admin_register(request):

    return render(request, "admin/register.html")


@validate_session
def admin_profile(request, user_id):
    context = {"user_id": user_id}
    return render(request, "admin/nav-bar/admin_profile.html", context)


@validate_session
def admin_setting(request, user_id):
    context = {"user_id": user_id}
    return render(request, "admin/nav-bar/admin_setting.html", context)


@validate_session
def admin(request, user_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
    }
    return render(request, "admin/admin.html", context)


@validate_session
def new_content(request, user_id):

    context = {"user_id": user_id}
    return render(request, "admin/add-content/new-content/new_content.html", context)


@validate_session
def new_subtopic(request, user_id, topic_id):

    context = {"user_id": user_id, "topic_id": topic_id}
    return render(request, "admin/add-content/new-content/new_subtopic.html", context)


@validate_session
def edit_subtopic(request, user_id, topic_id):

    context = {"user_id": user_id, "topic_id": topic_id}
    return render(request, "admin/add-content/edit-content/edit_subtopic.html", context)


@validate_session
def new_title(request, user_id, topic_id, subtopic_id):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "admin/add-content/new-content/new_title.html", context)


@validate_session
def edit_title(request, user_id, topic_id, subtopic_id):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "admin/add-content/edit-content/edit_title.html", context)


@validate_session
def new_questions(request, user_id, topic_id, subtopic_id, type, title_id):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "type": type,
        "title_id": title_id,
    }
    return render(request, "admin/add-content/new-content/new_questions.html", context)


@validate_session
def edit_questions(request, user_id, topic_id, subtopic_id, type, title_id):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "type": type,
        "title_id": title_id,
    }
    return render(
        request, "admin/add-content/edit-content/edit_questions.html", context
    )


@validate_session
def new_questions_import(request, user_id, topic_id, subtopic_id, type, title_id):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "type": type,
        "title_id": title_id,
    }
    return render(
        request, "admin/add-content/new-content/new_questions_import.html", context
    )


@validate_session
def edit_content(request, user_id):
    return render(request, "admin/add-content/edit-content/edit_content.html")


@validate_session
def new_subadmin(request, user_id):
    return render(request, "admin/admin-actions/new_subadmin.html")


@validate_session
def edit_subadmin(request, user_id):
    return render(request, "admin/admin-actions/edit_subadmin.html")


@validate_session
def allocate_subadmin(request, user_id):
    return render(request, "admin/course-allocation/allocate_subadmin.html")


@validate_session
def allocate_user(request, user_id):
    return render(request, "admin/course-allocation/allocate_user.html")


# SUBADMIN


@validate_session
def sub_admin(request, user_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
    }
    return render(request, "admin/subadmin.html", context)


# USER


def user_register(request):

    return render(request, "client/register.html")


@validate_session
def user(request, user_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
    }
    return render(request, "client/user.html", context)


@validate_session
def user_content(request, user_id):

    return render(request, "client/contents.html")


@validate_session
def user_questions(request, user_id):

    return render(request, "client/questions.html")


# View to display topic details
@validate_session
def topic_detail(request, topic_id, user_id):

    print(topic_id)

    return render(request, "client/topics.html", {"topic_id": topic_id})


@validate_session
def subtopic_details(request, topic_id, subtopic_id, type, user_id):
    print(topic_id, subtopic_id)

    try:

        return render(
            request,
            "client/subtopic_details.html",
            {
                "topic_id": topic_id,
                "subtopic_id": subtopic_id,
                "type": type,
            },
        )
    except Exception as e:
        return render(request, "error.html", {"message": str(e)})


@validate_session
def question_details(request, topic_id, subtopic_id, type, title_id, user_id):
    # print(topic_id,subtopic_id)

    try:

        return render(
            request,
            "client/questions.html",
            {
                "topic_id": topic_id,
                "subtopic_id": subtopic_id,
                "type": type,
                "title_id": title_id,
            },
        )
    except Exception as e:
        return render(request, "error.html", {"message": str(e)})


@csrf_exempt
def store_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request.session["user_id"] = data["user_id"]
            request.session["name"] = data["name"]
            request.session["role"] = data["role"]
            return JsonResponse({"message": "Session data stored successfully"})
        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=400)

    return JsonResponse({"message": "Invalid request"}, status=400)


def invalid(request):

    return render(request, "support/invalid.html")
