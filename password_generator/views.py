from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from . import forms
import string
import random

def checkPassword(password):
    upperChars, lowerChars, specialChars, digits, length = 0, 0, 0, 0, 0

    for i in range(0, length):
        if (password[i].isupper()):
            upperChars += 1
        elif (password[i].islower()):
            lowerChars += 1
        elif (password[i].isdigit()):
            digits += 1
        else:
            specialChars += 1

    if (upperChars != 0 and lowerChars != 0 and digits != 0 and specialChars != 0):
        if (length >= 10):
            data = ("The strength of password is strong.\n")
        else:
            data = ("The strength of password is medium.\n")
    else:
        data = ("The strength of password is medium.\n")

    return data


def generate_password(characterList, password_length, no_repeat=False):
    password = []
    
    if no_repeat:
        password = random.sample(characterList, password_length)
    else:
        password = random.choices(characterList, k=password_length)

    return ''.join(password)


def generate_characters(request):
    characterList = ""
    if 'upperCase' in request.POST.keys():
        characterList += string.ascii_uppercase
    if 'lowerCase' in request.POST.keys():
        characterList += string.ascii_lowercase
    if 'numbers' in request.POST.keys():
        characterList += string.digits
    if 'specialCharacter' in request.POST.keys():
        characterList += '!#$%&;()*+-:;&lt;=&gt;?@_|'
    
    return characterList


def home(request):
    form = forms.FormName()
    template = loader.get_template('index.html')
    context = {
    'form': form,
    }

    # Check to see if we are getting a POST request back
    if request.method == "POST":
        if 'passwordLength' not in request.POST:
            context['error_msg'] = "Password length is required"
        elif ( 'upperCase' not in request.POST and 'lowerCase' not in request.POST and 'numbers' not in request.POST and 'specialCharacter' not in request.POST ):
            context['error_msg'] = "Atleast one of the checkbox like uppercase or lowercase need to be selected" 
        
        else:

            form = forms.FormName(request.POST)
            # Then we check to see if the form is valid
            if form.is_valid():
                password_length = form.cleaned_data['passwordLength']
                if password_length.isdigit():
                    password_length = int(password_length)
                    if password_length >=6 and password_length <=20:

                        characterList = generate_characters(request)
                        no_repeat = True if 'noRepeatCharacter' in request.POST.keys() else False

                        password = generate_password(characterList, password_length, no_repeat)

                        context['password'] = password
                        # To check if password generated is strong or not
                        context['message'] = checkPassword(password)
                    else:
                        context['error_msg'] = "Password length should be from 6 to 20"
                else:
                    context['error_msg'] = "Password length should be of Type Integer from 6 to 20"
            else:
                context['message'] = form.errors
            


    return HttpResponse(template.render(context, request))
