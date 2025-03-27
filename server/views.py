from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse
from .models import (
    User,
    Topic,
    SubTopic,
    LearningMaterial,
    Practice,
    Test,
    PracticeQuestion,
    PracticeOption,
    TestQuestion,
    TestOption,
    UserTopic,
    TestHistory,
    Report,
)
import uuid
import json
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from django.shortcuts import get_object_or_404

import pandas as pd

import random


from .email_smtp_utils import queue_email


from io import BytesIO


def get_unique_id():

    return str(uuid.uuid4())


def get_user_name(id):
    print("_+_+_+_+", id)

    try:
        user = User.objects.get(user_id=id)
        return user.name  # Return only the user's name, or any other field you need
    except User.DoesNotExist:
        return None  # or you can return a default value, e.g., "Unknown"


# USER's


# def admin_register(request):
#     if request.method == "POST":
#         try:
#             data = request.POST.dict()
#             name = data.get("name")
#             phone_number = data.get("phone_number")
#             email = data.get("email")
#             password = data.get("password")
#             dob = data.get("dob", "")
#             city = data.get("city", "")
#             state = data.get("state", "")
#             country = data.get("country", "")
#             role = data.get("role", "user")
#             image = request.FILES.get("image")

#             if User.objects.filter(email=email).exists():
#                 return JsonResponse(
#                     {"error": "User with this email already exists"}, status=409
#                 )

#             user_id = get_unique_id()
#             photo_url = "media/images/krishtec.jpg"

#             if image:
#                 image_name = f"media/images/{user_id}.jpg"
#                 default_storage.save(image_name, ContentFile(image.read()))
#                 photo_url = image_name

#             user = User.objects.create(
#                 user_id=user_id,
#                 name=name,
#                 phone_number=phone_number,
#                 email=email,
#                 password=password,
#                 dob=dob,
#                 city=city,
#                 state=state,
#                 country=country,
#                 role=role,
#                 photo_url=photo_url,
#             )
#             user.save()

#             return JsonResponse(
#                 {"message": f"Registration successful, redirecting to {role} page."},
#                 status=201,
#             )

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#         except Exception as e:
#             return JsonResponse(
#                 {"error": f"Internal server error: {str(e)}"}, status=500
#             )

#     return JsonResponse({"error": "Invalid request method"}, status=405)


