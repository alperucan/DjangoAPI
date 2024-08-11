from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from airline.models import Airline
from airline.seriliazer import AirlineSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle


# Create your views here.

class AirlineView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    paginate_by = 2
    throttle_classes = [UserRateThrottle]

    def get(self, request, id=None ):
        try:
            # if id exist then get object with that id
            if id:
                result = Airline.objects.get(id=id)
                serializers = AirlineSerializer(result)
                return Response(
                    {
                        'statusCode': status.HTTP_200_OK,
                        "data":serializers.data
                    },status=status.HTTP_200_OK)
            # if id does not exist get all objects from db
            result = Airline.objects.all()
            ## use paginator for some performance improvement ! 
            paginator = PageNumberPagination()
            paginated_result = paginator.paginate_queryset(result, request)
            serializer = AirlineSerializer(paginated_result, many=True)
            return paginator.get_paginated_response(serializer.data)
        
            #totalObjectsCount = result.count()
            #serializers = AirlineSerializer(result, many=True)
            """ return Response(
                {
                    'statusCode': status.HTTP_200_OK, 
                    "totalObjectsCount":totalObjectsCount,
                    "data":serializers.data,
                }, status=status.HTTP_200_OK)  
     """
        except Airline.DoesNotExist:
            # if there is no data with given id, send error
            return Response(
                {
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": f"Airline with this ID = {id} does not exist."
                }, status=status.HTTP_404_NOT_FOUND
            )


    def post(self,request):

        # Check invalid fields for example {"ex": "3"}
        invalid_fields = [key for key in request.data.keys() if key not in AirlineSerializer.Meta.fields]
        if invalid_fields:
            return Response({
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid fields: {', '.join(invalid_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = AirlineSerializer(data=request.data)

        if serializer.is_valid():
            if Airline.objects.filter(name=serializer.validated_data.get('name')).exists():
                return Response({
                    "statusCode": status.HTTP_400_BAD_REQUEST, 
                    "message": "Airline with the same name already exists."
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"statusCode":status.HTTP_201_CREATED,"data":serializer.data} , status=status.HTTP_201_CREATED)
        else:
            return Response({"statusCode": status.HTTP_400_BAD_REQUEST, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id): 
        try:
            result = Airline.objects.get(id=id)
        except:
            return Response({
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": f"Airline with this ID = {id} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check invalid fields for example {"ex": "3"}
        invalid_fields = [key for key in request.data.keys() if key not in AirlineSerializer.Meta.fields]
        if invalid_fields:
            return Response({
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid fields: {', '.join(invalid_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = AirlineSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
    ## POST methodtan DELETE methoduna aldim !
    def delete(self, request, id):
        try:
            airline = Airline.objects.get(id=id)
            airline.delete()
            return Response({
                "statusCode": status.HTTP_204_NO_CONTENT,
                "message": f"Airline with ID = {id} has been deleted.",
                
            }, status=status.HTTP_204_NO_CONTENT)
        except Airline.DoesNotExist:
            return Response({
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": f"Airline with this ID = {id} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)