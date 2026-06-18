from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.companies.models import Company, CompanyMember
from apps.companies.serializers import (
    CompanySerializer,
    CreateCompanySerializer,
    CompanyMemberSerializer,
    InviteMemberSerializer,
)
from apps.users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_company_view(request):
    if hasattr(request.user, 'company'):
        return Response({
            'error': 'You already have a company registered'
        }, status=status.HTTP_400_BAD_REQUEST)
    serializer = CreateCompanySerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        company = serializer.save()
        request.user.role = 'company_admin'
        request.user.save()
        return Response({
            'message': 'Company created successfully',
            'company': CompanySerializer(company).data,
        }, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company_view(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        return Response({
            'error': 'You do not have a company'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = CompanySerializer(company)
    return Response(serializer.data)
@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def update_company_view(request):
    try:
        company=request.user.company
    except Company.DoesNotExist:
        return Response({
            'error': 'You do not have a company'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = CreateCompanySerializer(
        company,
        data=request.data,
        partial=request.method == 'PATCH',
        context={'request': request}

        
    )
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Company updated successfully',
            'company': CompanySerializer(company).data,
        
        })
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST

    )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_member_view(request):
    try:
        company=request.user.company
    except Company.DoesNotExist:
        return Response({
            'error': 'You do not have a company'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer =InviteMemberSerializer(data=request.data)
    if serializer.is_valid():
        email=serializer.validated_data['email']
        role=serializer.validated_data('[role]')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'User with this email does not exist'
            },status=status.HTTP_404_NOT_FOUND)
        if CompanyMember.objects.filter(
            company=company,
            user=user
            
        ).exists():
            return Response({
                'error': 'User is already a member of the company'
            }, status=status.HTTP_400_BAD_REQUEST)
        member=CompanyMember.objects.create(
            company=company,
            user=user,
            role=role
        )
        return Response({
            'message':f'{user.username} added to {company.name}',
            'member':CompanyMemberSerializer(member).data
        },status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.companies.models import Company, CompanyMember
from apps.companies.serializers import (
    CompanySerializer,
    CreateCompanySerializer,
    CompanyMemberSerializer,
    InviteMemberSerializer,
)
from apps.users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_company_view(request):
    if hasattr(request.user, 'company'):
        return Response({
            'error': 'You already have a company registered'
        }, status=status.HTTP_400_BAD_REQUEST)
    serializer = CreateCompanySerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        company = serializer.save()
        request.user.role = 'company_admin'
        request.user.save()
        return Response({
            'message': 'Company created successfully',
            'company': CompanySerializer(company).data,
        }, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company_view(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        return Response({
            'error': 'You do not have a company'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = CompanySerializer(company)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_company_view(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        return Response({
            'error': 'You do not have a company'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = CreateCompanySerializer(
        company,
        data=request.data,
        partial=request.method == 'PATCH',
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Company updated successfully',
            'company': CompanySerializer(company).data,
        })
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_member_view(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        return Response({
            'error': 'You do not have a company'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = InviteMemberSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        role = serializer.validated_data['role']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'No user found with this email'
            }, status=status.HTTP_404_NOT_FOUND)
        if CompanyMember.objects.filter(
            company=company,
            user=user
        ).exists():
            return Response({
                'error': 'User is already a member'
            }, status=status.HTTP_400_BAD_REQUEST)
        member = CompanyMember.objects.create(
            company=company,
            user=user,
            role=role
        )
        return Response({
            'message': f'{user.username} added to {company.name}',
            'member': CompanyMemberSerializer(member).data,
        }, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_members_view(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        return Response({
            'error': 'You do not have a company'
        }, status=status.HTTP_404_NOT_FOUND)
    members = CompanyMember.objects.filter(
        company=company
    ).select_related('user')
    serializer = CompanyMemberSerializer(
        members,
        many=True
    )
    return Response({
        'company': company.name,
        'total_members': members.count(),
        'members': serializer.data,
    })
    

       



    

