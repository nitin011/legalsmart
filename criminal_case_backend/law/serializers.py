from rest_framework import serializers
from . import models
from criminal_case_backend.users.models import User
from criminal_case_backend.law.models import Law, LawCategory, LawInnerCategory

class LawSerializer(serializers.ModelSerializer):

    class Meta:
        model = Law
        fields = ('laws', 'is_active')
        # extra_kwargs = {'password': {'write_only': True} }

class SubLawCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LawInnerCategory
        fields = ('id','name', 'summary_offence','indictable_offence','is_active')
        # exclude = ['name', 'is_active',]

class SubLawSerializer(serializers.ModelSerializer):
    sub_law_category = serializers.SerializerMethodField()
    class Meta:
        model = LawCategory
        fields = ('id','name', 'is_active', 'sub_law_category')

    def get_sub_law_category(self, obj):
        law_inner_category = LawInnerCategory.objects.filter(law=obj.id)
        sub_laws = []
        if law_inner_category:
            for sblaw in law_inner_category:
                sub_law = {}
                if sblaw.is_active:
                    sub_law['id'] = sblaw.id
                    sub_law['name'] = sblaw.name
                    sub_law['description_1'] = sblaw.description_1
                    sub_law['description_2'] = sblaw.description_2
                    sub_law['summary_offence'] = sblaw.summary_offence
                    sub_law['indictable_offence'] = sblaw.indictable_offence
                    sub_law['is_active'] = sblaw.is_active
                    sub_laws.append(sub_law)
        return sub_laws