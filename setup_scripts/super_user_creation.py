from django.contrib.auth.models import User

User.objects.filter(email='admin@example.com').delete()
User.objects.create_superuser('admin', 'admin@example.com', '12345')