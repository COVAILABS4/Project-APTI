from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .decorators import validate_session


# Create your views here.
def login(request):
    """Render the main template."""
    return render(request, "login.html")


# ADMIN1


def admin_register(request, role):

    return render(request, "admin/register.html")


@validate_session
def admin_setting(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "admin/nav-bar/setting.html", context)


@validate_session
def admin(request, user_id, role):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
    }
    return render(request, "admin/home.html", context)


@validate_session
def new_content(request, user_id, role):

    context = {"user_id": user_id}
    return render(request, "admin/add-content/new-content/new_content.html", context)


@validate_session
def new_subtopic(request, user_id, topic_id, role):

    context = {"user_id": user_id, "topic_id": topic_id}
    return render(request, "admin/add-content/new-content/new_subtopic.html", context)


@validate_session
def edit_subtopic(request, user_id, topic_id, role):

    context = {"user_id": user_id, "topic_id": topic_id}
    return render(request, "admin/add-content/edit-content/edit_subtopic.html", context)


@validate_session
def new_title(request, user_id, topic_id, subtopic_id, role):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "admin/add-content/new-content/new_title.html", context)


@validate_session
def edit_title(request, user_id, topic_id, subtopic_id, role):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "admin/add-content/edit-content/edit_title.html", context)


@validate_session
def new_questions(request, user_id, topic_id, subtopic_id, type, title_id, role):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "type": type,
        "title_id": title_id,
    }
    return render(request, "admin/add-content/new-content/new_questions.html", context)


@validate_session
def edit_questions(request, user_id, topic_id, subtopic_id, type, title_id, role):

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
def new_questions_import(request, user_id, topic_id, subtopic_id, type, title_id, role):

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
def edit_content(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "admin/add-content/edit-content/edit_content.html", context)


@validate_session
def new_subadmin(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "admin/admin-actions/new_subadmin.html", context)


@validate_session
def edit_subadmin(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "admin/admin-actions/edit_subadmin.html", context)


@validate_session
def allocate_subadmin(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "admin/course-allocation/allocate_subadmin.html", context)


@validate_session
def allocate_user(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "admin/course-allocation/allocate_user.html", context)


# SUBADMIN2


@validate_session
def sub_admin(request, user_id, role):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
    }
    return render(request, "subadmin/home.html", context)


@validate_session
def sub_admin_setting(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "subadmin/nav-bar/setting.html", context)


@validate_session
def sub_new_content(request, user_id, role):

    context = {"user_id": user_id}
    return render(request, "subadmin/add-content/new-content/new_content.html", context)


@validate_session
def sub_new_subtopic(request, user_id, topic_id, role):

    context = {"user_id": user_id, "topic_id": topic_id}
    return render(
        request, "subadmin/add-content/new-content/new_subtopic.html", context
    )


@validate_session
def sub_edit_subtopic(request, user_id, topic_id, role):

    context = {"user_id": user_id, "topic_id": topic_id}
    return render(
        request, "subadmin/add-content/edit-content/edit_subtopic.html", context
    )


@validate_session
def sub_new_title(request, user_id, topic_id, subtopic_id, role):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "subadmin/add-content/new-content/new_title.html", context)


@validate_session
def sub_edit_title(request, user_id, topic_id, subtopic_id, role):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "subadmin/add-content/edit-content/edit_title.html", context)


@validate_session
def sub_new_questions(request, user_id, topic_id, subtopic_id, type, title_id, role):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "type": type,
        "title_id": title_id,
    }
    return render(
        request, "subadmin/add-content/new-content/new_questions.html", context
    )


@validate_session
def sub_edit_questions(request, user_id, topic_id, subtopic_id, type, title_id, role):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "type": type,
        "title_id": title_id,
    }
    return render(
        request, "subadmin/add-content/edit-content/edit_questions.html", context
    )


@validate_session
def sub_new_questions_import(
    request, user_id, topic_id, subtopic_id, type, title_id, role
):

    context = {
        "user_id": user_id,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "type": type,
        "title_id": title_id,
    }
    return render(
        request, "subadmin/add-content/new-content/new_questions_import.html", context
    )


