from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import generics

from student.models import UserProfile

from labster.api.users.serializers import UserCreateSerializer, LabsterUserSerializer
from labster.api.users.serializers import CustomLabsterUser
from labster.api.views import AuthMixin


def get_user_as_custom_labster_user(user, password=None):
    labster_user = user.labster_user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    return CustomLabsterUser(
        id=user.id,
        user_id=user.id,
        is_labster_verified=labster_user.is_labster_verified,
        unique_id=labster_user.unique_id,
        nationality_name=labster_user.nationality.name,
        nationality=labster_user.nationality.code,
        language=labster_user.language,
        phone_number=labster_user.phone_number,
        user_type=labster_user.user_type,
        organization_name=labster_user.organization_name,
        user_school_level=labster_user.user_school_level,
        date_of_birth=labster_user.date_of_birth,
        name=profile.name,
        password=password,
        gender=profile.gender,
        year_of_birth=profile.year_of_birth,
        level_of_education=profile.level_of_education,
    )


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    model = User


class UserView(AuthMixin, generics.RetrieveUpdateAPIView):

    serializer_class = LabsterUserSerializer

    def get_object(self):
        try:
            user = self.get_queryset().get(id=self.kwargs.get('user_id'))
        except User.DoesNotExist:
            raise Http404

        password = self.request.DATA.get('password')
        return get_user_as_custom_labster_user(user, password)

    def get_queryset(self):
        return User.objects.all()