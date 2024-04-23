from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(VendorSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'post':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3