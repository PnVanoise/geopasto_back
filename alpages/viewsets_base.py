from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)


class BaseModelViewSet(ModelViewSet):
    """
    Standardized ModelViewSet with:
    - uniform create/update logging + error handling
    - generic getNextId action for models that use manual integer PKs
    """

    def create(self, request, *args, **kwargs):
        logger.debug(f"BaseModelViewset {self.__class__.__name__} - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.debug(f"BaseModelViewset {self.__class__.__name__} - Created instance: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"BaseModelViewset {self.__class__.__name__} - Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"BaseModelViewset {self.__class__.__name__} - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"BaseModelViewset {self.__class__.__name__} - Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"BaseModelViewset {self.__class__.__name__} - Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='getNextId')
    def get_next_id(self, request):
        """
        Generic next-id endpoint. Only returns a next id when the model uses a
        manual integer PK. Uses DB-side ordering but still not safe under heavy concurrency—
        prefer migrating to AutoField/BigAutoField or UUIDs.
        """
        try:
            qs = self.get_queryset().order_by(self.get_pk_field_name())
        except Exception:
            logger.warning(f"BaseModelViewset {self.__class__.__name__} - Error occurred while fetching queryset for next ID")
            return Response({'next_id': None})
        last = qs.last()
        if not last:
            return Response({'next_id': 1})
        pk_name = self.get_pk_field_name()
        last_val = getattr(last, pk_name, None)
        try:
            next_id = int(last_val) + 1
        except Exception:
            logger.warning(f"BaseModelViewset {self.__class__.__name__} - Error occurred while calculating next ID")
            return Response({'next_id': None})
        return Response({'next_id': next_id})

    def get_pk_field_name(self):
        # model PK attribute name (e.g. 'id', 'id_unite_pastorale', ...)
        return self.get_queryset().model._meta.pk.name
