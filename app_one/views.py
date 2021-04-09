from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def main(request):
    return render(request, 'main.html')

def create(request):
    #reg errors
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    #password hashing
    pw = request.POST['pw']
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)

    #creating a new user
    print(request.POST)
    new_user =  User.objects.create(
        f_name = request.POST['f_name'],
        l_name = request.POST['l_name'],
        email = request.POST['email'],
        pw = pw_hash
    )
    request.session['user_id'] = new_user.id
    return redirect('/wall')

def login(request):
    matching_email = User.objects.filter(email=request.POST['email']).first()
    print(matching_email)

    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

    request.session['sEmail'] = request.POST['email']

    if matching_email is not None:
        if bcrypt.checkpw (request.POST['pw'].encode(), matching_email.pw.encode()):
            request.session['user_id'] = matching_email.id
            return redirect('/wall')
        else:
            print('pw incorrect')
            return redirect('/')
    else:
        print ('no user found')
        return redirect('/')

def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user, 
        'messages' : Message.objects.all(),
        'comments' : Comment.objects.all()
    }

    return render(request, 'wall.html', context)

def message(request):
    Message.objects.create(
        message = request.POST['message'],
        user = User.objects.get(id= request.session['user_id'])
    )
    return redirect('/wall')

def comment(request):
    message = Message.objects.get(id = request.POST['message_id'])
    Comment.objects.create(
        message = message,
        comment = request.POST['comment'],
        user = User.objects.get(id= request.session['user_id'])
    )
    return redirect('/wall')


def delete_msg(request, msgid):
    message = Message.objects.get(id=msgid)
    message.delete()
    return redirect("/wall")

def delete_cmt(request, cmtid):
    comment = Comment.objects.get(id=cmtid)
    comment.delete()
    return redirect("/wall")