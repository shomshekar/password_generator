from django import forms

# Create the FormName class
class FormName(forms.Form):
    passwordLength = forms.CharField(label="Length Of Password [Min=6, Max=20]", initial=6)
    upperCase = forms.BooleanField(label="Include Upper Case [A-Z]", required=False)
    lowerCase = forms.BooleanField(label="Include Lower Case [a-z]", required=False)
    numbers = forms.BooleanField(label="Include Numbers [0-9]", required=False)
    specialCharacter = forms.BooleanField(label="Include Symbols [!#$%&()*+-:;<=>?@_|]", required=False)
    noRepeatCharacter = forms.BooleanField(label="No Repeated Characters", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # if visible.field.widget.input_type == 'text':
            #     visible.field.widget.attrs['type'] = 'numbers'
            #     visible.field.widget.attrs['min'] = '6'
            #     visible.field.widget.attrs['max'] = '20'