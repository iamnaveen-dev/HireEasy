from rest_framework import serializers
from apps.companies.models import Company, CompanyMember
from apps.users.serializers import UserSerializer


class CompanySerializer(serializers.ModelSerializer):

    admin = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'description',
            'industry',
            'size',
            'website',
            'logo',
            'admin',
            'member_count',
            'is_active',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'admin',
            'is_active',
            'created_at',
        ]

    def get_member_count(self, obj):
        return obj.members.count()


class CreateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'name',
            'description',
            'industry',
            'size',
            'website',
            'logo',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        company = Company.objects.create(
            admin=request.user,
            **validated_data
        )
        CompanyMember.objects.create(
            company=company,
            user=request.user,
            role='hiring_manager'
        )
        return company


class CompanyMemberSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    company_name = serializers.CharField(
        source='company.name',
        read_only=True
    )

    class Meta:
        model = CompanyMember
        fields = [
            'id',
            'user',
            'company_name',
            'role',
            'joined_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'joined_at',
        ]


class InviteMemberSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(
        choices=[
            ('interviewer', 'Interviewer'),
            ('hiring_manager', 'Hiring Manager'),
            ('recruiter', 'Recruiter'),
        ],
        default='interviewer'
    )