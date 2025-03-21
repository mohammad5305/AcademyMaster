import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUpdateProfileView:

    def setup(self):
        self.data = {
            'birth_date': '1990-01-01',
            'address': 'Fake addr',
            'passport_id': '1234',
            'phone_number': '+989919919911',
        }

        self.url_path = 'profiles:update_profile'

    def test_update_profile_unauthorized(self, superuser, api_client):
        url = reverse(
            self.url_path,
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.put(url, self.data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, superuser, api_client):
        api_client.force_authenticate(user=superuser)
        url = reverse(
            self.url_path,
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.put(url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_update_profile_with_account(self, superuser, api_client):
        '''Update user first/last name alongside profile data'''
        updated_first_name = 'Updated First Name'
        updated_last_name = 'Updated Last Name'

        api_client.force_authenticate(user=superuser)
        self.data['first_name'] = updated_first_name
        self.data['last_name'] = updated_last_name

        url = reverse(
            self.url_path,
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.put(url, self.data, format='json')
        superuser.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK

        assert response.json()['first_name'] == updated_first_name
        assert response.json()['last_name'] == updated_last_name

        assert superuser.first_name == updated_first_name
        assert superuser.last_name == updated_last_name

    def test_update_profile_invalid_data(self, superuser, api_client):
        api_client.force_authenticate(user=superuser)
        url = reverse(
            self.url_path,
            kwargs={'profile_token': superuser.profile.token}
        )
        response = api_client.put(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_other_profile(self, superuser, active_account, api_client):
        '''Users can only update their own profile'''
        other_profile = active_account.profile
        api_client.force_authenticate(user=superuser)
        url = reverse(
            self.url_path,
            kwargs={'profile_token': other_profile.token}
        )
        response = api_client.put(url, {}, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
