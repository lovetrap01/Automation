#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ***models.py***
# This file contains all the defination for models of Automation software. 
# including tables, classes, forms and mappers.
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#::::::::::::::IMPORT THE HEADER FILE HERE:::::::::::::::::::::::::::::#
from django.db import models
from django.forms import ModelForm, TextInput, ModelChoiceField
from django import forms
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Max ,Q, Sum
import datetime
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from tagging.fields import TagField
from tagging.models import Tag
from Automation.tcc.choices import *
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

#::::::::::::::::::::::DEFINE THE MODELS HERE:::::::::::::::::::::::::::#
class Report(models.Model):
	"""
	Define Client Report Form to reterive any Report Information,
	when we fill Job Number and type of Report Store in Database
	"""
	name = models.CharField(max_length=50)

	def __unicode__(self):
        	return self.name

class UserProfile(models.Model):
    # This field is required.
        user = models.ForeignKey(User)

    # Other fields here
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100,blank=True, null=True)
	last_name = models.CharField(max_length=100,blank=True, null=True)
	company =models.CharField(max_length=255,null=True,blank=True)
	address =models.CharField(max_length=255)
	city =models.CharField(max_length=255)
	pin_code = models.IntegerField(null=True,blank=True)
	state=models.CharField(max_length=30,choices=STATES_CHOICES,default='Punjab')
	website =models.URLField(blank=True, null=True)
	contact_no =models.CharField(max_length=25)
	type_of_organisation = models.CharField(max_length=20,choices=ORGANISATION_CHOICES)

	def __unicode__(self):
        	return self.first_name


class UserProfileForm(ModelForm):
	class Meta :
		model = UserProfile
		exclude= ['user']
		widgets = {
             'first_name' : TextInput(attrs={'size':60}),
	     'middle_name' : TextInput(attrs={'size':60}),
	     'last_name' : TextInput(attrs={'size':60}),
             'company' : TextInput(attrs={'size':60}),
             'address' : TextInput(attrs={'size':60}),
             'city' : TextInput(attrs={'size':60}),
             'pin_code' : TextInput(attrs={'size':60}),
             'website' : TextInput(attrs={'size':60}),
	     'contact_no' : TextInput(attrs={'size':60}),
                  }
	

class Auto_number(models.Model):
	id = models.AutoField(primary_key=True)
	job_no = models.IntegerField(unique = True)

class Organisation(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=150)
	phone = models.CharField(max_length=20)
	director = models.CharField(max_length=50) 
	

	def __unicode__(self):
        	return self.name

class Department(models.Model):
	organisation = models.ForeignKey(Organisation)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=150)
	phone = models.CharField(max_length=20, blank=True)
	dean = models.CharField(max_length=50, blank=True)
	faxno = models.IntegerField( blank=True, null=True)
	email_1 = models.CharField(max_length=75,blank=True)
	email_2 = models.CharField(max_length=75,blank=True)
	url = models.CharField(max_length=50,blank=True)
	about = models.CharField(max_length=150,blank=True)

	def __unicode__(self):
        	return self.name

class Lab(models.Model):
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=300)
	department = models.ForeignKey(Department)
	tags = TagField()

	def __unicode__(self):
        	return self.name

	def get_tags(self):
        	return Tag.objects.get_for_object(self) 


class Material(models.Model):
	lab = models.ForeignKey(Lab)
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=300)
	tags = TagField()
	report = models.ForeignKey(Report)

	def __unicode__(self):
        	return self.name

	def get_tags(self):
        	return Tag.objects.get_for_object(self) 

class Test(models.Model):
	#lab = models.ForeignKey(Lab)
	material = models.ForeignKey(Material)
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=300)
	quantity = models.CharField(max_length=100,blank=True, null=True)
	unit = models.CharField(max_length=15)
	cost = models.IntegerField(blank=True, null=True)
	tags = TagField()

	def __unicode__(self):
        	return self.name
	
	def get_tags(self):
        	return Tag.objects.get_for_object(self) 

class Clientadd(models.Model):
	user = models.ForeignKey(User)
	client = models.ForeignKey(UserProfile)
	
