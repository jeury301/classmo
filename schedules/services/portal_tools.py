def is_member(user, group):
    """Helper function that checkes the membership of given group

        user (obj): An instance of the User model
        group (string): The name of a defined group
           
        Returns:
           True if membership exists, False otherwise
    """
    return user.groups.filter(name=group).exists()