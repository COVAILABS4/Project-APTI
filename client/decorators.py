from django.shortcuts import redirect


def validate_session(view_func):
    def wrapper(request, *args, **kwargs):
        session_user_id = request.session.get("user_id")
        user_id = kwargs.get("user_id")

        print(user_id, session_user_id)

        if int(session_user_id) != int(user_id):
            print("INSIDE", user_id, session_user_id)
            return redirect(
                "invalid"
            )  # Redirect to the login page if user_id doesn't match

        return view_func(request, *args, **kwargs)

    return wrapper
