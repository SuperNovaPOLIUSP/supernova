from django import forms

class ProfessorForm(forms.Form):
    
    name = forms.CharField(max_length = 255, required = True, label = 'Name')
    memberId = forms.IntegerField(required = True, label = 'Member ID')
    office = forms.CharField(max_length = 45, required = False, label = 'Office')
    email = forms.CharField(max_length = 65, required = False, label = 'Email')
    phoneNumber = forms.IntegerField(required = False, label = 'Phone Number')
    cellphoneNumber = forms.IntegerField(required = False, label = 'CellPhone Number')
    idDepartment = forms.IntegerField(required = False, label = 'ID Department')
    