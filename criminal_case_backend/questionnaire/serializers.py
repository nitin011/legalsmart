from rest_framework import serializers
from . import models
from criminal_case_backend.users.models import User
from criminal_case_backend.questionnaire.models import Questionnaire, QuesAnswer

class QuestionnaireSerializer(serializers.ModelSerializer):
    option_list = serializers.SerializerMethodField()
    class Meta:
        model = Questionnaire
        fields = ('name', 'is_active', 'option_type', 'option_list')

    def get_option_list(self, obj):
        # options = QuesAnswer.objects.filter(ques_id=obj.id)
        options = obj.option
        options_list = {}
        if options:
            for option in options:
                data = {}
                if obj.option_type==2:
                    data['options'] = list(list(obj.option.split(",")))
                else:
                    # data['options'] = option.answer
                    data['options'] = list(list(obj.option.split(",")))
                options_list.update(data)
        return options_list
