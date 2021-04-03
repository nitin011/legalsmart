# -*- coding: utf-8 -*-
# # Third Party Stuff
from rest_framework import mixins, viewsets,  status
from . import models, serializers
from rest_framework.decorators import list_route, detail_route
from .models import Questionnaire
from criminal_case_backend.questionnaire.serializers import QuestionnaireSerializer
from criminal_case_backend.base import response
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
import string
import random
from rest_framework.views import APIView
from .models import Questionnaire, Age, QuesAnswer, QuestionnaireType, UserResponse, Ticket, ChallangeTicket
from criminal_case_backend.users.models import User, WiPayPayment
from django.db.models import Q
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail

class QuestionnaireViewSet(APIView):

	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		ques_type = self.request.query_params.get('type')
		inner_law_id = self.request.query_params.get('inner_law_id')
		print("inner_law_id ", inner_law_id)

		print(ques_type)
		if not ques_type:
			return Response({'status':False,'msg': "This method is not allowed."}, status=status.HTTP_404_NOT_FOUND)
		ques_data = models.Questionnaire.objects.filter(ques_type=ques_type,law_inner_category=inner_law_id)
		print(len(ques_data))
		serializer = []
		if ques_data:
			for ques in ques_data:
				# if ques.is_dropdown:
				# 	print("is_dropdown here")
				# 	serializer = QuestionnaireSerializer(ques_data, many=True)
				# else:
				# 	print("hello dd")
				serializer = QuestionnaireSerializer(ques_data, many=True)
		if serializer:
			return Response({'status':True, 'data':serializer.data}, status=status.HTTP_200_OK)
		else:
			return Response({'status':False,'msg': "Please contact Administrator to add content."}, status=status.HTTP_404_NOT_FOUND)

	def post(self, request):
		data = request.data
		answer_json = data.get("answer_json",None)
		user_id = data.get('user_id',None)
		device_id = data.get('device_id',None)
		answer = QuesAnswer.objects.filter(device_id=device_id).first()
		if answer:
			# answer = QuesAnswer()
			answer.answer = answer_json
			answer.user_id = user_id
			answer.device_id = device_id
			answer.save()
			return Response({'status':True,'msg': "Response is Updated."}, status=status.HTTP_200_OK)
		else:
			answer_obj = QuesAnswer()
			answer_obj.answer = answer_json
			answer_obj.user_id = user_id
			answer_obj.device_id = device_id
			answer_obj.save()
			return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)

import datetime

now = datetime.datetime.now()
class NeedAttorneyViewSet(APIView):

	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		# ques_type = self.request.query_params.get('type')
		print(request)
		data ={ 'user': 'FROM “'+request.user.name.capitalize()+'”'} 
		data['details'] = 'MY NAME IS  '+request.user.name.capitalize()+' MY CONTACT INFORMATION IS '+request.user.mobile+' I NEED AN ATTORNEY IN TRINIDAD AND TOBAGO TO REPRESENT ME IN COURT FOR A CRIMINAL MATTER. MY COURT DATE IS SET FOR '+str(now)+'. '
		data['notes'] = 'THIS WILL BE A NOTIFICATION SENT TO EVERYONE REGISTERED ON THE APP AS AN ATTORNEY WITH THEIR SPECIALIZATION AS CRIMINAL.'
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)

class NotGuiltyViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['details'] = 'You have selected NOT GUILTY, regarding the offence of “Injuring Someone with or without a weapon”.'
		data['notes'] = 'AT THIS STAGE, LEGAL SMART RECCOMENDS THAT YOU SEEK LEGAL PROFESSIONAL ADVICE FROM AN ATTORNEY BASED IN TRINIDAD AND TOBAGO.'
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)
	
class HighCourtViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['details'] = 'The accused has selected to have this matter heard in the HIGH COURT or the ASSIZES.A date will need to be assigned for the hearing.'
		data['notes'] = 'TIP: LEGAL SMART HIGHLY RECOMMENDS THAT ANY MATTER THAT IS TO BE TRIED IN THE HIGH COURT MUST ENGAGE WITH AN ATTORNEY FOR COURT REPRESENTATION.'
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)

class Trial_ChoiceViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] = 'ON FEBRUARY 1ST 2019, SECTION 2 OF THE MISCELLANEOUS PROVISIONS (TRIAL BY JUDGE ALONE) Act 2017 EFFECTIVELY GRANTS A PERSON A CHOICE BETWEEN'
		data['detail2'] = ['HAVING A JUDGE ALONE TRIAL','A TRIAL WITH A JURY']
		data['notes'] = 'TIP: PLEASE DISCUSS WITH YOUR ATTORNEY, WHAT IS THE MOST FAVOURABLE OPTION FOR A TRIAL BASED ON THE OFFENCE THE ACCUSED IS CHARGED.'
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)


class Judge_Alone_TrialViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] = 'In a judge alone trial, the accused will be in the HIGH COURT, and all evidence/disclosure and cross examination by your attorney will be heard by the Judge ALONE.'
		data['detail2'] = 'In a JUDGE ALONE TRIAL, the judge has a discretion to discount prison time or not to discount prison time based on the evidence presented in court, the accounts of witnesses in cross examination by both the defence and prosecution, the history of the accused and the seriousness of the incident.'
		data['notes'] = 'The JUDGE MUST follow MANDATORY jail time Discounts, before passing sentence.'
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)
	
