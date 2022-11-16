from django.contrib.auth import get_user_model
User = get_user_model()

def update_account(user_email, stripe_account):
    user = User.objects.get(email = user_email)
    user.stripe_account = stripe_account
    user.save()