def admin_register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            phone_number = data.get("phone_number")
            email = data.get("email")
            password = data.get("password")
            dob = data.get("dob", "DD/MM/YYYY")
            city = data.get("city", "CITY")
            role = data.get("role", "subadmin")
            state = data.get("state", "STATE")
            country = data.get("country", "CN")
            user_type = data.get("type", "user")  # Get type, default is user

            with transaction.atomic():
                if User.objects.filter(email=email).exists():
                    return JsonResponse(
                        {"error": "User with this email already exists"}, status=409
                    )

                user = User(
                    user_id=get_unique_id(),
                    name=name,
                    phone_number=phone_number,
                    role=role,
                    email=email,
                    password=password,
                    dob=dob,
                    city=city,
                    state=state,
                    country=country,
                    photo_url="images/krishtec.jpg",
                    type=user_type,  # Assigning the new field
                )
                user.save()

            return JsonResponse(
                {
                    "message": "Registration successful, redirecting to user page.",
                    "role": "user",
                },
                status=201,
            )

        except IntegrityError as err:
            return JsonResponse(
                {"error": "Database error. Please try again."}, status=500
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Internal server error: {str(e)}"}, status=500
            )
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def login(request):
    if request.method == "POST":
        try:

            print("Called")
            # Parse the incoming request body
            body = json.loads(request.body)
            email = body.get("email")
            password = body.get("password")

            print(email, password)

            # Check if email and password are provided
            if not email or not password:
                return JsonResponse(
                    {"error": "Email and password are required"}, status=400
                )

            # Query the database for the user
            try:
                user = User.objects.get(email=email, password=password)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

            # Respond with user details
            return JsonResponse(
                {
                    "message": "Login successful",
                    "user_id": user.user_id,
                    "name": user.name,
                    "role": user.role,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": f"Internal server error: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            phone_number = data.get("phone_number")
            email = data.get("email")
            password = data.get("password")
            dob = data.get("dob")
            city = data.get("city")
            state = data.get("state")
            country = data.get("country")
            user_type = data.get("type", "user")  # Get type, default is user

            if not all(
                [name, phone_number, email, password, dob, city, state, country]
            ):
                return JsonResponse({"error": "All fields are required"}, status=400)

            with transaction.atomic():
                if User.objects.filter(email=email).exists():
                    return JsonResponse(
                        {"error": "User with this email already exists"}, status=409
                    )

                user = User(
                    user_id=get_unique_id(),
                    name=name,
                    phone_number=phone_number,
                    role="user",
                    email=email,
                    password=password,
                    dob=dob,
                    city=city,
                    state=state,
                    country=country,
                    photo_url="images/krishtec.jpg",
                    type=user_type,  # Assigning the new field
                )
                user.save()

            return JsonResponse(
                {
                    "message": "Registration successful, redirecting to user page.",
                    "role": "user",
                },
                status=201,
            )

        except IntegrityError:
            return JsonResponse(
                {"error": "Database error. Please try again."}, status=500
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Internal server error: {str(e)}"}, status=500
            )
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


# Get all user
def get_all_users(request):
    try:
        users = User.objects.filter(role="user")
        user_data = [
            {
                "user_id": user.user_id,
                "name": user.name,
                "phone_number": user.phone_number,
                "email": user.email,
                "dob": user.dob,
                "city": user.city,
                "state": user.state,
                "country": user.country,
                "role": user.role,
            }
            for user in users
        ]
        return JsonResponse({"users": user_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


from django.conf import settings


def update_user(request, user_id):
    if request.method == "POST":
        try:
            user = get_object_or_404(User, user_id=user_id)

            # Handle image upload if present
            if "profilePhoto" in request.FILES:
                profile_image = request.FILES["profilePhoto"]

                # Delete the existing image if it exists
                if user.photo_url:
                    old_image_path = os.path.join(
                        settings.MEDIA_ROOT, user.photo_url.name
                    )

                    print("Old Image Path: ", old_image_path)
                    if os.path.exists(old_image_path):
                        print("True")
                        if "krishtec.jpg" not in old_image_path:
                            os.remove(old_image_path)

                # Save the new image with the same filename
                fs = FileSystemStorage(location="media/images")
                filename = f"{user_id}.jpg"
                file_path = fs.save(filename, profile_image)

                print("Saved file path: ", file_path)

                # Update the user's photo_url to point to the saved image
                user.photo_url = f"images/{filename}"

            # Update other fields
            user.name = request.POST.get("name", user.name)
            user.email = request.POST.get("email", user.email)
            user.dob = request.POST.get("dob", user.dob)
            user.city = request.POST.get("city", user.city)
            user.state = request.POST.get("state", user.state)
            user.country = request.POST.get("country", user.country)
            user.phone_number = request.POST.get("phone_number", user.phone_number)

            user.save()

            return JsonResponse({"message": "User updated successfully."}, status=200)
        except Exception as e:
            return JsonResponse(
                {"error": f"Internal server error: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_user(request, user_id):
    print("sausgduasydguyagdyuagyud")
    try:
        user = get_object_or_404(User, user_id=user_id)
        print("-------------------------", user)
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "phone_number": user.phone_number,
            "email": user.email,
            "dob": user.dob,
            "city": user.city,
            "state": user.state,
            "country": user.country,
            "photo_url": user.photo_url.name,
        }
        return JsonResponse(user_data, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


def dashboard_stats(request):
    if request.method == "GET":
        try:
            # Fetch all users and topics from the database
            users = User.objects.all()
            topics = Topic.objects.all()
            test_history_len = TestHistory.objects.all().count()

            if users is None or topics is None:
                return JsonResponse(
                    {"error": "Error reading data from the database."}, status=500
                )

            # Calculate statistics
            total_users = users.filter(
                role="user"
            ).count()  # Count users with 'user' role
            total_subadmins = users.filter(
                role="subadmin"
            ).count()  # Count users with 'subadmin' role
            total_courses = topics.count()  # Total number of topics
            # Count total tests attempted by all users
            active_users = (
                10  # users.filter(is_active=True).count()  # Count active users
            )

            # Respond with statistics
            return JsonResponse(
                {
                    "totalUsers": total_users,
                    "totalSubAdmins": total_subadmins,
                    "totalCourses": total_courses,
                    "totalTestsAttempted": test_history_len,
                    "activeUsers": active_users,
                }
            )

        except Exception as e:
            print(f"Error processing data: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_subadmins(request):
    if request.method == "GET":
        try:
            # Fetch all users with the role "subadmin"
            subadmins = User.objects.filter(role="subadmin")

            # Prepare a list of subadmins with relevant details
            subadmins_list = list(subadmins.values())

            print(subadmins)

            return JsonResponse(subadmins_list, safe=False, status=200)
        except Exception as e:
            print(f"Error in /get-subadmins: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def edit_subadmin(request, id):
    if request.method == "PUT":
        try:
            # Parse the incoming request body
            body = json.loads(request.body)
            name = body.get("name", None)
            phone_number = body.get("phone_number", None)
            email = body.get("email", None)
            password = body.get("password", None)
            dob = body.get("dob", None)
            city = body.get("city", None)
            type = body.get("type", None)
            state = body.get("state", None)
            country = body.get("country", None)

            # Fetch the Subadmin to update
            try:
                subadmin = User.objects.get(user_id=id, role="subadmin")
            except User.DoesNotExist:
                return JsonResponse({"error": "Subadmin not found"}, status=404)

            # Update Subadmin's details
            subadmin.name = name or subadmin.name
            subadmin.phone_number = phone_number or subadmin.phone_number
            subadmin.email = email or subadmin.email
            subadmin.type = type or subadmin.type
            subadmin.password = password or subadmin.password
            subadmin.dob = dob or subadmin.dob
            subadmin.city = city or subadmin.city
            subadmin.state = state or subadmin.state
            subadmin.country = country or subadmin.country

            # Save the updated details
            subadmin.save()
            return JsonResponse(
                {"message": "Subadmin updated successfully"}, status=200
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": f"Internal server error: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


def delete_subadmin(request, id):
    if request.method == "DELETE":
        try:
            # Fetch the Subadmin to delete
            try:
                subadmin = User.objects.get(user_id=id, role="subadmin")
            except User.DoesNotExist:
                return JsonResponse({"error": "Subadmin not found"}, status=404)

            # Delete the Subadmin
            subadmin.delete()
            return JsonResponse(
                {"message": "Subadmin deleted successfully"}, status=200
            )

        except Exception as e:
            return JsonResponse(
                {"error": f"Internal server error: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


def add_topic(request):
    if request.method == "POST":
        try:
            body = get_body_data(request)
            user_id = body.get("user_id")
            topic_name = body.get("topic_name")
            domain_type = body.get("domain_type", "tech")
            tech_type = body.get("tech_type", "sw")

            if not user_id or not topic_name:
                return JsonResponse(
                    {"error": "User ID and Topic Name are required"}, status=400
                )

            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            topic_id = get_unique_id()
            formatted_time = datetime.now().strftime("%d/%m/%Y , %H:%M:%S")

            new_topic = Topic.objects.create(
                topic_id=topic_id,
                name=topic_name,
                created_by=user,
                created_at=formatted_time,
                domain_type=domain_type,
                tech_type=tech_type,
            )

            response_data = {
                "topic_id": new_topic.topic_id,
                "name": new_topic.name,
                "created_by": new_topic.created_by.name,
                "created_at": new_topic.created_at,
                "domain_type": new_topic.domain_type,
                "tech_type": new_topic.tech_type,
                "sub_topics": [],
            }

            return JsonResponse(response_data, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_topics(request):
    if request.method == "GET":
        try:
            topics = Topic.objects.all()
            topic_list = [
                {
                    "topic_id": topic.topic_id,
                    "name": topic.name,
                    "created_by": topic.created_by.name,
                    "created_at": topic.created_at,
                    "domain_type": topic.domain_type,
                    "tech_type": topic.tech_type,
                }
                for topic in topics
            ]
            return JsonResponse(topic_list, safe=False, status=200)

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def organize_topic(request, id):
    if request.method == "GET":
        try:
            topic = get_object_or_404(Topic, topic_id=id)

            topic_data = {
                "topic_id": topic.topic_id,
                "name": topic.name,
                "created_by": topic.created_by.name,
                "created_at": topic.created_at,
                "domain_type": topic.domain_type,
                "tech_type": topic.tech_type,
            }

            return JsonResponse(topic_data, status=200)

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

    if request.method == "PUT":
        try:
            topic = get_object_or_404(Topic, topic_id=id)
            body = json.loads(request.body)

            new_name = body.get("name", topic.name)
            domain_type = body.get("domain_type", topic.domain_type)
            tech_type = body.get("tech_type", topic.tech_type)

            topic.name = new_name
            topic.domain_type = domain_type
            topic.tech_type = tech_type
            topic.save()

            return JsonResponse(
                {
                    "message": "Topic updated successfully",
                    "topic": {
                        "topic_id": topic.topic_id,
                        "name": topic.name,
                        "created_by": topic.created_by_id,
                        "created_at": topic.created_at,
                        "domain_type": topic.domain_type,
                        "tech_type": topic.tech_type,
                    },
                },
                status=200,
            )

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

    if request.method == "DELETE":
        try:
            topic = get_object_or_404(Topic, topic_id=id)
            topic.delete()
            return JsonResponse({"message": "Topic deleted successfully"}, status=200)

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_body_data(request):

    return json.loads(request.body)


def add_subtopic(request, topic_id):
    if request.method == "POST":
        try:

            body = get_body_data(request)
            # Retrieve the user ID and subtopic name from the request body
            user_id = body.get("user_id")
            subtopic_name = body.get("subtopic_name")

            print(user_id, subtopic_name, topic_id, "---------------------------")

            if not user_id or not subtopic_name:
                return JsonResponse(
                    {"error": "User ID and Subtopic name are required"}, status=400
                )

            # Fetch the topic from the database using topic_id
            topic = Topic.objects.filter(topic_id=topic_id).first()

            if not topic:
                return JsonResponse({"error": "Topic not found"}, status=404)

            # Retrieve the user who created the subtopic
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            # Generate unique subtopic ID
            subtopic_id = get_unique_id()

            # Get current date and time
            current_time = datetime.now()

            # Format the date and time as "DD/MM/YYYY , HH/MM/SS"
            formatted_time = str(current_time.strftime("%d/%m/%Y , %H:%M:%S"))

            # Print the formatted time
            print(formatted_time)

            # Create a new SubTopic entry in the database
            new_subtopic = SubTopic.objects.create(
                subtopic_id=subtopic_id,
                name=subtopic_name,
                topic_id_id=topic.topic_id,
                created_by_id=user_id,
                created_at=formatted_time,
            )

            # Respond with the new subtopic details
            response_data = {
                "subtopic_id": new_subtopic.subtopic_id,
                "name": new_subtopic.name,
                "created_by": new_subtopic.created_by.name,
                "created_at": new_subtopic.created_at,
            }

            return JsonResponse(response_data, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def add_title(request, topic_id, subtopic_id):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            content_type = body.get("type")  # "Practices" or "Test"
            title = body.get("title")
            duration = body.get("duration", 900)  # Default 0 seconds
            attempts = body.get("attempts", 1)  # Default 1 attempt

            if not title:
                return JsonResponse({"error": "Title is required"}, status=400)

            title_id = get_unique_id()  # Generate unique ID

            if content_type == "Practices":
                practice = Practice.objects.create(
                    title_id=title_id,
                    topic_id_id=topic_id,
                    subtopic_id_id=subtopic_id,
                    title=title,
                    duration=duration,
                    attempts=attempts,
                )
                response_data = {
                    "title_id": practice.title_id,
                    "title": practice.title,
                    "subtopic_id": practice.subtopic_id.subtopic_id,
                    "topic_id": practice.topic_id.topic_id,
                    "duration": practice.duration,
                    "attempts": practice.attempts,
                }

            elif content_type == "Test":
                test = Test.objects.create(
                    title_id=title_id,
                    topic_id_id=topic_id,
                    subtopic_id_id=subtopic_id,
                    title=title,
                    duration=duration,
                    attempts=attempts,
                )
                response_data = {
                    "title_id": test.title_id,
                    "title": test.title,
                    "subtopic_id": test.subtopic_id.subtopic_id,
                    "topic_id": test.topic_id.topic_id,
                    "duration": test.duration,
                    "attempts": test.attempts,
                }

            else:
                return JsonResponse({"error": "Invalid type specified"}, status=400)

            return JsonResponse(response_data, status=200)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


import os
import uuid
import json
from django.http import JsonResponse
from django.conf import settings
from .models import (
    Practice,
    PracticeQuestion,
    PracticeOption,
    Test,
    TestQuestion,
    TestOption,
)


def add_question(request):
    if request.method == "POST":
        try:
            form_data = request.POST
            files = request.FILES

            topic_id = form_data.get("topic_id")
            subtopic_id = form_data.get("subtopic_id")
            title_id = form_data.get("title_id")
            question = form_data.get("question")
            options = json.loads(form_data.get("options"))
            correct_option = int(form_data.get("correct_option"))
            explanation = form_data.get("explanation")
            type = form_data.get("type")

            if (
                not topic_id
                or not subtopic_id
                or not title_id
                or not question
                or not options
                or correct_option is None
            ):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if type == "Practices":
                try:
                    practice = Practice.objects.get(title_id=title_id)
                except Practice.DoesNotExist:
                    return JsonResponse({"error": "Practice not found"}, status=404)

                question_id = str(uuid.uuid4())
                practice_question = PracticeQuestion.objects.create(
                    question_id=question_id,
                    title_id=practice,
                    question=question,
                    correct_option=correct_option,
                    explanation=explanation,
                )

                if files.get("questionImage"):
                    question_image = files["questionImage"]
                    question_image_name = f"question_id_{question_id}_ques.jpg"
                    question_image_path = os.path.join(
                        settings.MEDIA_ROOT, "ques_images", question_image_name
                    )
                    with open(question_image_path, "wb+") as destination:
                        for chunk in question_image.chunks():
                            destination.write(chunk)
                    practice_question.question_img = os.path.join(
                        "media", "ques_images", question_image_name
                    )
                    practice_question.save()

                practice_option = PracticeOption.objects.create(
                    option_id=str(uuid.uuid4()),
                    question_id=practice_question,
                    option1=options[0],
                    option2=options[1],
                    option3=options[2],
                    option4=options[3],
                )

                for i in range(1, 5):
                    option_image = files.get(f"option{i}Image")
                    if option_image:
                        option_image_name = f"question_id_{question_id}_opt{i}.jpg"
                        option_image_path = os.path.join(
                            settings.MEDIA_ROOT, "ques_images", option_image_name
                        )
                        with open(option_image_path, "wb+") as destination:
                            for chunk in option_image.chunks():
                                destination.write(chunk)
                        setattr(
                            practice_option,
                            f"option{i}_img",
                            os.path.join("media", "ques_images", option_image_name),
                        )
                practice_option.save()

                if files.get("explanationImage"):
                    explanation_image = files["explanationImage"]
                    explanation_image_name = f"question_id_{question_id}_exp.jpg"
                    explanation_image_path = os.path.join(
                        settings.MEDIA_ROOT, "ques_images", explanation_image_name
                    )
                    with open(explanation_image_path, "wb+") as destination:
                        for chunk in explanation_image.chunks():
                            destination.write(chunk)
                    practice_question.explanation_img = os.path.join(
                        "media", "ques_images", explanation_image_name
                    )
                    practice_question.save()

                response_data = {
                    "message": "Question added successfully",
                    "question_id": practice_question.question_id,
                    "question": practice_question.question,
                    "options": options,
                }

            elif type == "Test":
                try:
                    test = Test.objects.get(title_id=title_id)
                except Test.DoesNotExist:
                    return JsonResponse({"error": "Test not found"}, status=404)

                question_id = str(uuid.uuid4())
                test_question = TestQuestion.objects.create(
                    question_id=question_id,
                    title_id=test,
                    question=question,
                    correct_option=correct_option,
                    explanation=explanation,
                )

                if files.get("questionImage"):
                    question_image = files["questionImage"]
                    question_image_name = f"question_id_{question_id}_ques.jpg"
                    question_image_path = os.path.join(
                        settings.MEDIA_ROOT, "ques_images", question_image_name
                    )
                    with open(question_image_path, "wb+") as destination:
                        for chunk in question_image.chunks():
                            destination.write(chunk)
                    test_question.question_img = os.path.join(
                        "media", "ques_images", question_image_name
                    )
                    test_question.save()

                test_option = TestOption.objects.create(
                    option_id=str(uuid.uuid4()),
                    question_id=test_question,
                    option1=options[0],
                    option2=options[1],
                    option3=options[2],
                    option4=options[3],
                )

                for i in range(1, 5):
                    option_image = files.get(f"option{i}Image")
                    if option_image:
                        option_image_name = f"question_id_{question_id}_opt{i}.jpg"
                        option_image_path = os.path.join(
                            settings.MEDIA_ROOT, "ques_images", option_image_name
                        )
                        with open(option_image_path, "wb+") as destination:
                            for chunk in option_image.chunks():
                                destination.write(chunk)
                        setattr(
                            test_option,
                            f"option{i}_img",
                            os.path.join("media", "ques_images", option_image_name),
                        )
                test_option.save()

                if files.get("explanationImage"):
                    explanation_image = files["explanationImage"]
                    explanation_image_name = f"question_id_{question_id}_exp.jpg"
                    explanation_image_path = os.path.join(
                        settings.MEDIA_ROOT, "ques_images", explanation_image_name
                    )
                    with open(explanation_image_path, "wb+") as destination:
                        for chunk in explanation_image.chunks():
                            destination.write(chunk)
                    test_question.explanation_img = os.path.join(
                        "media", "ques_images", explanation_image_name
                    )
                    test_question.save()

                response_data = {
                    "message": "Question added successfully",
                    "question_id": test_question.question_id,
                    "question": test_question.question,
                    "options": options,
                }

            else:
                return JsonResponse({"error": "Invalid content type"}, status=400)

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_subtopics(request):
    if request.method == "GET":
        try:
            topic_id = request.GET.get("topic_id")

            print("--------------", topic_id)
            if not topic_id:
                return JsonResponse({"error": "Topic ID is required"}, status=400)

            # Find the topic (not directly required for the subtopics fetch, but for validation)
            # topic = get_object_or_404(Topic, topic_id=topic_id)  # Optional check

            # Fetch subtopics for the given topic_id
            subtopics = SubTopic.objects.filter(topic_id=topic_id)

            # Prepare the subtopics data to send in the response
            subtopics_list = [
                {
                    "subtopic_id": subtopic.subtopic_id,
                    "name": subtopic.name,
                    "created_at": subtopic.created_at,
                    "created_by": get_user_name(
                        subtopic.created_by_id
                    ),  # Assuming 'User' model has a 'username' field
                }
                for subtopic in subtopics
            ]

            print(subtopics_list)

            return JsonResponse(subtopics_list, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_titles(request):
    if request.method == "GET":
        try:
            topic_id = request.GET.get("topic_id")
            subtopic_id = request.GET.get("subtopic_id")
            utils_type = request.GET.get("utils_type")

            if not topic_id or not subtopic_id or not utils_type:
                return JsonResponse(
                    {"error": "topic_id, subtopic_id, and utils_type are required"},
                    status=400,
                )

            # Find the subtopic
            subtopic = SubTopic.objects.filter(
                subtopic_id=subtopic_id, topic_id=topic_id
            ).first()

            if not subtopic:
                return JsonResponse({"error": "Subtopic not found"}, status=404)

            # Validate utils_type and process only for Practices and Test
            if utils_type not in ["Practices", "Test"]:
                return JsonResponse(
                    {"error": "Invalid utils type specified"}, status=400
                )

            # Fetch titles based on the utils type
            if utils_type == "Practices":
                titles = Practice.objects.filter(
                    subtopic_id=subtopic_id, topic_id=topic_id
                )
            elif utils_type == "Test":
                titles = Test.objects.filter(subtopic_id=subtopic_id, topic_id=topic_id)

            titles_list = [
                {
                    "title": title.title,
                    "title_id": title.title_id,
                    "attempts": title.attempts,
                    "duration": title.duration,
                }
                for title in titles
            ]

            return JsonResponse(titles_list, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def organize_subtopic(request, topic_id, subtopic_id):
    if request.method == "GET":
        try:
            # Fetch subtopic by topic_id and subtopic_id
            subtopic = SubTopic.objects.filter(
                subtopic_id=subtopic_id, topic_id=topic_id
            ).first()

            if not subtopic:
                return JsonResponse({"error": "Subtopic not found"}, status=404)

            return JsonResponse({"name": subtopic.name}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "POST":
        print("CALLEDPOST")
        try:
            # Retrieve data from the request body

            body = get_body_data(request)
            name = body.get("name")

            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)

            # Find the subtopic to update
            subtopic = SubTopic.objects.filter(
                subtopic_id=subtopic_id, topic_id=topic_id
            ).first()

            if not subtopic:
                return JsonResponse({"error": "Subtopic not found"}, status=404)

            # Update the subtopic
            subtopic.name = name
            subtopic.save()

            return JsonResponse(
                {"message": "Subtopic updated successfully"}, status=200
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "DELETE":
        try:
            # Find the subtopic to delete
            subtopic = SubTopic.objects.filter(
                subtopic_id=subtopic_id, topic_id=topic_id
            ).first()

            if not subtopic:
                return JsonResponse({"error": "Subtopic not found"}, status=404)

            # Delete the subtopic
            subtopic.delete()

            return JsonResponse(
                {"message": "Subtopic deleted successfully"}, status=200
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_question(request, title_id):
    try:
        # Get the query parameters
        topic_id = request.GET.get("topic_id")
        subtopic_id = request.GET.get("subtopic_id")
        utils = request.GET.get("utils")

        # Handle the requested utility (Practices or Test)
        if utils == "Practices":
            # Fetch the Practice objects associated with the subtopic
            practice = Practice.objects.filter(
                title_id=title_id, topic_id=topic_id, subtopic_id=subtopic_id
            ).first()

            # Fetch associated questions
            practice_questions = PracticeQuestion.objects.filter(title_id=title_id)

            questions_data = []

            for pq in practice_questions:
                options = PracticeOption.objects.filter(question_id_id=pq.question_id)
                options_data = [
                    {
                        "option_id": option.option_id,
                        "option1": option.option1,
                        "option1_img": (
                            option.option1_img if option.option1_img else None
                        ),
                        "option2": option.option2,
                        "option2_img": (
                            option.option2_img if option.option2_img else None
                        ),
                        "option3": option.option3,
                        "option3_img": (
                            option.option3_img if option.option3_img else None
                        ),
                        "option4": option.option4,
                        "option4_img": (
                            option.option4_img if option.option4_img else None
                        ),
                    }
                    for option in options
                ]

                questions_data.append(
                    {
                        "question_id": pq.question_id,
                        "question": pq.question,
                        "question_img": pq.question_img if pq.question_img else None,
                        "correct_option": pq.correct_option,
                        "explanation": pq.explanation,
                        "explanation_img": (
                            pq.explanation_img if pq.explanation_img else None
                        ),
                        "options": [
                            {
                                "text": options_data[0]["option1"],
                                "image": options_data[0]["option1_img"],
                            },
                            {
                                "text": options_data[0]["option2"],
                                "image": options_data[0]["option2_img"],
                            },
                            {
                                "text": options_data[0]["option3"],
                                "image": options_data[0]["option3_img"],
                            },
                            {
                                "text": options_data[0]["option4"],
                                "image": options_data[0]["option4_img"],
                            },
                        ],
                    }
                )

            response_data = {
                "title": practice.title,
                "title_id": practice.title_id,
                "questions": questions_data,
            }

            return JsonResponse(response_data, status=200, safe=False)

        elif utils == "Test":
            # Fetch the Test objects associated with the subtopic
            test = Test.objects.filter(
                title_id=title_id, topic_id=topic_id, subtopic_id=subtopic_id
            ).first()

            # Fetch associated questions
            test_questions = TestQuestion.objects.filter(title_id=title_id)
            questions_data = []

            for tq in test_questions:
                options = TestOption.objects.filter(question_id_id=tq.question_id)
                options_data = [
                    {
                        "option_id": option.option_id,
                        "option1": option.option1,
                        "option1_img": (
                            option.option1_img if option.option1_img else None
                        ),
                        "option2": option.option2,
                        "option2_img": (
                            option.option2_img if option.option2_img else None
                        ),
                        "option3": option.option3,
                        "option3_img": (
                            option.option3_img if option.option3_img else None
                        ),
                        "option4": option.option4,
                        "option4_img": (
                            option.option4_img if option.option4_img else None
                        ),
                    }
                    for option in options
                ]

                questions_data.append(
                    {
                        "question_id": tq.question_id,
                        "question": tq.question,
                        "question_img": tq.question_img if tq.question_img else None,
                        "correct_option": tq.correct_option,
                        "explanation": tq.explanation,
                        "explanation_img": (
                            tq.explanation_img if tq.explanation_img else None
                        ),
                        "options": [
                            {
                                "text": options_data[0]["option1"],
                                "image": options_data[0]["option1_img"],
                            },
                            {
                                "text": options_data[0]["option2"],
                                "image": options_data[0]["option2_img"],
                            },
                            {
                                "text": options_data[0]["option3"],
                                "image": options_data[0]["option3_img"],
                            },
                            {
                                "text": options_data[0]["option4"],
                                "image": options_data[0]["option4_img"],
                            },
                        ],
                    }
                )

            response_data = {
                "title": test.title,
                "title_id": test.title_id,
                "questions": questions_data,
            }

            return JsonResponse(response_data, status=200, safe=False)

    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)


def get_title(request):
    try:
        # Get the query parameters
        topic_id = request.GET.get("topic_id")
        subtopic_id = request.GET.get("subtopic_id")
        utils_type = request.GET.get("utils_type")
        title_id = request.GET.get("title_id")

        # Fetch the topic from the database
        topic = Topic.objects.filter(topic_id=topic_id).first()
        if not topic:
            return JsonResponse({"error": "Topic not found"}, status=404)

        # Fetch the subtopic from the topic
        subtopic = SubTopic.objects.filter(
            subtopic_id=subtopic_id, topic_id=topic
        ).first()
        if not subtopic:
            return JsonResponse({"error": "Subtopic not found"}, status=404)

        # Validate the utility type (Practices or Test)
        if utils_type not in ["Practices", "Test"]:
            return JsonResponse({"error": "Invalid utils type specified"}, status=400)

        # Fetch the title based on the utility type
        title = None
        if utils_type == "Practices":
            title = Practice.objects.filter(
                title_id=title_id, topic_id=topic, subtopic_id=subtopic
            ).first()
        elif utils_type == "Test":
            title = Test.objects.filter(
                title_id=title_id, topic_id=topic, subtopic_id=subtopic
            ).first()

        if not title:
            return JsonResponse({"error": "Title not found"}, status=404)

        # Return the title data in JSON format
        return JsonResponse(
            {
                "title_id": title.title_id,
                "title": title.title,
                "topic_id": title.topic_id.topic_id,
                "subtopic_id": title.subtopic_id.subtopic_id,
                "duration": title.duration,  # Added duration field
                "attempts": title.attempts,  # Added attempts field
            }
        )

    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)


def download_sample(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Extract required fields from request body
        data = get_body_data(request)
        topic_id = data.get("topic_id")
        subtopic_id = data.get("subtopic_id")
        title_id = data.get("title_id")
        type_ = data.get("type")
        no_of_questions = int(data.get("no_of_questions", 0))

        # Validate required fields
        if not all([topic_id, subtopic_id, title_id, type_, no_of_questions]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Sample data
        sample_data = {
            "topic_id": topic_id,
            "subtopic_id": subtopic_id,
            "title_id": title_id,
            "type": type_,
            "question": "What is LED?",
            "options": [
                "Light Emitting Diode",
                "Low Energy Device",
                "Light Energy Device",
                "Linear Energy Diode",
            ],
            "correct_option": 1,
            "explanation": (
                "An LED is a semiconductor device that emits light when an electric current passes through it. "
                "It is widely used in electronic displays, lighting, and indicators."
            ),
        }

        # Prepare rows for the spreadsheet
        rows = []
        for i in range(1, no_of_questions + 1):
            if i == 1:
                rows.append(
                    {
                        "S_No": i,
                        "topic_id": sample_data["topic_id"],
                        "subtopic_id": sample_data["subtopic_id"],
                        "title_id": sample_data["title_id"],
                        "type": sample_data["type"],
                        "question": sample_data["question"],
                        "option_1": sample_data["options"][0],
                        "option_2": sample_data["options"][1],
                        "option_3": sample_data["options"][2],
                        "option_4": sample_data["options"][3],
                        "correct_option": sample_data["correct_option"],
                        "explanation": sample_data["explanation"],
                    }
                )
            else:
                rows.append(
                    {
                        "S_No": i,
                        "topic_id": sample_data["topic_id"],
                        "subtopic_id": sample_data["subtopic_id"],
                        "title_id": sample_data["title_id"],
                        "type": sample_data["type"],
                        "question": "",
                        "option_1": "",
                        "option_2": "",
                        "option_3": "",
                        "option_4": "",
                        "correct_option": "",
                        "explanation": "",
                    }
                )

        # Create a Pandas DataFrame
        df = pd.DataFrame(rows)

        # Save the DataFrame to an Excel file in memory
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sample Data")

        # Set up the response to send the file
        buffer.seek(0)
        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="Sample_Format  .xlsx"'

        return response

    except Exception as e:

        print(e)
        return JsonResponse({"error": str(e)}, status=500)


import os
from django.core.files.storage import FileSystemStorage


def add_questions_import(request):
    print("CALEED")

    if request.method == "POST":
        try:
            # Handle file upload
            uploaded_file = request.FILES.get("file")
            if not uploaded_file:
                return JsonResponse({"error": "No file uploaded"}, status=400)

            # Save the uploaded file temporarily
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)
            full_file_path = fs.path(file_path)

            # Read the Excel file
            df = pd.read_excel(full_file_path)

            for _, row in df.iterrows():
                # Extract data from each row
                topic_id = row.get("topic_id")
                subtopic_id = row.get("subtopic_id")
                title_id = row.get("title_id")
                type_ = row.get("type")
                question_text = row.get("question")
                option_1 = row.get("option_1")
                option_2 = row.get("option_2")
                option_3 = row.get("option_3")
                option_4 = row.get("option_4")
                correct_option = row.get("correct_option")
                explanation = row.get("explanation")

                # Check and process based on type
                if type_ == "Practices":
                    # try:
                    #     section = Practice.objects.get(
                    #         subtopic_id_id=subtopic_id, title_id_id=title_id
                    #     )
                    # except Practice.DoesNotExist:
                    #     print(f"Practice section not found for title_id: {title_id}")
                    #     continue

                    # Create the question
                    question = PracticeQuestion.objects.create(
                        question_id=get_unique_id(),
                        title_id_id=title_id,
                        question=question_text,
                        correct_option=correct_option,
                        explanation=explanation,
                    )

                    # Create the options
                    PracticeOption.objects.create(
                        option_id=get_unique_id(),
                        question_id_id=question.question_id,
                        option1=option_1,
                        option2=option_2,
                        option3=option_3,
                        option4=option_4,
                    )

                elif type_ == "Test":
                    # try:
                    #     section = Test.objects.get(
                    #         subtopic_id_id=subtopic_id, title_id_id=title_id
                    #     )
                    # except Test.DoesNotExist:
                    #     print(f"Test section not found for title_id: {title_id}")
                    #     continue

                    # Create the question
                    question = TestQuestion.objects.create(
                        question_id=get_unique_id(),
                        title_id_id=title_id,
                        question=question_text,
                        correct_option=correct_option,
                        explanation=explanation,
                    )

                    # Create the options
                    TestOption.objects.create(
                        option_id=get_unique_id(),
                        question_id_id=question.question_id,
                        option1=option_1,
                        option2=option_2,
                        option3=option_3,
                        option4=option_4,
                    )
                else:
                    print(f"Invalid type: {type_}")
                    continue

            # Delete the temporary file
            if os.path.exists(full_file_path):
                os.remove(full_file_path)

            return JsonResponse(
                {"message": "Bulk questions added successfully."}, status=200
            )

        except Exception as e:

            print(e)
            # Ensure temporary file is removed on error
            if os.path.exists(full_file_path):
                os.remove(full_file_path)
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def manage_content(request):
    if request.method == "GET":
        try:
            topic_id = request.GET.get("topic_id")
            subtopic_id = request.GET.get("subtopic_id")

            print(topic_id)
            print(subtopic_id)

            # Fetch the learning material content
            material = LearningMaterial.objects.filter(
                topic_id_id=topic_id, subtopic_id_id=subtopic_id
            ).first()

            content = ""

            if material:
                content = material.content

            return JsonResponse({"content": content})
        except Exception as e:

            print("---------", e)
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "POST":
        try:
            # Parse JSON request body
            body = json.loads(request.body)
            topic_id = body.get("topic_id")
            subtopic_id = body.get("subtopic_id")
            content = body.get("content")

            # Validate topic and subtopic existence
            topic = Topic.objects.filter(topic_id=topic_id).first()
            if not topic:
                return JsonResponse({"error": "Topic not found"}, status=404)

            subtopic = SubTopic.objects.filter(
                subtopic_id=subtopic_id, topic_id=topic
            ).first()
            if not subtopic:
                return JsonResponse({"error": "Subtopic not found"}, status=404)

            # Update or create the learning material
            material, created = LearningMaterial.objects.update_or_create(
                topic_id=topic, subtopic_id=subtopic, defaults={"content": content}
            )

            message = (
                "Content created successfully!"
                if created
                else "Content updated successfully!"
            )
            return JsonResponse({"message": message})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def get_user_topics(request):
    if request.method == "GET":
        try:
            # Extract the user_id parameter from the query string
            user_id = request.GET.get("user_id")

            if not user_id:
                return JsonResponse(
                    {"error": "User ID parameter is required"}, status=400
                )

            # Query the UserTopic model to fetch topics for the specified user
            user_topics = UserTopic.objects.filter(user_id=user_id)

            # Serialize the user topics data
            topics_data = []
            for user_topic in user_topics:
                # Fetch the associated Topic object to get domain_type and tech_type
                topic = user_topic.topic_id  # This is the related Topic object

                topics_data.append(
                    {
                        "topic_id": topic.topic_id,  # Topic ID from Topic model
                        "name": user_topic.name,
                        "created_by": user_topic.created_by,
                        "created_at": user_topic.created_at,
                        "domain_type": topic.domain_type,  # domain_type from Topic model
                        "tech_type": topic.tech_type,  # tech_type from Topic model
                    }
                )

            return JsonResponse(topics_data, safe=False)
        except Exception as e:
            return JsonResponse(
                {"error": f"Failed to fetch topics: {str(e)}"}, status=500
            )
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def get_users_by_role(request):
    if request.method == "GET":
        try:
            # Get the 'role' parameter from the query string
            role = request.GET.get("role")

            if not role:
                return JsonResponse({"error": "Role parameter is required"}, status=400)

            # Filter users by role
            users = User.objects.filter(role=role)

            # Prepare a list of serialized user data
            user_data = [
                {
                    "user_id": user.user_id,
                    "name": user.name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                    "email": user.email,
                    "dob": user.dob,
                    "city": user.city,
                    "state": user.state,
                    "country": user.country,
                    "type": user.type,
                }
                for user in users
            ]

            return JsonResponse(user_data, safe=False)
        except Exception as e:

            print(e)
            return JsonResponse(
                {"error": f"Failed to fetch users: {str(e)}"}, status=500
            )
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def allocate_topics(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Parse the JSON body
        body = json.loads(request.body)
        user_id = body.get("user_id")
        topics = body.get("topics")  # List of topic IDs

        print(user_id, topics, "--><")

        if not user_id or not topics:
            return JsonResponse(
                {"error": "user_id and topics are required"}, status=400
            )

        UserTopic.objects.filter(user_id_id=user_id).delete()

        # Allocate topics
        allocated_topics = []
        for topic_id in topics:
            try:
                topic = Topic.objects.get(topic_id=topic_id)

                created_by_id = topic.created_by.user_id

                print(created_by_id)

                # Create or update UserTopic
                user_topic, created = UserTopic.objects.update_or_create(
                    user_id_id=user_id,
                    topic_id_id=topic.topic_id,
                    defaults={
                        "name": topic.name,
                        "created_by": get_user_name(created_by_id),
                        "created_at": topic.created_at,
                    },
                )

                user_topic.save()

            except Topic.DoesNotExist:
                return JsonResponse(
                    {"error": f"Topic with ID {topic_id} not found"}, status=404
                )

        return JsonResponse(
            {
                "message": "Topics allocated successfully",
                "allocated_topics": allocated_topics,
            }
        )

    except json.JSONDecodeError as e:
        print(e)

        return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    except Exception as e:

        print(e)
        return JsonResponse(
            {"error": f"Failed to allocate topics: {str(e)}"}, status=500
        )


def get_attempts(request, user_id, title_id):
    try:
        # Check if the user exists
        if not User.objects.filter(user_id=user_id).exists():
            return JsonResponse({"error": "User not found"}, status=404)

        # Check if the test exists
        test = Test.objects.filter(title_id=title_id).first()
        if not test:
            return JsonResponse({"error": "Test not found"}, status=404)

        # Count the number of attempts for the given user_id and title_id
        user_attempts = TestHistory.objects.filter(
            user_id_id=user_id, title_id_id=title_id
        ).count()

        # Prepare the response data
        response_data = {
            "title_id": title_id,
            "user_attempts": user_attempts,
            "title_attempts": test.attempts,
            "title_duration": test.duration,
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        return JsonResponse(
            {"error": "Failed to retrieve attempts count", "details": str(e)},
            status=500,
        )


def get_test_history_by_user(request, user_id):
    try:
        # Check if user exists
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Retrieve all test history for the user
        test_history = TestHistory.objects.filter(user_id=user)

        print(test_history)

        # Prepare the response with test history and associated reports
        response_data = []
        for history in test_history:
            # print(history)
            print(history.test_id)
            report = Report.objects.filter(
                test_id_id=history.test_id
            ).all()  # Fetch all associated reports for the test
            report_data = []

            # print(report)

            for idx, report_item in enumerate(report, 1):
                # For each report, create a dictionary with the required fields

                rep = report_item.report
                report_data.append(rep)
            # Append the test history along with report data
            response_data.append(
                {
                    "test_id": history.test_id,
                    "user_id": str(history.user_id.user_id),
                    "topic_id": str(history.topic_id.topic_id),
                    "subtopic_id": str(history.subtopic_id.subtopic_id),
                    "title": history.title,
                    "title_id": str(history.title_id.title_id),
                    "type": history.type,
                    "start_at": history.start_at,
                    "finished_at": history.finished_at,
                    "status": history.status,
                    "score": history.score,
                    "total_questions": history.total_question,
                    "report": report_data,
                }
            )

        return JsonResponse(response_data, safe=False, status=200)

    except Exception as e:
        return JsonResponse(
            {"error": "Failed to retrieve test history", "details": str(e)}, status=500
        )


def get_test_history_by_user_and_test(request, user_id, test_id):
    try:
        # Check if user exists
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Retrieve test history for the specific user and test
        test_history = TestHistory.objects.filter(user_id=user, test_id=test_id).first()

        if not test_history:
            return JsonResponse(
                {"error": "Test history not found for this user and test"}, status=404
            )

        # Prepare the response with test history and associated reports
        report = Report.objects.filter(
            test_id_id=test_history.test_id
        ).all()  # Fetch all associated reports for the test
        report_data = []

        for idx, report_item in enumerate(report, 1):
            # For each report, create a dictionary with the required fields
            rep = report_item.report
            report_data.append(rep)

        # Prepare the final response data
        response_data = {
            "test_id": test_history.test_id,
            "user_id": str(test_history.user_id.user_id),
            "topic_id": str(test_history.topic_id.topic_id),
            "subtopic_id": str(test_history.subtopic_id.subtopic_id),
            "title": test_history.title,
            "title_id": str(test_history.title_id.title_id),
            "type": test_history.type,
            "start_at": test_history.start_at,
            "finished_at": test_history.finished_at,
            "status": test_history.status,
            "score": test_history.score,
            "total_questions": test_history.total_question,
            "report": report_data,
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        return JsonResponse(
            {"error": "Failed to retrieve test history", "details": str(e)}, status=500
        )


def get_question_count(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    # Retrieve query parameters
    topic_id = request.GET.get("topic_id")
    subtopic_id = request.GET.get("subtopic_id")
    title_id = request.GET.get("title_id")
    util_type = request.GET.get("util_type")

    print(request.GET)
    print(topic_id, subtopic_id, title_id, util_type)

    # Validate required parameters
    if not all([topic_id, subtopic_id, title_id, util_type]):
        return JsonResponse(
            {"status": "error", "message": "Missing required parameters."}, status=400
        )

    try:
        # Verify `title_id` in the respective model based on `util_type`
        if util_type.lower() == "practice":
            # Check if `title_id` exists in `Practice`
            title = Practice.objects.filter(title_id=title_id).first()
            if not title:
                return JsonResponse(
                    {"status": "error", "message": "Practice title not found."},
                    status=404,
                )

            # Get the question count from `PracticeQuestion`
            question_count = PracticeQuestion.objects.filter(title_id=title).count()

        elif util_type.lower() == "test":
            # Check if `title_id` exists in `Test`
            title = Test.objects.filter(title_id=title_id).first()
            if not title:
                return JsonResponse(
                    {"status": "error", "message": "Test title not found."}, status=404
                )

            # Get the question count from `TestQuestion`
            question_count = TestQuestion.objects.filter(title_id=title).count()

        else:
            return JsonResponse(
                {"status": "error", "message": "Invalid utility type."}, status=400
            )

        # Return the question count
        return JsonResponse(
            {"status": "success", "question_count": question_count}, status=200
        )

    except Exception as e:
        print("------", e)
        return JsonResponse(
            {"status": "error", "message": f"An error occurred: {str(e)}"}, status=500
        )


from django.conf import settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(
    settings.GOOGLE_CREDENTIALS_PATH, scopes=SCOPES
)
client = gspread.authorize(creds)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1VA89fyCd3_DF54p3JCg5DG1dqHMjrNOa66KDqUgN-2U/edit"
sheet = client.open_by_url(SHEET_URL).sheet1  # Access the first sheet


def finish_test(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Parse the incoming JSON payload
        payload = json.loads(request.body)

        # Extract required data
        user_id = payload.get("user_id")
        topic_id = payload.get("topic_id")
        subtopic_id = payload.get("subtopic_id")
        title_id = payload.get("title_id")
        type = payload.get("type")
        start_at = payload.get("start_at")
        finished_at = payload.get("finished_at")
        status = payload.get("status")
        score = payload.get("score")
        total_questions = payload.get("total_questions")
        report_data = payload.get("report", [])

        # Validate required fields
        if not all([user_id, topic_id, subtopic_id, title_id, type]):
            return JsonResponse(
                {"error": "Missing required fields in payload"}, status=400
            )

        # Fetch related objects
        user = User.objects.filter(user_id=user_id).first()
        topic = Topic.objects.filter(topic_id=topic_id).first()
        subtopic = SubTopic.objects.filter(subtopic_id=subtopic_id).first()
        test = Test.objects.filter(title_id=title_id).first()

        if not all([user, topic, subtopic, test]):
            return JsonResponse(
                {"error": "Invalid references for user, topic, subtopic, or test"},
                status=404,
            )

        # Generate unique test ID
        test_u_id = str(uuid.uuid4())

        # Create a new TestHistory entry
        test_history = TestHistory.objects.create(
            test_id=test_u_id,
            user_id=user,
            topic_id=topic,
            subtopic_id=subtopic,
            title_id=test,
            type=type,
            title=test.title,  # Fetching title from Test model
            start_at=start_at,
            finished_at=finished_at,
            status=status,
            score=score,
            total_question=total_questions,
        )

        # Save reports
        for report_item in report_data:
            Report.objects.create(
                test_id=test_history,
                report=report_item,
            )

        # Retrieve User Details (Name, Phone Number)
        user_name = user.name
        user_phone = user.phone_number
        user_email = user.email

        # Retrieve Title from Test
        test_title = test.title

        # Get existing row count (excluding header)
        existing_data = sheet.get_all_values()
        row_count = len(existing_data)

        # Prepare Data for Google Sheet
        new_entry = [
            user_name,  # User Name
            user_phone,  # User Phone Number
            test_title,  # Test Title
            total_questions,  # Total Questions
            score,  # Score
        ]

        # Append Data to Google Sheet
        new_row = [row_count] + new_entry  # S.No is row count
        sheet.append_row(new_row)

        try:
            queue_email(user_email, user_name, test_title, total_questions, score)
        except Exception as err:
            print("Error senting email : " + str(err))

        return JsonResponse(
            {
                "message": "Test finished successfully and stored in Google Sheets",
                "testID": test_u_id,
            },
            status=200,
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


def organize_title(request, id):
    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            topic_id = body.get("topic_id")
            subtopic_id = body.get("subtopic_id")
            title_type = body.get("type")  # "Practices" or "Test"
            new_title = body.get("newTitle")
            duration = body.get("duration", None)
            attempts = body.get("attempts", None)

            if not topic_id or not subtopic_id or not title_type or not new_title:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if title_type == "Practices":
                title = Practice.objects.filter(
                    title_id=id, topic_id=topic_id, subtopic_id=subtopic_id
                ).first()
            elif title_type == "Test":
                title = Test.objects.filter(
                    title_id=id, topic_id=topic_id, subtopic_id=subtopic_id
                ).first()
            else:
                return JsonResponse({"error": "Invalid type specified"}, status=400)

            if not title:
                return JsonResponse({"error": "Title not found"}, status=404)

            title.title = new_title
            if duration is not None:
                title.duration = duration
            if attempts is not None:
                title.attempts = attempts
            title.save()

            return JsonResponse(
                {
                    "message": "Title updated successfully",
                    "title": {
                        "title_id": title.title_id,
                        "title": title.title,
                        "duration": title.duration,
                        "attempts": title.attempts,
                    },
                }
            )
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to update title", "details": str(e)}, status=500
            )

    elif request.method == "DELETE":
        try:
            topic_id = request.GET.get("topic_id")
            subtopic_id = request.GET.get("subtopic_id")
            title_type = request.GET.get("type")  # "Practices" or "Test"

            if not topic_id or not subtopic_id or not title_type:
                return JsonResponse(
                    {"error": "Missing required query parameters"}, status=400
                )

            if title_type == "Practices":
                title = Practice.objects.filter(
                    title_id=id, topic_id=topic_id, subtopic_id=subtopic_id
                ).first()
            elif title_type == "Test":
                title = Test.objects.filter(
                    title_id=id, topic_id=topic_id, subtopic_id=subtopic_id
                ).first()
            else:
                return JsonResponse({"error": "Invalid type specified"}, status=400)

            if not title:
                return JsonResponse({"error": "Title not found"}, status=404)

            title.delete()

            return JsonResponse({"message": "Title deleted successfully"})
        except Exception as e:
            return JsonResponse(
                {"error": "Failed to delete title", "details": str(e)}, status=500
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


def update_question(request):
    if request.method == "POST":
        try:
            form_data = request.POST
            files = request.FILES

            question_id = form_data.get("question_id")
            question_text = form_data.get("question")
            correct_option = int(form_data.get("correct_option"))
            explanation = form_data.get("explanation")
            options = json.loads(form_data.get("options"))
            question_type = form_data.get("type")

            if question_type == "Practices":
                question = get_object_or_404(PracticeQuestion, question_id=question_id)
                option_model = PracticeOption
            elif question_type == "Test":
                question = get_object_or_404(TestQuestion, question_id=question_id)
                option_model = TestOption
            else:
                return JsonResponse({"error": "Invalid type specified"}, status=400)

            # Update question fields
            question.question = question_text
            question.correct_option = correct_option
            question.explanation = explanation

            # Handle question image
            if "question_image" in files:
                question_image = files["question_image"]
                question_image_name = f"question_id_{question_id}_ques.jpg"
                question_image_path = os.path.join(
                    settings.MEDIA_ROOT, "ques_images", question_image_name
                )
                with open(question_image_path, "wb+") as destination:
                    for chunk in question_image.chunks():
                        destination.write(chunk)
                question.question_img = os.path.join(
                    "media", "ques_images", question_image_name
                )
            elif "remove_question_image" in form_data:
                # Remove existing question image
                if question.question_img:
                    old_image_path = os.path.join("", question.question_img)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                    question.question_img = None

            # Handle explanation image
            if "explanation_image" in files:
                explanation_image = files["explanation_image"]
                explanation_image_name = f"question_id_{question_id}_exp.jpg"
                explanation_image_path = os.path.join(
                    settings.MEDIA_ROOT, "ques_images", explanation_image_name
                )
                with open(explanation_image_path, "wb+") as destination:
                    for chunk in explanation_image.chunks():
                        destination.write(chunk)
                question.explanation_img = os.path.join(
                    "media", "ques_images", explanation_image_name
                )
            elif "remove_explanation_image" in form_data:
                # Remove existing explanation image
                if question.explanation_img:
                    old_image_path = os.path.join(
                        "",
                        question.explanation_img,
                    )
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                    question.explanation_img = None

            question.save()

            # Update options
            options_obj = get_object_or_404(option_model, question_id=question)
            options_obj.option1 = options[0]
            options_obj.option2 = options[1]
            options_obj.option3 = options[2]
            options_obj.option4 = options[3]

            # Handle option images
            for i in range(1, 5):
                option_image = files.get(f"option{i}_image")
                if option_image:
                    option_image_name = f"question_id_{question_id}_opt{i}.jpg"
                    option_image_path = os.path.join(
                        settings.MEDIA_ROOT, "ques_images", option_image_name
                    )
                    with open(option_image_path, "wb+") as destination:
                        for chunk in option_image.chunks():
                            destination.write(chunk)
                    setattr(
                        options_obj,
                        f"option{i}_img",
                        os.path.join("media", "ques_images", option_image_name),
                    )
                elif f"remove_option{i}_image" in form_data:
                    # Remove existing option image
                    option_image_field = getattr(options_obj, f"option{i}_img")
                    if option_image_field:
                        old_image_path = os.path.join(
                            "",
                            option_image_field,
                        )
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                        setattr(options_obj, f"option{i}_img", None)

            options_obj.save()

            return JsonResponse(
                {
                    "message": "Question updated successfully",
                    "updated_question": {
                        "question_id": question.question_id,
                        "question": question.question,
                        "correct_option": question.correct_option,
                        "explanation": question.explanation,
                        "options": [
                            options_obj.option1,
                            options_obj.option2,
                            options_obj.option3,
                            options_obj.option4,
                        ],
                        "question_img": question.question_img,
                        "explanation_img": question.explanation_img,
                        "option_images": [
                            options_obj.option1_img,
                            options_obj.option2_img,
                            options_obj.option3_img,
                            options_obj.option4_img,
                        ],
                    },
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def delete_question(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        question_id = data.get("question_id")
        title_id = data.get("title_id")
        question_type = data.get("type")  # "Practice" or "Test"

        # Fetch and delete the question based on type
        if question_type == "Practices":
            question = get_object_or_404(
                PracticeQuestion, question_id=question_id, title_id=title_id
            )
            option_model = PracticeOption
        elif question_type == "Test":
            question = get_object_or_404(
                TestQuestion, question_id=question_id, title_id=title_id
            )
            option_model = TestOption
        else:
            return JsonResponse({"error": "Invalid type specified"}, status=400)

        # Delete associated images from the file system
        if question.question_img:
            question_image_path = os.path.join("", question.question_img)
            print(f"Question Image Path: {question_image_path}")  # Debugging
            if os.path.exists(question_image_path):
                os.remove(question_image_path)
                print("Question image deleted.")  # Debugging
            else:
                print(
                    "Question image does not exist at the specified path."
                )  # Debugging

        if question.explanation_img:
            explanation_image_path = os.path.join("", question.explanation_img)
            print(f"Explanation Image Path: {explanation_image_path}")  # Debugging
            if os.path.exists(explanation_image_path):
                os.remove(explanation_image_path)
                print("Explanation image deleted.")  # Debugging
            else:
                print(
                    "Explanation image does not exist at the specified path."
                )  # Debugging

        # Delete associated options and their images
        options = option_model.objects.filter(question_id=question)
        for option in options:
            for i in range(1, 5):
                option_image_field = getattr(option, f"option{i}_img")
                if option_image_field:
                    option_image_path = os.path.join("", option_image_field)
                    print(f"Option {i} Image Path: {option_image_path}")  # Debugging
                    if os.path.exists(option_image_path):
                        os.remove(option_image_path)
                        print(f"Option {i} image deleted.")  # Debugging
                    else:
                        print(
                            f"Option {i} image does not exist at the specified path."
                        )  # Debugging

        # Delete the options
        options.delete()

        # Delete the question
        question.delete()

        return JsonResponse({"message": "Question deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)
