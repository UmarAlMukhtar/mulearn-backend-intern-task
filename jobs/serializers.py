from rest_framework import serializers
from .models import Job, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class JobSerializer(serializers.ModelSerializer):
    # This shows the skill names instead of just IDs in the response
    skills = SkillSerializer(many=True, read_only=True)
    # This allows us to send a list of skill IDs when creating/updating
    skill_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all(), write_only=True, source='skills'
    )
    company = serializers.ReadOnlyField(source='company.username')

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'job_type', 'location', 
            'salary', 'skills', 'skill_ids', 'status', 'company', 'created_at'
        ]
        # Ensure companies can't change the status themselves via this serializer
        read_only_fields = ['status', 'company', 'created_at']