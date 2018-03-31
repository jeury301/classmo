import random

from django.conf import settings
from django.contrib.auth.models import Group, User

from .models import Comment, Post, Vote


def create_demo(subjects, instructors):
    """Creates posts and comments for demo purposes when
    called in Django's manage.py shell
    """

    # Create some user accounts to serve as authors
    # for our comments
    usernames = ['BobMcBobberson', 'YomboElite', 'xxEMO_BOIxx',
                 'sandwich_king', 'pm_me_a_panini', 'millivanilli4eva',
                 'ringo', 'paul', 'john', 'george', 'padma_lakshmi',
                 'emoji_roboto', 'm_thatcher', 'xi_j', 'j_trudeau']
    password = 'password'

    print("Loading student user data to db")
    # retrieving instructors from data

    users = []
    for username in usernames:
        try:
            # avoiding duplicate users
            User.objects.get(username=username)
        except User.DoesNotExist:
            # instructor with username does not exists, let's create it
            email = '{}@gmail.com'.format(username)
            password = 'password'
            user_entity = User.objects.create_user(
                username, email, password)

            user_entity.first_name = "Somename"
            user_entity.last_name = "Lastname"
            user_entity.save()
            users.append(user_entity)

            # adding instructor to instructor group
            student_group = Group.objects.get(name=settings.GROUPS["STUDENTS"])
            student_group.user_set.add(user_entity)

    post_content =  [('Is everyone doing their homework? I hope so',
                      '...cause some of those quiz scores I saw were pretty NOT SO GOOD.'),
                     ('Attn class: Hackathon at NJIT next week',
                      "If you're interested, check out yoaf.org to register."),
                     ('NJIT CS department in the news.',
                      "It's true - check out the ACM's Journal of Good Stuff, April issue."),
                     ("Big time BBQ champion coming to Newark",
                      "I have no idea what Big Bogus Quidditch involves, but it sounds interesting"),
                     ("Large cat alert in Essex!",
                      "This mini monster is going to eat a human if we don't band together and keep our wits about us."),
                     ("Did anyone see Blade Runner 2049?",
                      "If not, what are you doing with your life? It's pretty good."),
                     ("Congratulations!!",
                      "Congratulations! ConGRATulations. Congradulashuuuuns. Congratulations!"),
                     ("Businesses currently looking for COBOL programmers.",
                      "Who doesn't like COBOL?")
                    ]
    comment_content = ["Well, I never!",
                       "I have to disagree completely",
                       "lol ok",
                       "first thing's first - you're wrong.  second, your opinon is garbage-elite ",
                       "That's some pleasant content if I've ever seen it.",
                       "User engagement is off the CHARTS",
                       "The rent is too darn high",
                       "Each day / I greet like a new sandwich / flying high",
                       "Personally, I'm at liberty to discuss nothing",
                       "Thanks, friendo.",
                       "I get misty-eyed when that commercial comes on",
                       "Time to make the doughnuts!",
                       "I honestly don't understand what red black trees are for",
                       "I heard that 'Fresh Prince of Bel Aire' is in the public domain.",
                       "It is possible to get an A",
                       "Thank you for the vote of confidence!",
                       "This.  A million times this.",
                       "Facebook stole my data!",
                       "Go Highlanders!",
                       "Please, be a little more civil",
                       "I binge watch The Great British Baking Show",
                       "YOOOOOOOooooooOOOoooo",
                       "I'm more a dog person than a cat person",
                       "I'm more of a cat person than a dog person",
                       "meh",
                       "I am a content MASTER, with MILLIONS of likes on twitter!!"
                      ]


    # Create three posts for each subject
    posts = []
    for subj in subjects:
        for x in range(3):
            content = random.choice(post_content)
            author = random.choice(instructors)
            post = Post.create(subject=subj,
                               title=content[0],
                               body=content[1],
                               author=author)
            post.save()
            posts.append(post)

    # For each post, create a comment tree:
    for post in posts:
        #Direct responses
        author = random.choice(users)
        comm1 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm1.save()
        Vote.create(voter=author, value=1, comment=comm1)

        author = random.choice(users)
        comm2 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm2.save()
        Vote.create(voter=author, value=1, comment=comm2)

        # Responses to comm1
        author = random.choice(users)
        comm3 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm3.save()
        Vote.create(voter=author, value=1, comment=comm3)

        author = random.choice(users)
        comm4 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm4.save()
        Vote.create(voter=author, value=1, comment=comm4)

        # Responses to comm2
        author = random.choice(users)
        comm5 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm5.save()
        Vote.create(voter=author, value=1, comment=comm5)

        author = random.choice(users)
        comm6 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm6.save()
        Vote.create(voter=author, value=1, comment=comm6)

        # Response to comm3
        author = random.choice(users)
        comm7 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm7.save()
        Vote.create(voter=author, value=1, comment=comm7)

        # Response to comm4
        author = random.choice(users)
        comm8 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm8.save()
        Vote.create(voter=author, value=1, comment=comm8)

        # Response to comm5
        author = random.choice(users)
        comm9 = Comment.create(post=post,
                               body=random.choice(comment_content),
                               author=author)
        comm9.save()
        Vote.create(voter=author, value=1, comment=comm9)

        # Response to comm6
        author = random.choice(users)
        comm10 = Comment.create(post=post,
                                body=random.choice(comment_content),
                                author=author)
        comm10.save()
        Vote.create(voter=author, value=1, comment=comm10)
