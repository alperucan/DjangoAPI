from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from aircraft.models import Aircraft
from rest_framework.response import Response
from rest_framework import status
from aircraft.seriliazer import AircraftSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle

# Create your views here.
class AircraftView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, id=None ):
        try:
            if id:
                # Get aircraft with given id
                result = Aircraft.objects.get(id=id)
                serializer = AircraftSerializer(result)
                return Response(
                    {
                        'statusCode': status.HTTP_200_OK,
                        "data": serializer.data
                    }, status=status.HTTP_200_OK
                )
            else:
                # if there is no id, get all data
                result = Aircraft.objects.all()
                ## use paginator for some performance improvement ! 
                paginator = PageNumberPagination()
                paginated_result = paginator.paginate_queryset(result, request)
                serializer = AircraftSerializer(paginated_result, many=True)
                return paginator.get_paginated_response(serializer.data)
            """     totalObjectsCount = result.count()
                serializer = AircraftSerializer(result, many=True)
                return Response(
                    {
                        'statusCode': status.HTTP_200_OK,
                        "totalObjectsCount": totalObjectsCount,
                        "data": serializer.data,
                    }, status=status.HTTP_200_OK
                ) """
        except Aircraft.DoesNotExist:
            # if there is no data with given id send error
            return Response(
                {
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": f"Aircraft with this ID = {id} does not exist."
                }, status=status.HTTP_404_NOT_FOUND
            )






    def post(self,request):

        # Check invalid fields for example {"ex": "3"}
        invalid_fields = [key for key in request.data.keys() if key not in AircraftSerializer.Meta.fields]
        if invalid_fields:
            return Response({
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid fields: {', '.join(invalid_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AircraftSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"statusCode":status.HTTP_201_CREATED,"data":serializer.data} , status=status.HTTP_201_CREATED)
        else:
            return Response({"statusCode": status.HTTP_400_BAD_REQUEST, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, id): 
        try:
            result = Aircraft.objects.get(id=id)
        except:
            return Response({
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": f"Aircraft with this ID = {id} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
    
         
        # Check invalid fields for example {"ex": "3"}
        invalid_fields = [key for key in request.data.keys() if key not in AircraftSerializer.Meta.fields]
        if invalid_fields:
            return Response({
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid fields: {', '.join(invalid_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)


        serializer = AircraftSerializer(result, data=request.data, partial=True)
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
        



    def delete(self, request, id):
        try:
            aircraft = Aircraft.objects.get(id=id)
            aircraft.delete()
            return Response({
                "statusCode": status.HTTP_204_NO_CONTENT,
                "message": f"Aircraft with ID = {id} has been deleted.",
                
            }, status=status.HTTP_204_NO_CONTENT)
        except Aircraft.DoesNotExist:
            return Response({
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": f"Aircraft with this ID = {id} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)