class editClientadd(models.Model):
	user = models.ForeignKey(User)
	client = models.ForeignKey(UserProfile)

class Govt(models.Model):
	name =	models.CharField(max_length=600, blank=True )

	def __unicode__(self):
        	return self.name

class Payment(models.Model):
	name = models.CharField(max_length = 50,blank =True)

	def __unicode__(self):
        	return self.name

class Job(models.Model):
	"""
	**ClientJob**
	
	ClientJob Class is define all field required to submit detail about new Job.
	
	""" 
        client = models.ForeignKey(Clientadd)
	job_no = models.IntegerField(editable =False)
	sample = models.IntegerField()
	ip = models.CharField(max_length=50)
	site = models.CharField(max_length=1000)
	type_of_work = models.ForeignKey(Govt)
	report_type = models.ForeignKey(Report)
	pay = models.CharField(max_length=600)
	check_number = models.CharField(max_length=15,blank=True)
	check_dd_date = models.CharField(blank=True, max_length=15)
	date = models.DateField(auto_now_add=True)
	letter_no = models.IntegerField(blank=True,null=True)
	letter_date = models.DateField( blank=True, null=True)
	tds = models.IntegerField(default="0")

	def __unicode__(self):
          return self.id()

class EditJob(models.Model):
	"""
	**ClientJob**
	
	ClientJob Class is define all field required to submit detail about new Job.
	
	""" 
        client = models.ForeignKey(editClientadd)
	job_no = models.IntegerField(editable =False)
	sample = models.CharField(max_length=11)
	ip = models.CharField(max_length=50)
	site = models.CharField(max_length=600)
	type_of_work = models.ForeignKey(Govt)
	report_type = models.ForeignKey(Report)
	pay = models.CharField(max_length=600, blank=True )
	date = models.DateField(auto_now_add=True)
	check_number = models.CharField(max_length=15,blank=True)
	check_dd_date = models.CharField(blank=True, max_length=15)
	letter_no = models.IntegerField(blank=True,null=True)
	letter_date = models.DateField( blank=True, null=True)
	tds = models.IntegerField(default="0")

	def __unicode__(self):
          return self.id()

class JobForm(forms.ModelForm):
	class Meta :
		model = Job
		exclude= ['client','job_no','report_type','date','ip']
        
class editJobForm(forms.ModelForm):
	class Meta :
		model = EditJob
		exclude= ['client','job_no','report_type','date','ip'] 
	
	
class ClientJob(models.Model):
	job = models.ForeignKey(Job)
	material = models.ForeignKey(Material)
	test = models.ManyToManyField(Test)
	
	def __unicode__(self):
          return self.id()

class ClientJobForm(forms.ModelForm):
	class Meta :
		model = ClientJob
		exclude= ['job','material']

class ClientEditJob(models.Model):
	job = models.ForeignKey(EditJob)
	material = models.ForeignKey(Material)
	test = models.ManyToManyField(Test)
	
	def __unicode__(self):
          return self.id()
	

class ClientjobForm(forms.ModelForm):
	test = forms.ModelMultipleChoiceField(queryset=Test.objects.all(), required=False,widget=forms.CheckboxSelectMultiple)

	class Meta :
		model = ClientJob
		exclude= ['job']

	def __init__(self,*args, **kwargs):
		super(ClientjobForm,self).__init__(*args,**kwargs)
		try:
            		material = kwargs['instance'].material
       		except KeyError:
           		 material = 1 	
		self.fields['test'].queryset=Test.objects.filter(material_id = material) 

class editClientJobForm(forms.ModelForm):
	class Meta :
		model = ClientEditJob
		exclude= ['job','material']
	


class SuspenceJob(models.Model):
	"""
	**SuspenceJob**
	
	SuspenceJob Class is used to define all fields required to submit detail about new Suspence Job.
	
	""" 
	job = models.ForeignKey(Job)
	field = models.ForeignKey(Material)
	test = models.ForeignKey(Test)
	other = models.CharField(max_length=600, blank=True )
	

	def __unicode__(self):
          return self.id()

