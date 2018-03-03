from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
import logging

def is_member(user, group):
    """Helper function that checkes the membership of given group

        user (obj): An instance of the User model
        group (string): The name of a defined group
           
        Returns:
           True if membership exists, False otherwise
    """
    return user.groups.filter(name=group).exists()

def students_only(student_action):
    """@student Decorator, used as role-based permission filter only allowing
    students to execute the passed action

        student_action (function): The function that a user is trying to access
    """
    def filtered_student_action(request, **kwargs):
        is_student = request.user.groups.filter(name=settings.GROUPS["STUDENTS"])
        #print("Am I a student? {}".format(is_student))

        if is_student:
            # user is indeed a student, allowed the given requested action
            return student_action(request, **kwargs)
        else:
            return redirect("/")
    return filtered_student_action


def instructors_only(instructor_action):
    """@instructor Decorator, used as role-based permission filter only allowing
    instructor to execute the passed action

        instructor (function): The function that a user is trying to access
    """
    def filtered_instructor_action(request, **kwargs):
        is_instructor = request.user.groups.filter(name=settings.GROUPS["INSTRUCTORS"])

        if is_instructor:
            # user is indeed an instructor, allowed the given requested action
            return instructor_action(request, **kwargs)
        else:
            return redirect("/")
    return filtered_instructor_action