class Magistrate_CourtViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] = 'I DO NOT KNOW \n SEEMS LIKE YOU ARE UNSURE OF WHAT COURT TO SELECT.\n HERE IS SOME INFORMATION THAT MAY HELP YOU MAKE A DECISION.'
		data['detail2'] = 'If one chooses to remain in the MAGISTRATES COURT, the matter will be heard before the Magistrate before you. The accused will be read the fact of the alleged assault and the arrest as well as any evidence relevant at this time. The accused can correct any errors by adding or explaining the difference in the facts read. The Magistrate will ask how the accused wishes to plead. The plead will be entered and the Magistrate will pass sentence if the plead is guilty, after questions are asked. '
		data['notes'] = 'THIS IS A QUICKER PROCESS.\n If one chooses to fo to the High Court, a date will need to be selected for the matter to be heard in High Court. This may take some time and you may require BAIL. The accused can be heard by a judge alone or by a jury. If you have a matter that need to be in the High Court, Legal Smart recommends you retain an Attorney to represent you.'
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)

class To_JurrorsViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] = 'I DO NOT KNOW'
		data['detail2'] = 'If one chooses'
		data['notes'] = ''
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)

class Trial_By_JuryViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] = 'If the penalty for the offence is death by hanging, then 12 jurors are required.'
		data['detail2'] = 'For all other cases, 9 jurors are required and the Judge has a discretion to select a MAXIMUM of 6 alternate Jurors.'
		data['notes'] = 'LEGAL SMART APP can assist the user to get a consensus as to what type of verdict jurors may hand down.'
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)

class SentenceViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] =  '1. Maximum sentence is 5 years in prison\
							2. DEDUCTIONS of 1/3 if guilty plea and/or time spent in remand'
		data['detail2'] = 'OR 3. Additional time off for mitigating and aggravating factors'
		data['notes'] = ''
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)	

class Tip_InformationViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] = 'Sentencing method is as followed:'
		data['detail2'] =  '1. Starting point calculation of the offence by statue or by degree and gravity of offence.\
							2. Upward adjustment for the good things about the offender and downward adjustment for the bad things about the offender.\
							3. A one third discount of the jail time will be given at the earliest possible guilty plead.\
							4. Discount of Jail time based on the time spent in pre-trial custody or remand.'
		data['notes'] = ''
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)

class HighcourtQuestionsViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		data = {}
		data['detail1'] = 'Sentencing method is as followed:'
		data['detail2'] =  '1. Starting point calculation of the offence by statue or by degree and gravity of offence.\
							2. Upward adjustment for the good things about the offender and downward adjustment for the bad things about the offender.\
							3. A one third discount of the jail time will be given at the earliest possible guilty plead.\
							4. Discount of Jail time based on the time spent in pre-trial custody or remand.'
		data['notes'] = ''
		return Response({'status':True,'msg': "success.", 'data':data}, status=status.HTTP_200_OK)