class SuspenceEditJob(models.Model):
	"""
	**SuspenceJob**
	
	SuspenceJob Class is used to define all fields required to submit detail about new Suspence Job.
	
	""" 
	job = models.ForeignKey(EditJob)
	field = models.ForeignKey(Material)
	test = models.ForeignKey(Test)
	other = models.CharField(max_length=600, blank=True )
	

	def __unicode__(self):
          return self.id()

class SuspenceJobForm(forms.ModelForm):
	class Meta :
		model = SuspenceJob
		exclude= ['job','field','test']

class editSuspenceJobForm(forms.ModelForm):
	class Meta :
		model = SuspenceEditJob
		exclude= ['job','field','test']

class SuspencejobForm(forms.ModelForm):
	class Meta :
		model = SuspenceJob
		exclude= ['job']


class TestTotal(models.Model):
	job_no = models.IntegerField(editable =False)
	job = models.ForeignKey(Job)
	mat = models.IntegerField(editable =True,null=True)
	unit_price = models.IntegerField(blank=True,null=True)
	balance = models.IntegerField(blank=True,null=True)
	type = models.CharField(max_length=100,blank=True,null=True)

	def __unicode__(self):
        	return self.id


class TestTotalPerf(models.Model):
	job_no = models.IntegerField(editable =False)
	job = models.ForeignKey(EditJob)
	mat = models.IntegerField(editable =True,null=True)
	unit_price = models.IntegerField(blank=True,null=True)
	balance = models.IntegerField(blank=True,null=True)
	type = models.CharField(max_length=100,blank=True,null=True)

	def __unicode__(self):
        	return self.id

class Bill(models.Model):
	job_no = models.IntegerField(primary_key=True, editable =False)
	education_tax = models.IntegerField(blank=True,null=True)
	higher_education_tax = models.IntegerField(blank=True,null=True)
	service_tax = models.IntegerField(blank=True,null=True)
	net_total = models.IntegerField(blank=True,null=True)
	price = models.IntegerField(blank=True,null=True)

class BillPerf(models.Model):
	job_no = models.IntegerField(primary_key=True, editable =False)
	education_tax = models.IntegerField(blank=True,null=True)
	higher_education_tax = models.IntegerField(blank=True,null=True)
	service_tax = models.IntegerField(blank=True,null=True)
	net_total = models.IntegerField(blank=True,null=True)
	price = models.IntegerField(blank=True,null=True)


class Amount(models.Model):
	job = models.ForeignKey(Job)
	college_income = models.IntegerField(blank=True, null=True)
	admin_charge = models.IntegerField(blank=True,null=True)
	consultancy_asst = models.IntegerField(blank=True,null=True)
	development_fund = models.IntegerField(blank=True,null=True)
	unit_price = models.IntegerField(blank=True,null=True)
	report_type = models.CharField(max_length=100,blank=True,null=True)
		
        def __unicode__(self):
          return self.id()



class AmountForm(ModelForm):
	class Meta :
		model = Amount

class CdfAmount(models.Model):
	job_no = models.IntegerField(primary_key=True, editable =False)
	date = models.DateField(default=datetime.date.today(), editable=False)
	lab = models.CharField(max_length=100)
	total = models.IntegerField()
	field = models.CharField(max_length=10)
	other_field = models.CharField(max_length=100,blank=True,null=True)
	report_type = models.CharField(max_length=20,editable=False)

class CdfAmountForm(ModelForm):
	class Meta :
		model = CdfAmount	
	
class Distance(models.Model):
    	job =models.IntegerField(editable =False)
    	sandy = models.DecimalField(max_digits=10, decimal_places=3)

class DistanceForm(ModelForm):
	class Meta :
		model = Distance
		exclude= ['job']
	
	def __unicode__(self):
        	return self.id



