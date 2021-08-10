from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache


@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    ct = cache.get('count', 0, version=user.pk)
    newct = ct+1
    ct = cache.set('count', newct, 60*60*24, version=user.pk)


@receiver(user_login_failed)
def login_fail(sender, credentials, request, **kwargs):

    # login_fail_count = request.session.get(
    #     'login_fail_count', default=0)

    # new_login_fail_count = int(login_fail_count) + 1
    # print(f'from signal count: {new_login_fail_count}')
    # request.session['login_fail_count'] = new_login_fail_count

    # if new_login_fail_count == 3:
    #     request.session.set_expiry(60)

    login_fail_count = cache.get(
        'login_fail_count', 0, version=credentials['username'])

    new_login_fail_count = login_fail_count + 1

    cache.set(
        'login_fail_count', new_login_fail_count, 60, version=credentials['username'])

    print(f'login_fail_count:- {new_login_fail_count}')

    if new_login_fail_count == 2:
        cache.set(
            'fail_count', new_login_fail_count, 60, version=credentials['username'])
