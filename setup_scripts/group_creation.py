from django.contrib.auth.models import Group

# create students group
group_1, created = Group.objects.get_or_create(name='Students')
print("Created 'Students' group")

# create instructors group
group_1, created = Group.objects.get_or_create(name='Instructors')
print("Created 'Instructors' group")

exit()