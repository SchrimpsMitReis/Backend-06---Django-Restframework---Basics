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
        fields = ['id', 'name', 'market_ids', 'markets', 'contact_data']

class SellerListSerializer(
    SellerSerializer, 
    serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Seller
        fields = ['id', 'url', 'name', 'market_ids', 'markets', 'contact_data']




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
        fields = ['id', 'name', 'description', 'market_id' , 'seller_id','price', 'markets', 'sellers', 'isBio'] # 'market_id' , 'seller_id',
    
    def create(self, validated_data):
        # """Ermöglicht das korrekte Erstellen des Produktes mit seller_id und market_id"""
        print("Validatet Data", validated_data)
        market = validated_data.pop("markets")
        seller = validated_data.pop("sellers")
        product = Product.objects.create(markets=market, seller=seller, **validated_data)
        return product
