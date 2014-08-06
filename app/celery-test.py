from tasks import get_user

user = get_user.delay(5)
print user.get()
