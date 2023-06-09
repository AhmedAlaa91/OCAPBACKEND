from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import CharField, Select, HiddenInput
from phonenumber_field.formfields import PhoneNumberField
from website.models import Profile
from django.forms import ModelForm
import json
from pathlib import Path

class RegisterForm(UserCreationForm):
	password1 = CharField(widget=HiddenInput(), required=False)
	password2 = CharField(widget=HiddenInput(), required=False)

	def __init__(self, *args, request=None, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.request = request
		if self.request:
			self.user_info = self.request.session.get('user_info')
			self.fields['username'].initial = self.user_info.get('sub')
			self.fields['email'].initial = self.user_info.get('email')
			self.fields['first_name'].initial = self.user_info.get('given_name')
			self.fields['last_name'].initial = self.user_info.get('family_name')
			self.fields['username'].widget.attrs['readonly'] = True
			self.fields['email'].widget.attrs['readonly'] = True
			self.fields['first_name'].widget.attrs['readonly'] = True
			self.fields['last_name'].widget.attrs['readonly'] = True


	class Meta:
		model = User
		fields = ['username','email','first_name','last_name']

class ChangeUserForm(UserChangeForm):
	password1 = CharField(widget=HiddenInput(), required=False)
	password2 = CharField(widget=HiddenInput(), required=False)

	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)
		del self.fields['password']
		self.fields['username'].help_text = None
		self.fields['username'].widget.attrs['readonly'] = True
		self.fields['email'].widget.attrs['readonly'] = True
		self.fields['first_name'].widget.attrs['readonly'] = True
		self.fields['last_name'].widget.attrs['readonly'] = True

	class Meta:
		model = User
		fields = ['username','email','first_name','last_name']	


class ProfileForm(ModelForm):
	def get_cities():
		current_dir = Path.cwd()
		citys_file_loc= "static/json/cities.json"
		f = open(current_dir.joinpath(citys_file_loc),encoding="utf8")
		cities_json = json.load(f)
		f.close()
		citys = []
		for city in cities_json["data"]:
			city_tuple = tuple([city["id"],city["governorate_name_en"]])
			citys.append(city_tuple)
		return citys
	
	phone = PhoneNumberField()
	gender = CharField(widget=Select(choices=Profile.UserGender))
	city = CharField(
		widget=Select(choices=get_cities(),
		attrs={"onchange" : "change_areas();","id":"cities"}))
	area = CharField(
		widget=Select(
		choices=[('0', 'Choose Area')],
		attrs={"id":"areas"})
		)
	class Meta:
		model = Profile
		fields = ['phone','gender','city','area']
	