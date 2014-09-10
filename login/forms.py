#coding: utf8
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class LoginControlForm(forms.Form):
    def updateForm(self):
        users = list(User.objects.all())
        users_ids = [user.id for user in users]
        users_names = [user.username for user in users]
        users_ids.append("all")
        users_names.append("TODOS")
        usersInfo = zip(users_ids,users_names)
        monthsInfo = zip([0,1,2,3,4,5,6,7,8,9,11,12],["TODOS","Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
        yearInfo = zip([2014,2015,2016,2017,2018,2019,2020],["2014","2015","2016","2017","2018","2019","2020"])
        self.fields['dropDownUsers'] = forms.ChoiceField(widget=forms.Select, choices=usersInfo, label = "Usuário")
        self.fields['dropDownMonth'] = forms.ChoiceField(widget=forms.Select, choices=monthsInfo, label = "Mês")
        self.fields['dropDownYear'] = forms.ChoiceField(widget=forms.Select, choices=yearInfo, label = "Ano")
        
        