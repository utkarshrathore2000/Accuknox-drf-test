from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer, FriendSerializer
from .models import Friends

User = get_user_model()


class FriendsAPITests(APITestCase):
    def setUp(self):
        # Create users for testing
        self.user1 = User.objects.create(email='user1@gmail.com', username='user1', password='password1')
        self.user2 = User.objects.create(email='user2@gmail.com', username='user2', password='password2')
        self.user3 = User.objects.create(email='user3@gmail.com', username='user3', password='password3')

        # Create a friend request from user1 to user2
        self.friend1 = Friends.objects.create(sender=self.user1, receiver=self.user2, status='pending')

        # Create an accepted friend between user1 and user3
        self.friend2 = Friends.objects.create(sender=self.user1, receiver=self.user3, status='accepted')


    def test_get_user_list_with_pagination(self):
        # Set up the URL for the API view
        url = reverse("get-user-list")

        self.client.force_authenticate(self.user1)
        # Make a GET request to the API view
        response = self.client.get(url)
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the serialized user list
        serialized_data = UserListSerializer(User.objects.all(), many=True).data
        self.assertEqual(len(response.json().get("results")), len(serialized_data))

    def test_get_user_list_with_search_query(self):
        # Set up the URL for the API view
        url = reverse("get-user-list")
        self.client.force_authenticate(self.user1)

        # Add a search query parameter to the URL
        search_query = "John"
        response = self.client.get(url, {"query": search_query})

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains only the user matching the search query
        serialized_data = UserListSerializer(
            User.objects.filter(first_name__icontains=search_query), many=True
        ).data
        self.assertEqual(len(response.json().get("results")), len(serialized_data))

    def test_get_accepted_friends_list(self):
        # Log in user1
        self.client.force_authenticate(self.user1)

        # Make a GET request to the GetFriendListView
        response = self.client.get(reverse('get-friend-list'))

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the expected data for accepted friends
        expected_data = UserListSerializer([self.user3], many=True).data
        self.assertEqual(len(response.json()['results']), len(expected_data))

    def test_get_pending_friend_requests_list(self):
        # Log in user2
        self.client.force_authenticate(self.user2)

        # Make a GET request to the GetFriendRequestListView
        response = self.client.get(reverse('get-friend-request-list'))

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the expected data for pending friend requests
        expected_data = FriendSerializer(Friends.objects.get(sender=self.user1, receiver=self.user2)).data
        self.assertEqual(len(response.json()['results']), len(expected_data))

    def test_send_friend_request(self):
        # Log in user1
        self.client.force_authenticate(self.user1)

        # Create a friend request to user2
        data = {'receiver': self.user2.id}
        response = self.client.post(reverse('send-friend-request'), data)

        # Check that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response data contains the expected data
        expected_data = FriendSerializer(Friends.objects.get(sender=self.user1, receiver=self.user2)).data
        self.assertEqual(response.data, expected_data)

    def test_accept_friend_request(self):
        # Log in user2
        self.client.force_authenticate(self.user2)

        # Get the pending friend request from user1
        friend_request = Friends.objects.get(sender=self.user1, receiver=self.user2)

        # Make a PATCH request to accept the friend request
        data = {'status': 'accepted'}
        response = self.client.patch(reverse('accept-friend-request', kwargs={'friend_id': friend_request.id}), data)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the status of the friend request is now 'accepted'
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'accepted')

    def test_reject_friend_request(self):
        # Log in user2
        self.client.force_authenticate(self.user2)

        # Get the pending friend request from user1
        friend_request = Friends.objects.get(sender=self.user1, receiver=self.user2)

        # Make a PATCH request to reject the friend request
        data = {'status': 'rejected'}
        response = self.client.patch(reverse('reject-friend-request', kwargs={'friend_id': friend_request.id}), data)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the status of the friend request is now 'rejected'
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'rejected')

    def tearDown(self):
        # Clean up after the tests
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()
        self.friend1.delete()
        self.friend2.delete()