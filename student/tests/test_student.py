import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from django.urls import reverse
from student.models import Student  # Change relative import to absolute import

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    user = User.objects.create_user(username='prasanth', password='Su6yalun@')
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.mark.django_db
def test_create_student(authenticated_client):
    url = reverse('student-list')
    data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'course': 'Math'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Student.objects.count() == 1
    assert Student.objects.get().first_name == 'John'

@pytest.mark.django_db
def test_get_students(authenticated_client):
    Student.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com', course='Math')
    Student.objects.create(first_name='Jane', last_name='Smith', email='jane.smith@example.com', course='Science')
    url = reverse('student-list')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_update_student(authenticated_client):
    student = Student.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com', course='Math')
    url = reverse('student-detail', kwargs={'pk': student.id})
    data = {'first_name': 'Johnny', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'course': 'Math'}
    response = authenticated_client.put(url, data, format='json')
    assert response.status_code == 200
    assert Student.objects.get(id=student.id).first_name == 'Johnny'

@pytest.mark.django_db
def test_delete_student(authenticated_client):
    student = Student.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com', course='Math')
    url = reverse('student-detail', kwargs={'pk': student.id})
    response = authenticated_client.delete(url)
    assert response.status_code == 204
    assert Student.objects.count() == 0