@validate_session
def sub_edit_content(request, user_id, role):
    context = {"user_id": user_id}
    return render(
        request, "subadmin/add-content/edit-content/edit_content.html", context
    )


@validate_session
def sub_new_subadmin(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "subadmin/admin-actions/new_subadmin.html", context)


@validate_session
def sub_edit_subadmin(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "subadmin/admin-actions/edit_subadmin.html", context)


@validate_session
def sub_allocate_subadmin(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "subadmin/course-allocation/allocate_subadmin.html", context)


@validate_session
def sub_allocate_user(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "subadmin/course-allocation/allocate_user.html", context)


# USER3


def user_register(request, role):

    return render(request, "client/register.html")


@validate_session
def user_setting(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "client/nav-bar/setting.html", context)


@validate_session
def test_history(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "client/side-bar/test-history.html", context)


@validate_session
def contact_us(request, user_id, role):
    context = {"user_id": user_id}
    return render(request, "client/side-bar/contact-us.html", context)


@validate_session
def user(request, user_id, role):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
    }
    return render(request, "client/body-pages/home.html", context)


@validate_session
def sample(request, user_id, role):

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
def user_subtopic(request, user_id, role, topic_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {"user_id": user_id, "name": name, "role": role, "topic_id": topic_id}
    return render(request, "client/body-pages/subtopic.html", context)


@validate_session
def user_learning(request, user_id, role, topic_id, subtopic_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "client/body-pages/learning.html", context)


@validate_session
def user_test(request, user_id, role, topic_id, subtopic_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "client/body-pages/test-pages/test.html", context)


@validate_session
def user_practice(request, user_id, role, topic_id, subtopic_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
    }
    return render(request, "client/body-pages/practice-pages/practice.html", context)


@validate_session
def user_practice_take_test(request, user_id, role, topic_id, subtopic_id, title_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "title_id": title_id,
    }
    return render(request, "client/body-pages/practice-pages/take-test.html", context)


@validate_session
def user_test_take_test(request, user_id, role, topic_id, subtopic_id, title_id):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "title_id": title_id,
    }
    return render(request, "client/body-pages/test-pages/take-test.html", context)


@validate_session
def user_test_take_test_res(
    request, user_id, role, topic_id, subtopic_id, title_id, test_id
):

    print("LOGINSSS")
    user_id = request.session.get("user_id", "Unknown")
    name = request.session.get("name", "Guest")
    role = request.session.get("role", "Unknown")

    context = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "title_id": title_id,
        "test_id": test_id,
    }
    return render(request, "client/body-pages/test-pages/res.html", context)


@validate_session
def user_content(request, user_id, role):

    context = {"user_id": user_id}
    return render(request, "client/contents.html", context)


@validate_session
def user_questions(request, user_id, role):

    context = {"user_id": user_id}

    return render(request, "client/questions.html", context)


# View to display topic details
@validate_session
def topic_detail(request, topic_id, user_id, role):

    print(topic_id)

    return render(
        request, "client/topics.html", {"user_id": user_id, "topic_id": topic_id}
    )


@validate_session
def subtopic_details(request, topic_id, subtopic_id, type, user_id, role):
    print(topic_id, subtopic_id)

    try:

        return render(
            request,
            "client/subtopic_details.html",
            {
                "user_id": user_id,
                "topic_id": topic_id,
                "subtopic_id": subtopic_id,
                "type": type,
            },
        )
    except Exception as e:
        return render(request, "error.html", {"message": str(e)})


@validate_session
def question_details(request, topic_id, subtopic_id, type, title_id, user_id, role):
    # print(topic_id,subtopic_id)

    try:

        return render(
            request,
            "client/questions.html",
            {
                "user_id": user_id,
                "topic_id": topic_id,
                "subtopic_id": subtopic_id,
                "type": type,
                "title_id": title_id,
            },
        )
    except Exception as e:
        return render(request, "error.html", {"message": str(e)})


# UTILS
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