class Suspence(models.Model):
	job = models.ForeignKey(Job)
	rate = models.IntegerField(null=True, blank=True)
	sus = models.ForeignKey(SuspenceJob)
	work_charge = models.IntegerField(null=True, blank=True)
	labour_charge = models.IntegerField( blank=True, null=True)
	boring_charge_external = models.IntegerField( blank=True, null=True)
	boring_charge_internal = models.IntegerField( blank=True, null=True)
	car_taxi_charge = models.IntegerField( blank=True, null=True)
	lab_testing_staff = models.CharField( max_length=90,blank=True)
	field_testing_staff =models.CharField( max_length=90,blank=True)
	test_date = models.DateField( blank=True, null=True)
	suspence_bill_no = models.IntegerField( blank=True, null=True)

class SuspenceForm(ModelForm):
	class Meta :
		model = Suspence




class Staff(models.Model):
	department = models.ForeignKey(Department)
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=50)
	daily_income = models.IntegerField(blank=True)
	position = models.CharField(max_length=15)
	lab = models.ForeignKey(Lab)
	email =models.EmailField(blank=True)

	def __unicode__(self):
        	return self.name
	


class ProfromaTax(models.Model):
    pro_no = models.IntegerField(primary_key=True)
    service_tax = models.IntegerField()
    higher_education_tax = models.IntegerField()
    education_tax = models.IntegerField()
    total = models.IntegerField()

class TaDa(models.Model):
	"""
	Model of TA/DA Report
	"""
	job = models.ForeignKey(Job)
	departure_time_up = models.TimeField(default = "00:00:00") 
	arrival_time_up = models.TimeField(default = "00:00:00") 
	departure_time_down = models.TimeField(default = "00:00:00")
	arrival_time_down = models.TimeField(default = "00:00:00") 
	tada_amount = models.IntegerField(blank=True, null=True, editable=False)
	reach_site = models.CharField(max_length=60, blank=True)
	test_date = models.CharField(max_length=15)
	end_date = models.CharField(max_length=15)
	testing_staff_code = models.CharField(max_length=50)
	

class TadaForm(ModelForm):
	class Meta :
		model = TaDa
		exclude= ['job']
		widgets = {
             'job' : TextInput(attrs={'size':20}),
             'departure_time_up' : TextInput(attrs={'size':20}),
             'arrival_time_up' : TextInput(attrs={'size':20}),
             'departure_time_down' : TextInput(attrs={'size':20}),
             'arrival_time_down' : TextInput(attrs={'size':20}),
             'tada_amount' : TextInput(attrs={'size':20}),
	     'reach_site' : TextInput(attrs={'size':20}),
	     'test_date' : TextInput(attrs={'size':20}),
	     'end_date' : TextInput(attrs={'size':20}),
	     'testing_staff_code' : TextInput(attrs={'size':20}),
                  }

		
		
class Transportation(models.Model):
	vehicleno = models.CharField(max_length=150)
	rate = models.IntegerField(default='7')

       	def __str__(self):
          return '%s %s' % (self.vehicleno, self.rate)

class Transport(models.Model):
	"""
	Model of Transport  Bill record
	"""
	vehicle = models.ForeignKey(Transportation)
	id = models.AutoField(primary_key=True)
	job_no = models.IntegerField()
	bill_no = models.IntegerField(null=True, editable=False)
	kilometer = models.CharField(max_length=150, default="00, 00, 00")
	#rate = models.IntegerField(default='4')
	amounts = models.CharField(max_length=180, blank=True,editable=False)
	total = models.IntegerField(blank=True, null=True , editable=False)
	date = models.DateField(default=datetime.date.today())
	test_date = models.CharField(max_length=300, default="0000-00-00, 0000-00-00")

class TransportForm(ModelForm):
	class Meta :
		model = Transport

class Bankdetails(models.Model):
	accname = models.CharField(max_length=50)
	accountno = models.IntegerField(null=False)
	accountcode = models.CharField(max_length=50)
	address = models.CharField(max_length=150)

class BankdetailsForm(ModelForm):
	class Meta :
		model = Bankdetails

class LabReport(forms.Form):
	"""
	Form that displays start and end date and thus helps in retrieving data between this date range for a particular material.
	"""
	start_date= forms.DateField()
        end_date= forms.DateField()
	material = forms.ModelChoiceField(queryset=Material.objects.all())
