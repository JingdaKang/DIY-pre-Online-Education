from rest_framework import serializers
from backend.models import Note, NoteBook,Tag,Image



class NoteSerializer(serializers.ModelSerializer):
    note_create = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    note_modify = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    note_delete = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    tags = serializers.StringRelatedField(many=True,read_only=True)
    modifier_id = serializers.StringRelatedField()
    writer_id = serializers.StringRelatedField()
    class Meta:
        model = Note
        fields = ('id', 'note_title', 'note_text', 'note_type', 'note_create', 'note_modify','note_delete','writer_id','team_id','notebook_id','tags','modifier_id')

class NoteBookSerializerBase(serializers.ModelSerializer):
    notebook_create = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    notebook_modify = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = NoteBook
        fields = ('id', 'notebook_name', 'notebook_create', 'notebook_modify','creator_id','team_id')

class TagSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True,read_only=True)
    tag_create = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Tag
        fields = ('id','tag_name','tag_create','notes','creator_id')
class NoteBookSerializer(serializers.ModelSerializer):
    notebook_note = NoteSerializer(many=True,read_only=True)#一对多
    notebook_create = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    notebook_modify = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    modifier_id = serializers.StringRelatedField()
    creator_id = serializers.StringRelatedField()

    class Meta:
        model = NoteBook
        fields = ('id', 'notebook_name', 'notebook_create', 'notebook_modify', 'creator_id', 'team_id','notebook_note','modifier_id')

class ImageUploadSerializer(serializers.ModelSerializer):
    """上传图片到服务端的序列化器类"""
    class Meta:
        model = Image
        fields = ["id", "img"]

    def create(self, validated_data):
        img = validated_data.get("img")
        image_instance = Image.objects.create(img=img)
        return image_instance