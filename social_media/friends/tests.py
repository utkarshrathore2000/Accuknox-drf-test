from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer

User = get_user_model()


class GetUserListViewTests(APITestCase):
    def setUp(self):
        # Create some test users for the database
        self.user1 = User.objects.create(
            first_name="John", email="john@example.com", username="john"
        )
        self.user2 = User.objects.create(
            first_name="Jane", email="jane@example.com", username="jane"
        )

    def test_get_user_list_with_pagination(self):
        # Set up the URL for the API view
        url = reverse("get-user-list")

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
