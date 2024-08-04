from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from library_api.models import LibraryModel
from library_api.serializers import LibrarySerializer
import math


class Library(generics.GenericAPIView):
    serializer_class = LibrarySerializer
    queryset = LibraryModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        books = LibraryModel.objects.all()
        total_books = books.count()

        if search_param:
            books = books.filter(title__icontains=search_param)
        serializer = self.serializer_class(books[start_num:end_num], many=True)
        return Response(
            {
                "status": "success",
                "total": total_books,
                "page": page_num,
                "last_page": math.ceil(total_books / limit_num),
                "books": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "book": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LibraryDetail(generics.GenericAPIView):
    queryset = LibraryModel.objects.all()
    serializer_class = LibrarySerializer

    def get_book(self, pk):
        try:
            return LibraryModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        book = self.get_book(pk=pk)
        if book is None:
            return Response(
                {"status": "fail", "message": f"Book with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(book)
        return Response({"status": "success", "book": serializer.data})

    def patch(self, request, pk):
        book = self.get_book(pk)
        if book is None:
            return Response(
                {"status": "fail", "message": f"Book with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "book": serializer.data})
        return Response(
            {"status": "fail", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        book = self.get_book(pk)
        if book is None:
            return Response(
                {"status": "fail", "message": f"Book with Id {id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
