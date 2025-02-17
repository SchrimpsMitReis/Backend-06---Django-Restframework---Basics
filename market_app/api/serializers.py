from rest_framework import serializers
from market_app.models import Market, Product, Seller


class MarketSerializer(serializers.ModelSerializer):

    sellers = serializers.StringRelatedField(many = True, read_only = True)

    class Meta:
        model = Market
        fields = '__all__'
  

class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Market
        fields = ['id', 'url', 'name', 'location', 'description', 'net_worth']



class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset = Market.objects.all(),
        many = True,
        write_only = True,
        source = 'markets'
    )
    class Meta:
        model = Seller
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(read_only=True)

    market_id = serializers.PrimaryKeyRelatedField(
        queryset = Market.objects.all(),
        # many = True,
        write_only = True,
        source = 'markets'
    )

    sellers = SellerSerializer(read_only=True)

    seller_id = serializers.PrimaryKeyRelatedField(
        queryset = Seller.objects.all(),
        # many = True,
        write_only = True,
        source = 'sellers'
    )
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'market_id' , 'seller_id','price', 'markets', 'sellers', 'isBio'] #market_id , seller_id
    
    def create(self, validated_data):
        """Ermöglicht das korrekte Erstellen des Produktes mit seller_id und market_id"""
        print("Validatet Data", validated_data)
        market = validated_data.pop("market_id")
        seller = validated_data.pop("seller_id")
        product = Product.objects.create(markets=market, seller=seller, **validated_data)
        return product

# class SellersDetailSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=250)
#     contact_data = serializers.CharField()
#     markets = MarketSerializer(many=True, read_only=True)

# class SellersCreateSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=250)
#     contact_data = serializers.CharField()
#     markets = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())  # Market als ID

#     def validate_markets(self, value):
#         markets = Market.objects.filter(id__in = value)
#         if len(markets) != len(value):
#             serializer = MarketSerializer(markets, many=True)
#             raise serializers.ValidationError(serializer.data)
#         return value
    
#     def create(self, validated_data):
#         market_ids = validated_data.pop('markets')
#         seller = Seller.objects.create(**validated_data)
#         markets = Market.objects.filter(id__in=market_ids)
#         seller.markets.set(markets) 


# class ProductDetailSerializer(serializers.Serializer): #Funktioniert !
#     name = serializers.CharField(max_length=250)
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=50, decimal_places=2)
#     markets = MarketSerializer(many=True, read_only=True)
#     seller = SellerSerializer(read_only=True)
#     isBio = serializers.BooleanField()


# class ProductCreateSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=250)
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=50, decimal_places=2)
#     isBio = serializers.BooleanField()
#     markets = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())  # Market als ID
#     seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())  # Seller als ID

#     def create(self, validated_data):
#         return Product.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.price = validated_data.get('price', instance.price)
#         instance.isBio = validated_data.get('isBio', instance.isBio)
#         instance.markets = validated_data.get('markets', instance.market)
#         instance.seller = validated_data.get('seller', instance.seller)
#         instance.save()
#         return instance