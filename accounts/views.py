from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission


# Droits utilisateurs / Permissions
class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Récupérer toutes les permissions de l'utilisateur
        user_permissions = user.get_all_permissions()
        
        # Récupérer les permissions détaillées
        all_permissions = Permission.objects.filter(codename__in=[
            perm.split('.')[1] for perm in user_permissions
        ]).select_related('content_type')
        
        # Grouper les permissions par modèle
        grouped_permissions = {}
        for perm in all_permissions:
            model = perm.content_type.model  # Le modèle auquel appartient la permission
            if model not in grouped_permissions:
                grouped_permissions[model] = []
            grouped_permissions[model].append(perm.codename)
        
        return Response({
            'username': user.username,
            'permissions_by_model': grouped_permissions,
        })
