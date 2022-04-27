from rest_framework import serializers
from .models import Team, Task, CustomUser

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

    def create(self, validated_data):
        """
            First saving the instance of Team, then adding the members to the Team
        """
        instance = Team.objects.create(name=validated_data['name'], leader=validated_data['leader'])
        [instance.members.add(member.id) for member in validated_data['members']]
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def create(self, validated_data):
        """
            for setting hashed password, when new registration is from API
        """
        user = CustomUser.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user