class FCMViewSet(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		print("Ethe")
		from pyfcm import FCMNotification
 
		push_service = FCMNotification(api_key="AIzaSyAkREAA2RUQ9JhNbdiNxrncGqm6UaIodzA")
		 
		# OR initialize with proxies
		 
		# proxy_dict = {
		#           "http"  : "http://127.0.0.1",
		#           "https" : "http://127.0.0.1",
		#         }
		# push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)
		 
		# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
		 
		# registration_id = "854fab61-1717-45e1-8be5-48481cafd5d3"
		registration_ids = ['fdfda6eb-0943-4316-a1c1-8a9809b6a166','d9e51ced-ac0d-4720-a433-01641821e7a5','b24c5799-3135-41c5-9d81-4348e06532e6','9dc91ce8-9eeb-414f-8025-c8c72d4a968d','854fab61-1717-45e1-8be5-48481cafd5d3','7d63a78f-961f-47c0-8253-5e8254923bea','668cb329-1e23-4453-b9fc-44e2709e0ed1','57e21654-9368-4731-887f-5df336472f03','2ab93b45-aed6-4c31-aa9c-0fe8b6f6e930'
'161f2d43-0294-4c03-a289-a31f556068bf']
		message_title = "Uber update"
		message_body = "Hi john, your customized news for today is ready"
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
		# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
		 
		print (result)
		 
		# Send to multiple devices by passing a list of ids.
		# registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
		# message_title = "Uber update"
		# message_body = "Hope you're having fun this weekend, don't forget to check today's news"
		# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
		 
		# print result


		return Response({'status':True,'msg': "success.", 'data':'data'}, status=status.HTTP_200_OK)


class NeedLawyerSet(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		data = request.data
		print (request.user.pk)
		print (data)
		print("=======================")
		name = data.get("name",None)
		response_for = data.get('response_for',None)
		contact_info = data.get('contact_info',None)
		date = data.get('date',None)
		device_id = data.get('device_id',None)
		option = data.get('option',None)
		offence = data.get('offence',None)
		appearance = data.get('appearance',None)
		users = User.objects.filter(Q(role='Judge') | Q(role='Attorney')) #attorney
		registration_ids = [user.fcm_token for user in users if user.fcm_token]
		emails = [user.email for user in users if user.email]
		print("registration_ids")
		print(registration_ids)
		if device_id:
			# response = UserResponse.objects.filter(device_id=device_id).first()
			# if response:
			# 	# answer = UserResponse()
			# 	response.name = name
			# 	response.response_for = response_for
			# 	response.device_id = device_id
			# 	response.contact_info = contact_info
			# 	response.date = date
			# 	response.option = option
			# 	response.offence = offence
			# 	response.appearance = appearance
			# 	response.user = request.user
			# 	response.save()

			# 	# return Response({'status':True,'msg': "Response is Updated."}, status=status.HTTP_200_OK)
			# else:
				# if device_id:

			response_obj = UserResponse()
			response_obj.name = name
			response_obj.response_for = response_for
			response_obj.device_id = device_id
			response_obj.contact_info = contact_info
			response_obj.date = date
			response_obj.option = option
			response_obj.offence = offence
			response_obj.appearance = appearance
			response_obj.user = request.user
			response_obj.save()

				
			# FCM Notifications
			from pyfcm import FCMNotification
			print("here")
			try:
				# push_service = FCMNotification(api_key="AIzaSyAkREAA2RUQ9JhNbdiNxrncGqm6UaIodzA")
				# push_service1 = FCMNotification(api_key="3f863a488f718795e1e3bbf54a85fa1c473d7a40")

				# push_service = FCMNotification(api_key="AAAAIKrmm0o:APA91bFd3-Pt4HuykGYPcorgIZDXyUNClmHtvurJQ0j4hGdhN1Ct8JzIMMpZxNJ3Iw1GJhzGlDM917XJqCVCa-2y3LTp_3TUeZByIAIHs_o_Tl0IItACkuAvhW2DXvgEIYmqWv5IwDDq")
				
				push_service = FCMNotification(api_key="AAAAP7tX290:APA91bFfwFuShQwi2k2sr8p1rhQKMZpZ-VbU-F6QEw3nglsfe1tAHvXB_DSfAEXKWtcKYnTgxMKZh2o-cgdjBdk_F_u_4Cdz2Lv8_LuHTrs91cy3T17CiLr3kIjnhlbdHzwoaHzgtZpe")
				
				

				# registration_ids = "854fab61-1717-45e1-8be5-48481cafd5d3"
				# '0fe2f181ad69b9bf',
				# 3f863a488f718795e1e3bbf54a85fa1c473d7a40
				# registration_ids = ['de121391ffaacb2e']
				# registration_ids = ['3f863a488f718795e1e3bbf54a85fa1c473d7a40']
				print("here3")
				print("push >> " , push_service)
				# registration_ids = ['fQqXACOWRUS3bx3uDUh-t5:APA91bFXmHrimaBY1P8BoITPuSOHxBTruVu5nYD2G9t1tD-7Y69xipYkxqXmYoadKgUdAYwEx4X_Q5kBkO9QIwC2Z_s-v3aU96Rg0tYGFR4QkfWIoiQ9p08IW0KynDxqSdPKlBQTzuZA', 'fXxqKkpDRMOABO7JCPp21K:APA91bEUlhnxhXFNjYt2nq8twcuoPpJ4HjrQIVRY9e88V4vC6y4tSgYvgmwHBpLAh6dPUoO_rHRRc9PyU8rS1DwAmbRTgOyTj6Bjfe77Tkpw8v4XV7881RC9sxUmpHMUMyc1xLNtlbKZ']
				# print("push1 >> ", push_service1)
				message_title = "You have received notification"
				message_body = "You have received notification from " +str(name)+ ",  Kindly check the Legal Smart App to Accept or Reject the Request. Thank you"
				# result = push_service1.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
				result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
				# result1 = push_service1.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
				print ("result  >> " ,result)
				# print ("result1 >> " ,result1)
				for eml in emails:
					send_mail("Notification from Legal Smart", message_body, "smart_law@yopmail.com", [eml], fail_silently=False,)
					print("Email Sent 4")
			except Exception as e:
				print(e)
				return Response({'status':False,'msg': "Error in sending notifications."}, status=status.HTTP_200_OK)
			print("here4")
			return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)
		else:
			return Response({'status':False,'msg': "Device id is not there."}, status=status.HTTP_200_OK)


class NeedBailSet(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		data = request.data
		adata = request.data
		name = data.get("name",None)
		response_for = data.get('response_for',None)
		contact_info = data.get('contact_info',None)
		date = data.get('date',None)
		device_id = data.get('device_id',None)
		response = UserResponse.objects.filter(device_id=device_id).first()
		if response:
			# answer = UserResponse()
			response.name = name
			response.response_for = response_for
			response.device_id = device_id
			response.contact_info = contact_info
			response.date = date
			response.save()
			return Response({'status':True,'msg': "Response is Updated."}, status=status.HTTP_200_OK)
		else:
			response_obj = UserResponse()
			response_obj.name = name
			response_obj.response_for = response_for
			response_obj.device_id = device_id
			response_obj.contact_info = contact_info
			response_obj.date = date
			response_obj.save()
			return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)

class GetResponseViewSet(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		print("===========================>>>>>>>>>>>>>>>>>>>")
		response = UserResponse.objects.filter(Q(user__role='End User') | Q(user__role='user') | Q(user__role='VIP User') | Q(user__role='User')).order_by('-created_at')
		print("response >>> ", response)
		challenge_res = ChallangeTicket.objects.filter(Q(user__role='End User') | Q(user__role='user') | Q(user__role='VIP User') | Q(user__role='User')).order_by('-created_at')
		data = []
		challange = []
		if response or challenge_res:
			response = response.filter((Q(lawyer=request.user) & Q(status=1))  | Q(status=''))
			# print(response)
			# response = response.filter(lawyer=request.user)
			print("****************************")

			for chlng in challenge_res:
				c = {}
				c['id'] = chlng.id 
				c['rep_status'] = chlng.rep_status 
				c['rep_deadline'] = chlng.rep_deadline
				c['notice_ref_number'] = chlng.notice_ref_number
				c['vehicle_reg_number'] = chlng.vehicle_reg_number
				c['driver_permit_number'] = chlng.driver_permit_number
				c['notice_issue'] = chlng.notice_issue
				c['reason'] = chlng.reason
				c['accepted_by_name'] = chlng.accepted_by_name
				c['accepted_by_contact'] = chlng.accepted_by_contact
				ticket = Ticket.objects.filter(Q(user=chlng.user)).first()
				c['ticket_url'] =  ""
				c['permit'] =  ""

				c['file_url'] =  ""
				if ticket:
					print(ticket)
					c['ticket_url'] =  ticket.ticket_url
					c['permit'] =  ticket.permit
								
				if chlng.file_url:
					c['file_url'] =  chlng.file_url

				c['name'] = ""
				if chlng.name:
					c['name'] = chlng.name

				c['challange_ticket'] = ""
				if chlng.challange_ticket:
					c['challange_ticket'] = chlng.challange_ticket

				c['deadline_comingup'] = ""
				if chlng.deadline_comingup:
					c['deadline_comingup'] = chlng.deadline_comingup
				challange.append(c)
				
			for res in response:
				# print(res.name)
				# print(res.lawyer)
				# print(request.user)
				
				if res.status != "0" or res.lawyer!=request.user:
					print("here")
					d = {}
					d['id'] = res.id
					d['name'] = res.name
					d['response_for'] = res.response_for
					d['device_id'] = res.device_id
					d['contact_info'] = res.contact_info
					d['date'] =  ""
					if res.date:
						d['date'] = res.date

					d['option'] = res.option
					d['offence'] = res.offence
					d['appearance'] = res.appearance
					if res.status == "1":
						d['status'] = 1
					elif res.status == "0":
						d['status'] = 0
					else:
						d['status'] = 3
					
					if res.contact_info:
						contact = res.contact_info
					else:
						contact = ''

					if res.needed_for_law:
						print("\n\n\n\n\n\n")
						print("chupo")
						d['needed_for_law'] = res.needed_for_law
						d['device_id'] = res.device_id
						d['contact_info'] = res.contact_info
						d['needed_for_options'] = res.needed_for_options

					# d['details'] = 'MY NAME IS  '+str(res.name.capitalize())+' I NEED AN ATTORNEY IN TRINIDAD AND TOBAGO TO REPRESENT ME IN COURT FOR A '+ str(res.response_for)+' matter.'
					d['details'] = 'MY NAME IS  '+str(res.name.capitalize())+' I NEED AN ATTORNEY IN TRINIDAD AND TOBAGO TO REPRESENT ME IN COURT FOR A Criminal matter.'
					if str(res.response_for) == "Need a Lawyer":
						d['details'] = 'MY NAME IS  '+str(res.name.capitalize())+' I NEED AN ATTORNEY IN TRINIDAD AND TOBAGO TO REPRESENT ME IN COURT FOR A Criminal matter. MY COURT DATE IS SET FOR '+str(res.date)+'. '
					# data['notes'] = 'THIS WILL BE A NOTIFICATION SENT TO EVERYONE REGISTERED ON THE APP AS AN ATTORNEY WITH THEIR SPECIALIZATION AS CRIMINAL.'
					data.append(d)
			# print(" response => ", data)
			return Response({'status':True,'msg': "response.",'data':data, "challenge_tickets" : challange}, status=status.HTTP_200_OK)
		else:
			return Response({'status':True,'msg': "Response is empty.",'data':data, "challenge_tickets" : challange}, status=status.HTTP_200_OK)

class TicketPayViewSet(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		data = request.data
		info = data.get("info",None)
		paypalConfirm = data.get("paypalConfirm",None)
		totalAmountRecieved = data.get("totalAmountRecieved",None)
		orderId = data.get("orderId",None)
		# res_id = data.get("phone_number",None)
		# user_type = data.get("amount",None)
		# data['option'] = user_res_data.option
		# print(info)
		print (request.data)
		print (request.user.pk)
		# import json 
		# res = json.loads(info[0]) 
		# print(res)
		if info:
			for pay_user in info:
				# print(pay_user)
				print(pay_user['idUrl'])
				print("hello I am here")
				print(pay_user['ticketurl'])
				# exit()
				tick = Ticket()
				tick.ticket_order_id = orderId
				tick.name = pay_user['name']
				tick.email = pay_user['email']
				tick.phone_number = pay_user['phoneNumber']
				tick.amount  = pay_user['ticketAmount']
				
				pay_user['idUrl'] = ""
				if pay_user['idUrl']:
					tick.idUrl  = pay_user['idUrl']
				
				tick.ticket_url = ""
				if pay_user['ticketurl']:
					tick.ticket_url = pay_user['ticketurl']
				tick.challenge_status = pay_user['challengeStatus']

				tick.permit = ""
				if pay_user['permit']:
					tick.permit = pay_user['permit']
				tick.total_amount = pay_user['totalAmount']
				tick.total_amount_USD = pay_user['totalAmountUSD']
				tick.ticket_status = 1
				tick.user = request.user
				tick.save()
			return Response({'status':True,'msg': "Response saved successfully"})
		else:
			return Response({'status':True,'msg': "Response is empty."})
			# return Response({'status':False,'msg': "Name is required"}, status=status.HTTP_404_NOT_FOUND)


class TicketPayFilesViewSet(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		data = request.data
		file_ticket = request.FILES.get('file_ticket')
		file_id = request.FILES.get('file_id')
		permit = request.FILES.get('permit')
		is_image = data.get("is_image",None)
		
		print(is_image)
		print("======================>>>>>")

		# mediaTpye = file_ticket.content_type.split('/')[0]
		directory_file_ticket = settings.MEDIA_ROOT + "/tickets"
		directory_file_id = settings.MEDIA_ROOT + "/ids"
		directory_permit = settings.MEDIA_ROOT + "/permits"
		
		file_ticket_url = ''
		file_id_url = ''
		permit_url = ''

		if is_image == "ticket":
			if file_ticket:
				# Storing file for Tickets
				file_ticket_name = file_ticket.name
				fs = FileSystemStorage()
				fs.base_location = directory_file_ticket
				filename = fs.save(file_ticket_name, file_ticket)

				file_ticket_url = "http://3.133.98.231:8000/media/tickets/"+ str(filename)
		
		if file_id:
			# Storing file for ids
			file_id_name = file_ticket.name
			fs = FileSystemStorage()
			fs.base_location = directory_file_id
			id_filename = fs.save(file_id_name, file_id)
			file_id_url = "http://3.133.98.231:8000/media/ids/"+ str(id_filename)
		
		if is_image == "permit":
			if directory_permit:
				# Storing file for ids
				permit_name = permit.name
				fs = FileSystemStorage()
				fs.base_location = directory_permit
				permit_filename = fs.save(permit_name, permit)
				permit_url = "http://3.133.98.231:8000/media/permits/"+ str(permit_filename)
					
		return Response({'status':True, 'file_ticket_path':file_ticket_url, 'file_id_path':file_id_url,'permit_url':permit_url,'msg':''})
		# size = file._size
		# print(size)
		# destination = open(directory+'/%s'%file_name, 'wb+')

		# for chunk in file.chunks():
		#     destination.write(chunk)

		# destination.close()



		# for file in request.FILES.getlist('file'):
		# 	print(file)
		# 	file_type = file.content_type.split('/')[0]
		# 	file_ext = file.name.split('.')[-1] 
		# 	file_name = file.name
		# 	size = file.size/1024
		# try:
		# 	print("here")
		# 	file = request.data['file']
		# 	file1 = request.FILES.get('file')
		# 	print(file1)
		# except KeyError:
		# 	raise ParseError('Request has no resource file attached')

		# print(file)
		return Response({'status':True})
		# data = request.data
		# file = data.get("file",None)
		# print("file >>>> ")
		# print(file)
		# print("file >>>> ")
		# return Response({'status':True,'msg': "Response saved successfully"})
		# else:
		# 	return Response({'status':True,'msg': "Response is empty."})
		# 	# return Response({'status':False,'msg': "Name is required"}, status=status.HTTP_404_NOT_FOUND)

class NeedLawyerForViewSet(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		# response = UserResponse.objects.filter(Q(needed_for_law='civil') | Q(needed_for_law='family') | Q(user__role='End User') | Q(user__role='user') | Q(user__role='VIP User') | Q(user__role='User'))
		response = UserResponse.objects.filter(Q(needed_for_law='civil') | Q(needed_for_law='family') )
		print("===================")
		print(response)
		data = []
		if response:
			# response = response.filter(Q(status=1)|Q(status=3))
			# response = response.filter(lawyer=request.user)
			for res in response:
				d = {}
				d['id'] = res.id
				d['name'] = res.name
				d['needed_for_law'] = res.needed_for_law
				d['device_id'] = res.device_id
				d['contact_info'] = res.contact_info
				d['needed_for_options'] = res.needed_for_options
				# d['option'] = res.option
				# d['offence'] = res.offence
				# d['appearance'] = res.appearance
				# if res.status == "1":
				# 	d['status'] = 1
				# elif res.status == "0":
				# 	d['status'] = 0
				# else:
				# 	d['status'] = 3
				
				# if res.contact_info:
				# 	contact = res.contact_info
				# else:
				# 	contact = ''
				# d['details'] = 'MY NAME IS  '+str(res.name.capitalize())+' MY CONTACT INFORMATION IS '+str(contact)+' I NEED AN ATTORNEY IN TRINIDAD AND TOBAGO TO REPRESENT ME IN COURT FOR A CRIMINAL MATTER. MY COURT DATE IS SET FOR '+str(res.date)+'. '
				# data['notes'] = 'THIS WILL BE A NOTIFICATION SENT TO EVERYONE REGISTERED ON THE APP AS AN ATTORNEY WITH THEIR SPECIALIZATION AS CRIMINAL.'
				data.append(d)
			# print(" response => ", data)
			return Response({'status':True,'msg': "response.", 'data':data}, status=status.HTTP_200_OK)
		else:
			return Response({'status':True,'msg': "Response is empty.",'data':data}, status=status.HTTP_200_OK)

	def post(self, request):
		data = request.data
		print (request.user.pk)
		print (data)
		print("=======================")
		name = data.get("name",None)
		needed_for_law = data.get('needed_for_law',None)
		response_for = data.get('response_for',None)
		needed_for_options = data.get('needed_for_options',None)
		contact_info = data.get('contact_info',None)
		device_id = data.get('device_id',None)
		is_authorise_check = data.get('is_authorise_check',None)
		is_age_check = data.get('is_age_check',None)
		
		# date = data.get('date',None)
		# option = data.get('option',None)
		# offence = data.get('offence',None)
		# appearance = data.get('appearance',None)
		
		users = User.objects.filter(Q(role='Judge') | Q(role='Attorney')) #attorney
		registration_ids = [user.fcm_token for user in users if user.fcm_token]
		emails = [user.email for user in users if user.email]
		print("registration_ids")
		print(registration_ids)
		print(is_authorise_check)
		if device_id:
			# response = UserResponse.objects.filter(device_id=device_id).first()
			# if response:
			# 	# answer = UserResponse()
			# 	response.name = name
			# 	response.needed_for_law = needed_for_law
			# 	response.device_id = device_id
			# 	response.contact_info = contact_info
			# 	response.needed_for_options = needed_for_options
			# 	# response.option = option
			# 	# response.offence = offence
			# 	# response.appearance = appearance
			# 	response.user = request.user
			# 	response.is_authorise_check = is_authorise_check
			# 	response.is_age_check = is_age_check
			# 	response.save()

			# 	# return Response({'status':True,'msg': "Response is Updated."}, status=status.HTTP_200_OK)
			# else:
				# if device_id:
			response_obj = UserResponse()
			response_obj.name = name
			response_obj.needed_for_law = needed_for_law
			response_obj.device_id = device_id
			response_obj.contact_info = contact_info
			response_obj.needed_for_options = needed_for_options
			response_obj.response_for = response_for
			# response_obj.date = date
			# response_obj.offence = offence
			# response_obj.appearance = appearance
			response_obj.user = request.user

			response_obj.is_authorise_check = is_authorise_check
			response_obj.is_age_check = is_age_check
			response_obj.save()

				
			# FCM Notifications
			from pyfcm import FCMNotification
			print("here")
			try:
				push_service = FCMNotification(api_key="AAAAP7tX290:APA91bFfwFuShQwi2k2sr8p1rhQKMZpZ-VbU-F6QEw3nglsfe1tAHvXB_DSfAEXKWtcKYnTgxMKZh2o-cgdjBdk_F_u_4Cdz2Lv8_LuHTrs91cy3T17CiLr3kIjnhlbdHzwoaHzgtZpe")
				message_title = "You have received notification"
				# message_body = "You have received notification, Kindly check your profile to accept the request"
				message_body = "You have received notification from "+ str(name)+ ",  Kindly check the Legal Smart App to Accept or Reject the Request. Thank you"
				for eml in emails:
					send_mail("Notification from Legal Smart", message_body, "smart_law@yopmail.com", [eml], fail_silently=False,)
					print("Email Sent 4")
				result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
				print(result)
			except Exception as e:
				print(e)
				pass
				# return Response({'status':False,'msg': "User has no FCM Token so geting error in sending notifications."}, status=status.HTTP_200_OK)
			return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)
		else:
			return Response({'status':False,'msg': "Device id is not there."}, status=status.HTTP_200_OK)



# I, "name of attorney (Attorney at Law)", received your Request on “Legal Smart”.  My number is "xxx-xxxx" please contact me. At that time we will discuss my consultation fee, and schedule an appointment date when we can meet to discuss your matter in detail and any further fees associated with representation in Court. Thank you.

class AttorneyResponseViewSet(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		data = request.data
		print (request.user.pk)
		print (data)
		print("=======================")
		name = data.get("name",None)
		contact_info = data.get('contact_info',None)
		device_id = data.get('device_id',None)
		
		users = User.objects.filter(Q(role='Judge') | Q(role='Attorney')) #attorney
		registration_ids = [user.fcm_token for user in users if user.fcm_token]
		print("registration_ids")
		print(registration_ids)
		if device_id:
			response = UserResponse.objects.filter(device_id=device_id).first()
			if response:
				# answer = UserResponse()
				response.name = name
				response.needed_for_law = needed_for_law
				response.device_id = device_id
				response.contact_info = contact_info
				response.needed_for_options = needed_for_options
				# response.option = option
				# response.offence = offence
				# response.appearance = appearance
				response.user = request.user
				response.save()

				# return Response({'status':True,'msg': "Response is Updated."}, status=status.HTTP_200_OK)
			else:
				# if device_id:
				response_obj = UserResponse()
				response_obj.name = name
				response_obj.needed_for_law = needed_for_law
				response_obj.device_id = device_id
				response_obj.contact_info = contact_info
				response_obj.needed_for_options = needed_for_options
				# response_obj.date = date
				# response_obj.offence = offence
				# response_obj.appearance = appearance
				response_obj.user = request.user
				response_obj.save()

				
			# FCM Notifications
			from pyfcm import FCMNotification
			print("here")
			try:
				push_service = FCMNotification(api_key="AAAAP7tX290:APA91bFfwFuShQwi2k2sr8p1rhQKMZpZ-VbU-F6QEw3nglsfe1tAHvXB_DSfAEXKWtcKYnTgxMKZh2o-cgdjBdk_F_u_4Cdz2Lv8_LuHTrs91cy3T17CiLr3kIjnhlbdHzwoaHzgtZpe")
				message_title = "You have received notification"
				message_body = "You have received notification, Kindly check your profile to accept the request"
				# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
			except Exception as e:
				return Response({'status':False,'msg': "Error in sending notifications."}, status=status.HTTP_200_OK)
			return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)
		else:
			return Response({'status':False,'msg': "Device id is not there."}, status=status.HTTP_200_OK)


class ChallengeTicketViewSet(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		data = request.data
		print("=======================")
		rep_status = data.get("rep_status",None)
		rep_deadline = data.get('rep_deadline',None)
		notice_ref_number = data.get('notice_ref_number',None)
		vehicle_reg_number = data.get('vehicle_reg_number',None)
		driver_permit_number = data.get('driver_permit_number',None)
		notice_issue = data.get('notice_issue',None)
		reason = data.get('reason',None)
		device_id = data.get('device_id',None)
		deadline_comingup = data.get('deadline_comingup',None)
		challange_ticket = data.get('challange_ticket',None)
		file_url = data.get('file_url',None)
		name = data.get('name',None)

		if device_id:
			# chlge_ticket = ChallangeTicket.objects.filter(device_id=device_id).first()
			# if chlge_ticket:
				# answer = UserResponse()
			print("dsadjaghdjas")
			chlge_ticket = ChallangeTicket()
			print(chlge_ticket)
			print("dsadjaghdjadwadasdsas")
			print("USer >>>   ", request.user)
			chlge_ticket.rep_status = rep_status
			chlge_ticket.rep_deadline = rep_deadline
			chlge_ticket.notice_ref_number = notice_ref_number
			chlge_ticket.vehicle_reg_number = vehicle_reg_number
			chlge_ticket.driver_permit_number = driver_permit_number
			chlge_ticket.notice_issue = notice_issue
			chlge_ticket.reason = reason
			chlge_ticket.user = request.user
			chlge_ticket.deadline_comingup = deadline_comingup
			chlge_ticket.challange_ticket = challange_ticket
			chlge_ticket.name = name
			chlge_ticket.file_url = file_url
			chlge_ticket.save()

			# 	# return Response({'status':True,'msg': "Response is Updated."}, status=status.HTTP_200_OK)
			# else:
			# 	# if device_id:
			# 	response_obj = UserResponse()
			# 	response_obj.name = name
			# 	response_obj.needed_for_law = needed_for_law
			# 	response_obj.device_id = device_id
			# 	response_obj.contact_info = contact_info
			# 	response_obj.needed_for_options = needed_for_options
			# 	# response_obj.date = date
			# 	# response_obj.offence = offence
			# 	# response_obj.appearance = appearance
			# 	response_obj.user = request.user
			# 	response_obj.save()

				
			# # FCM Notifications
			# from pyfcm import FCMNotification
			# print("here")
			# try:
			# 	push_service = FCMNotification(api_key="AAAAP7tX290:APA91bFfwFuShQwi2k2sr8p1rhQKMZpZ-VbU-F6QEw3nglsfe1tAHvXB_DSfAEXKWtcKYnTgxMKZh2o-cgdjBdk_F_u_4Cdz2Lv8_LuHTrs91cy3T17CiLr3kIjnhlbdHzwoaHzgtZpe")
			# 	message_title = "You have received notification"
			# 	message_body = "You have received notification, Kindly check your profile to accept the request"
			# 	# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
			# except Exception as e:
			# 	return Response({'status':False,'msg': "Error in sending notifications."}, status=status.HTTP_200_OK)
			print(request.user)
			usrs = User.objects.filter(Q(role='Attorney')) #attorney
			message_title = "You have received notification"
			for usr in usrs:
				message_body = "You have received notification from "+ str(name)+ ",  Kindly check the Legal Smart App to Accept or Reject the Request. Thank you"
				send_mail("Notification from Legal Smart", message_body, "smart_law@yopmail.com", [usr.email], fail_silently=False,)
			return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)
		else:
			return Response({'status':False,'msg': "Device id is not there."}, status=status.HTTP_200_OK)


	def get(self, request):
		# response = UserResponse.objects.filter(Q(needed_for_law='civil') | Q(needed_for_law='family') | Q(user__role='End User') | Q(user__role='user') | Q(user__role='VIP User') | Q(user__role='User'))
		response = ChallangeTicket.objects.all()
		data = []
		if response:
			for res in response:
				d = {}
				d['id'] = res.id
				d['rep_status'] = res.rep_status
				d['rep_deadline'] = res.rep_deadline
				d['notice_ref_number'] = res.notice_ref_number
				d['vehicle_reg_number'] = res.vehicle_reg_number
				d['driver_permit_number'] = res.driver_permit_number
				d['notice_issue'] = res.notice_issue
				d['reason'] = res.reason
				data.append(d)
			# print(" response => ", data)
			return Response({'status':True,'msg': "response.", 'data':data}, status=status.HTTP_200_OK)
		else:
			return Response({'status':True,'msg': "Response is empty.",'data':data}, status=status.HTTP_200_OK)



class ChallengeTicketAcceptViewSet(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		data = request.data
		print("=======================")
		rep_status = data.get("rep_status",None)
		challenge_id = data.get('challenge_id',None)
		accepted_by_name = data.get('name',None)
		accepted_by_contact = data.get('contact',None)

		if challenge_id:
			chlge_ticket = ChallangeTicket.objects.filter(id=challenge_id).first()
			chlge_ticket.rep_status = rep_status
			chlge_ticket.accept_by = request.user
			chlge_ticket.accepted_by_name = accepted_by_name
			chlge_ticket.accepted_by_contact = accepted_by_contact
			chlge_ticket.save()

			# users = User.objects.filter(Q(role='Judge') | Q(role='Attorney')) #attorney
			user = User.objects.filter(id=chlge_ticket.user.id).first() 
			registration_ids = [user.fcm_token]
			# registration_ids = ["dBzvVemUQEa0ugxixogu4Y:APA91bE42_OlhuI-702ArnbOYkxXsGZbdRdIg5xzymiXiR8DnuHYGC15akQKzWZnBBBvhmNHZnC328S8q9e6t_W0NKYS61coAMLfHW9XUfw9-dqh65YcvA9sMJ5ETC1001s3zxhJ1gxg"]
			print("registration_ids")
			print(registration_ids)
			if registration_ids:				
				# FCM Notifications
				from pyfcm import FCMNotification
				print("here")
				try:
					push_service = FCMNotification(api_key="AAAAP7tX290:APA91bFfwFuShQwi2k2sr8p1rhQKMZpZ-VbU-F6QEw3nglsfe1tAHvXB_DSfAEXKWtcKYnTgxMKZh2o-cgdjBdk_F_u_4Cdz2Lv8_LuHTrs91cy3T17CiLr3kIjnhlbdHzwoaHzgtZpe")
					message_title = "You have received notification"
					message_body = "I, "+ str(accepted_by_name)+ ",  received your Chalenge a Ticket Request on 'Legal Smart'. My number is "+ str(accepted_by_contact)+ " please contact me. At that time we will discuss my consultation fee, and schedule an appointmentdate when we can meet to discuss your matter in detail and my fees associated with the representation in Court. Thank you"
					# message_body = "You have received notification, Kindly check your profile to accept the request"
					# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
					result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
					# result = push_service.notify_single_device(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
					print(result)
					send_mail("Notification from Legal Smart", message_body, "smart_law@yopmail.com", [chlge_ticket.user.email], fail_silently=False,)
				
				except Exception as e:
					print("eeor >> ", e)
					return Response({'status':False,'msg': "Error in sending notifications."}, status=status.HTTP_200_OK)
				return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)
# 
					# return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)
		else:
			return Response({'status':False,'msg': "Device id is not there."}, status=status.HTTP_200_OK)


class WipayStatusViewSet(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		data = request.data
		print("=======================")
		payment = WiPayPayment()
		payment.name = data.get('name',None)
		payment.email = data.get('email',None)
		payment.order_id = data.get('order_id',None)
		payment.transaction_id = data.get('transaction_id',None)
		payment.reasonCode = data.get('reasonCode',None)
		payment.reasonDescription = data.get('reasonDescription',None)
		payment.responseCode = data.get('responseCode',None)
		payment.date = data.get('date',None)
		payment.total = data.get('total',None)
		stats = 0
		if data.get('status',None) == "success":
			stats = 1
		payment.status = stats
		print(stats)    
		payment.save()
		return Response({'status':True,'msg': "Response is submitted."}, status=status.HTTP_200_OK)