from datetime import datetime

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


# VK
def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    url_method = settings.URL_METHOD
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about', 'photo_max_orig'])
    api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v={settings.API_VERSION}'

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data_json = response.json()['response'][0]

    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data_json['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'bdate' in data_json:
        try:
            birthday = datetime.strptime(data_json['bdate'], '%d.%m.%Y')
            age = datetime.now().year - birthday.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age
        except Exception as err:
            print(err)

    if 'about' in data_json:
        user.shopuserprofile.about = data_json['about']

    if 'photo_max_orig' in data_json:
        path = f'users_avatars/{user.username}s_avatar.jpg'
        photo_data = requests.get(data_json['photo_max_orig'])
        with open(f'{settings.BASE_DIR}{settings.MEDIA_URL}{path}', 'wb') as ava:
            ava.write(photo_data.content)
        user.avatar = path

    user.save()
