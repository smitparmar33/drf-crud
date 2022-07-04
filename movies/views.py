from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from .models import Movie
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer,MovieNewSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()

class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    filterset_class = MovieFilter
    queryset=Movie.objects.all()
    serializer_class = MovieNewSerializer
    
    #Overiding the method
    breakpoint()
    def retrieve(self, request, *args, **kwargs):
        
        serializer = super(MovieViewSet, self).retrieve(request)
        return Response({'data': serializer.data})

    def list(self, request, *args, **kwargs): #For setting custom response
        print(request.user)
        
        serializer = super(MovieViewSet, self).list(request)
        return Response({'data': serializer.data})


class MovieApiView(APIView):

    serializer_class = MovieNewSerializer

    def get(self, request, *args, **kwargs):

        products = Movie.objects.all()

        serializer = self.serializer_class(products, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data:":serializer.data})




    

