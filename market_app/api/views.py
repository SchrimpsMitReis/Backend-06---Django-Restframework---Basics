from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, ProductSerializer,  SellerSerializer, MarketHyperlinkedSerializer
from market_app.models import Market, Product, Seller

# ---- Markets -------

@api_view(['GET', 'POST'])
def first_view(request):

    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketHyperlinkedSerializer(markets, many=True, context={'request': request}, fields = ('id', 'name'))
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = MarketSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        # try:
            # msg = request.data['message']
            # return Response({'your_message': msg}, status= status.HTTP_201_CREATED)
        # except:
            # return Response({'your_message': 'error'}, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET','DELETE','PUT'])
def markets_single_view(request, pk): # pk = primarykey (von der DB eingtragene ID)

    if request.method == 'GET':
        market = Market.objects.get(pk = pk)
        serializer = MarketSerializer(market )
        return Response(serializer.data, status= status.HTTP_200_OK)

    if request.method == 'DELETE':
        market = Market.objects.get(pk = pk)
        serializer = MarketSerializer(market)
        market.delete()
        return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
    
    if request.method == 'PUT':
        market = Market.objects.get(pk = pk)
        serializer = MarketSerializer(market, data = request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

        # return Response(serializer.data, status= status.HTTP_200_OK)



#------- Sellers ---------

@api_view(['GET', 'POST'])
def seller_view(request):

    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True, context={'request': request})
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = SellerSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


@api_view()
def seller_single_view(request, pk):
    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    if request.method == 'POST':
        
        serializer = ProductSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#-------Product ----------

# @api_view(['GET', 'POST'])
# def product_view(request):

#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductDetailSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK) 

#     if request.method == 'POST':
#         serializer = ProductCreateSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)
    

# @api_view(['DELETE'])
# def product_delete_view(request,pk):
#     if request.method == 'DELETE':
#         product = Product.objects.get(pk=pk)
#         serializer = ProductDetailSerializer(product)
#         product.delete()
#         return Response(serializer.data, status= status.HTTP_202_ACCEPTED)