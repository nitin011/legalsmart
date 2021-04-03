from django.contrib import admin
from .models import Questionnaire, Age, QuesAnswer, QuestionnaireType, StaticContentApi, UserResponse, Ticket, ChallangeTicket
from django.template.response import TemplateResponse
from django.conf.urls import url
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from criminal_case_backend.law.models import LawInnerCategory
import csv
from django.utils.html import format_html

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

def remove_prefix(text):
    prefix = '"'
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

# Customised Admin view for Block users List
class QuestionnaireAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ('id', 'name','ques_type','option_type', 'law_inner_category')
    list_display_links = ('id','name')
    actions = ["export_as_csv"]
    change_list_template = "admin/ques_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            print("======================= CRIMINAL ADMIN ADD CSV ===========================")
            csv_file = request.FILES["csv_file"]
            rows = [] 
            # reading csv file 
         
                    
            # reader = csv.reader(csv_file, delimiter=":", quotechar=' ')
            reader = csv.reader(csv_file)
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            i = 0
            all_inner_law = LawInnerCategory.objects.all()
            firstline = True

            result = []
            # for line in csv_file.splitlines():
            #     result.append(tuple(line.split(",")))
            # print(result)
                
            for line in lines:
                # result.append(tuple(line.split(":")))
                if firstline:    #skip first line
                    firstline = False
                    continue

                field = line.split(";")
                print(field)

                print(len(field))
                # print(result)
               
                if len(field) > 2:
                    print("data >> ", field)
                    print("data >> ", len(field))
                    print("data 0 >> ", field[0])
                    print("data 1 >> ", field[1])
                    print("data 2 >> ", field[2])
                    print("data 3 >> ", field[3])
                    print("data 4 >> ", field[4])
                    # exit()
                    if field[0] != 'name' and field[0]:
                        import re
                        prefix = '"'
                        inner_law = re.sub(r'^{0}'.format(re.escape(prefix)), '', field[4])
                        # inner_law = field[4].removeprefix()
                        print(inner_law)
                        ques = Questionnaire.objects.filter(name=field[0]).first()

                        if ques is None:
                            law_inner_category_id = ''
                            for inner_cat in all_inner_law:
                                # print(">>>>>>>>>>>>>>>>>>>  ", inner_cat.name)
                                if inner_cat.name == inner_law:
                                    law_inner_category_id = inner_cat.id   
                            
                            quesObj = Questionnaire()
                            quesObj.name = field[0]
                            quesObj.ques_type = field[1]
                            quesObj.option_type = field[2]

                            # print("law_inner_category_id >> ", law_inner_category_id)
                            # print()
                            # print("law_inner_category_id >> ", law_inner_category_id)
                            quesObj.law_inner_category_id = law_inner_category_id
                            quesObj.option = field[2]
                            quesObj.is_active = True
                            quesObj.save()
                        
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

class QuestionnaireTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'q_type')
    list_display_links = ('id','q_type')

class QuesAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'device_id')
    list_display_links = ('id','answer')

class StaticContentApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'api_name', 'option1', 'option2')
    list_display_links = ('id','api_name')

class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'response_for', 'name', 'contact_info','option','offence')
    list_display_links = ('id','name')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'ticket_order_id', 'total_amount_USD','show_ticket_url','show_permit')
    list_display_links = ('id','name')
    readonly_fields = ['ticket_url']
  
    def show_ticket_url(self, obj):
        import re
        print(obj.ticket_url)
        if obj.ticket_url:
            return format_html('<button><a href="%s" target="_blank">Download</a></button>' % (obj.ticket_url))
    
    def show_permit(self, obj):
        import re 
        print(obj.permit)
        if obj.permit:
            if re.search( "permits", obj.permit):
                print("========================================")
                return format_html('<button><a href="%s" target="_blank">Download</a></button>' % (obj.permit))

    show_ticket_url.allow_tags = False
    show_ticket_url.short_description = "Ticket Url"
    
    show_permit.allow_tags = False
    show_permit.short_description = "Permit"

class ChallangeTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'notice_ref_number', 'vehicle_reg_number', 'driver_permit_number', 'reason')
    list_display_links = ('id','notice_ref_number')

# Registering the Admin View
admin.site.register(Questionnaire, QuestionnaireAdmin)
# admin.site.register(Age, AgeAdmin)
admin.site.register(QuesAnswer, QuesAnswerAdmin)
# admin.site.register(StaticContentApi, StaticContentApiAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(ChallangeTicket, ChallangeTicketAdmin)
