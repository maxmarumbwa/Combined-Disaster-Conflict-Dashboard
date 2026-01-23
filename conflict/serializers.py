from rest_framework import serializers
from conflict.models import PoliticalViolenceAdm1Monthly


class PoliticalViolenceAdm1MonthlySerializer(serializers.ModelSerializer):
    province = serializers.CharField(source="province.shapename2", read_only=True)
    province_id = serializers.IntegerField(source="province.id", read_only=True)

    class Meta:
        model = PoliticalViolenceAdm1Monthly
        fields = [
            "province_id",
            "province",
            "year",
            "month",
            "events",
            "fatalities",
        ]
