from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from . import forms
import string
import random

special_characters = '!#$%&()*+-:;?@_|'

# Function to check if the generated password is strong or medium
def checkPassword(password):
    upperChars, lowerChars, specialChars, digits, length = 0, 0, 0, 0, len(password)

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


def select_character(characterList, string_type, no_repeat):
    choice = random.choices(string_type, k=1)
    choice = ''.join(choice)
    if no_repeat:
        characterList.replace(choice, '')
    return choice, characterList


def generate_password(characterList, password_length, no_repeat, str_type):

    password = ''
    if 'upperCase' in str_type:
        passData, characterList = select_character(characterList, string.ascii_uppercase, no_repeat)
        password += ''.join(passData)
    if 'lowerCase' in str_type:
        passData, characterList = select_character(characterList, string.ascii_lowercase, no_repeat)
        password += ''.join(passData)
    if 'numbers' in str_type:
        passData, characterList = select_character(characterList, string.digits, no_repeat)
        password += ''.join(passData)
    if 'specialCharacter' in str_type:
        passData, characterList = select_character(characterList, special_characters, no_repeat)
        password += ''.join(passData)

    if no_repeat:
        password += ''.join(random.sample(characterList, password_length))
    else:
        password += ''.join(random.choices(characterList, k=password_length))

    # import requests
    # r = requests.get('cNSg<P')
    
    return password


# Function to group characters, as per options selected by user, before generating password
def generate_characters(request, str_type):
    characterList = ""
    if 'upperCase' in request.POST.keys():
        str_type.append('upperCase')
        characterList += string.ascii_uppercase
    if 'lowerCase' in request.POST.keys():
        str_type.append('lowerCase')
        characterList += string.ascii_lowercase
    if 'numbers' in request.POST.keys():
        str_type.append('numbers')
        characterList += string.digits
    if 'specialCharacter' in request.POST.keys():
        str_type.append('specialCharacter')
        characterList += special_characters
    
    return characterList

# Additional conditions to check before form valid
def checkPasswordConditions(request, context):

    password_length = request.POST['passwordLength']
    context['password_length'] = password_length
    if not password_length.isdigit():
        context['error_msg'] = "Password length should be of Type Integer from 6 to 20"
    else:
        password_length = int(password_length)
        if password_length < 6 or password_length > 20:
            context['error_msg'] = "Password length should be from 6 to 20"
        else:
            if ( 'upperCase' not in request.POST and 'lowerCase' not in request.POST and 'numbers' not in request.POST and 'specialCharacter' not in request.POST ):
                context['error_msg'] = "Atleast one of the checkbox like uppercase or lowercase need to be selected" 
            elif ( 'upperCase' not in request.POST and 'lowerCase' not in request.POST and 'specialCharacter' not in request.POST and 'numbers' in request.POST and 'noRepeatCharacter' in request.POST and password_length > len(string.digits) ):
                context['error_msg'] = "Cannot generate password without repeating to match password length"

    return context


def home(request):
    form = forms.FormName()
    template = loader.get_template('index.html')
    context = {
    'form': form,
    }

    # Check to see if we are getting a POST request back
    if request.method == "POST":

        form = forms.FormName(request.POST)
        context = checkPasswordConditions(request, context)

        if 'error_msg' not in context:
            # Then we check to see if the form is valid
            if form.is_valid():
                str_type = []
                password_length = int(context['password_length'])
                # Group characters as per option selected by user
                characterList = generate_characters(request, str_type)
                password_length = password_length - len(str_type)

                no_repeat = True if 'noRepeatCharacter' in request.POST.keys() else False
                password = generate_password(characterList, password_length, no_repeat, str_type)

                context['password'] = password
                # To check if password generated is strong or not
                context['message'] = checkPassword(password)
            else:
                context['message'] = form.errors

    return HttpResponse(template.render(context, request))
