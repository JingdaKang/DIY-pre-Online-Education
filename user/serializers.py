#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework import serializers

from notes.serializers import NoteBookSerializer, NoteSerializer
from backend.models import User,Team
from django.contrib.auth.models import Group as UserGroup

'''
class UserGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('id', 'name')

class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    groups = UserGroupSerializer(many=True, read_only=True)
    groups_id = serializers.ListField(write_only=True, required=True)

    class Meta:
        model = NewUser
        fields = ('id', 'username', 'email', 'groups', 'groups_id', 'name')
        write_only_fields = ('password',)
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #序列化所有字段
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    team_create = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    team_modify = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    leader_id = serializers.StringRelatedField()
    modifier_id = serializers.StringRelatedField()
    members = serializers.StringRelatedField(many=True,read_only=True)
    notebooks = NoteBookSerializer(many=True,read_only=True)
    notes = NoteSerializer(many=True,read_only=True)
    class Meta:
        model = Team
        fields = ('id','team_name','team_desc','team_create','team_modify','leader_id','modifier_id','members','notebooks','notes')
