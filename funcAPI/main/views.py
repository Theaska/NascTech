from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import FieldInspector, SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers import MainSerializer, DataSerializer
from main.helper import FuncClass
from main.exceptions import FunctionNotFound


class MultiInspector(FieldInspector):
    """
        Inspector ListField for sending list queries as: ?data=1&data=2 but not ?data=1,2
    """
    def process_result(self, result, method_name, obj, **kwargs):
        if isinstance(obj, serializers.ListField):
            schema = openapi.resolve_ref(result, self.components)
            schema['collectionFormat'] = 'multi'
        return result


class MultiListInspector(SwaggerAutoSchema):
    field_inspectors = [MultiInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS


class MainViewAPI(APIView):
    """
        Main View for taking a sentence of 'rules', match it with functions from the functions.py,
        and append functions to the 'data' list in the same order.
    """
    swagger_schema = MultiListInspector
    serializer_class = MainSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self, *data, **kwargs_data):
        return self.get_serializer_class()(*data, **kwargs_data)

    @swagger_auto_schema(responses={200: DataSerializer()},
                         query_serializer=serializer_class())
    def get(self, request):
        serializer = self.get_serializer(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data)


class MainViewDetail(MainViewAPI):
    """
        Detail view for using the specific function from functions.py
    """
    serializer_class = DataSerializer

    @swagger_auto_schema(query_serializer=DataSerializer())
    def get(self, request, name):
        func_class = FuncClass()

        try:
            func = func_class.get_func(name)
        except FunctionNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data['data']
            return Response({'data': list(map(func, validated_data))})
