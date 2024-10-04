from core.models import CustomUser as User


def update_user(user: User, **kwargs) -> User:
    for attr, value in kwargs.items():
        setattr(user, attr, value)
    if 'password' in kwargs:
        user.set_password(kwargs['password'])
    user.save()
    return user

def delete_user(user: User) -> None:
    # user.group_set.clear()
    user.user_groups.clear()
    user.tags.clear()

    user.delete()