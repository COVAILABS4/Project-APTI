from django.shortcuts import redirect


def validate_session(view_func):
    def wrapper(request, *args, **kwargs):
        session_user_id = request.session.get("user_id")
        session_role = request.session.get("role")
        user_id = kwargs.get("user_id")
        role = kwargs.get("role")

        session_role = session_role + "s" if session_role == "admin" else session_role

        print(role, session_role)

        print(user_id, session_user_id)

        if session_user_id != user_id:
            print("INSIDE", user_id, session_user_id)
            return redirect(
                "invalid"
            )  # Redirect to the login page if user_id doesn't match
        if role != session_role:
            print("INSIDE", user_id, session_user_id)
            return redirect(
                "invalid"
            )  # Redirect to the login page if user_id doesn't match

        return view_func(request, *args, **kwargs)

    return wrapper
