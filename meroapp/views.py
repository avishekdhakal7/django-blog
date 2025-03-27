import random
import string

from django.shortcuts import render,redirect

from django.http import HttpResponse 

from django.contrib.auth.models import User, auth

from django.contrib import messages 

from django.core.mail import send_mail

from django.conf import settings

from .models import *


def index(request):
    approvedposts=ApprovedPost.objects.all().order_by('-date') 
    
    return render (request,"index.html",{'approvedposts':approvedposts} )


def contact(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        subject=f"You got a message from {username} < {email} >|| SUBJECT: {request.POST['subject']}"
        message=request.POST['message']
        from_mail= request.POST['email']
        recipient=[settings.EMAIL_HOST_USER,]
        try:  
            send_mail(subject, message, from_mail, recipient, fail_silently=False)  
            # Add a success message  
            messages.success(request, "Email sent successfully!")  
            return redirect("/") # Replace with your success URL  
        except Exception as e:
            messages.info(request, f"Encountered error: {e}")
            return redirect("/")
        finally:
            return redirect("/")

def register(request):
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password==password2:
            
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email is already registered please login with different email")
                return redirect ('register')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, "The username is already taken")
                return redirect('register')
            
            else:
                password_otp=(random.sample(string.digits,4))
                computer_otp=("".join(password_otp))
                
                subject="Confirm your OPT"
                message=f"Your OTP is {computer_otp}"
                from_mail= settings.EMAIL_HOST_USER
                recipient=[request.POST['email']]
                send_mail(subject, message, from_mail, recipient, fail_silently=False)
                
                request.session['username'] = username  
                request.session['email'] = email  
                request.session['password'] = password # Avoid store sensitive info like password 
                request.session['computer_otp'] = computer_otp  
                return redirect('otp')
            
            
        else:
            messages.info(request,"Entered Password Didnot Match")
            return redirect ('register')
            
    else:
        return render(request,'register.html')
            
def otp(request):
    username = request.session.get('username', '')  # Use POST if you are submitting the OTP form  
    email = request.session.get('email', '')  
    password = request.session.get('password', '')  
    computer_otp = request.session.get('computer_otp', '') 
    
    if request.method=="POST":
        user_otp=request.POST['otp']
        
        if user_otp==computer_otp:
            user=User.objects.create_user(username=username, password=password, email=email)
            user.save();
        
            del request.session['password'] 
            del request.session['computer_otp']
            return redirect('login')
            
        elif user_otp != computer_otp:
            messages.info(request,"One Miss Game Finish Submit form again!")
            return render (request,'otp_form.html')
            
    else:
        return render(request,'otp_form.html',{'username': username, 'email': email}) 
    
    
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        
        else:
            messages.info(request, "Either username or password is Incorrect")
            return redirect('login')
    else:
        return render(request,'login.html')
    
    
def logout(request):
    auth.logout(request)
    return redirect("/")

def resetpassword(request):
    
    if request.method=="POST":
        email=request.POST['email']
    
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
    
            username=user.username
            print("user",user)
            request.session['username'] = username
            
            messages.info(request,"OTP sent to your email for reset password." )
            
            password_otp=(random.sample(string.digits,4))
            computer_otp=("".join(password_otp))
            
            request.session['computer_otp'] = computer_otp 
 
            subject="Use this OTP to reset your password"
            message=f"Dear user {username}, your Password reset OTP is {computer_otp}.Please keep it safe"
            from_mail= settings.EMAIL_HOST_USER
            recipient=[request.POST['email']]
            send_mail(subject, message, from_mail, recipient, fail_silently=False) 
                 
            return render (request,"resetpassword_otp.html",{'email':email})
 
        else:
             messages.info(request,"Please correctly input your user email ")
             return redirect ('resetpassword')
        
    return render(request,"resetpassword.html")


def resetpassword_otp(request):

    if request.method=="POST":
        
        computer_otp = request.session.get('computer_otp', '')
        
        username=request.session.get('username','')
        user_otp=request.POST['otp']
        email=request.POST['email']

        if user_otp==computer_otp:
            del request.session['computer_otp']
            return render(request,'confirmpassword.html',{'email':email,'username':username})
        else:
            messages.info(request,"OTP WRONG !")
            return render(request,'resetpassword_otp.html')
        
    return render (request,'resetpassword_otp.html')

def confirmpassword(request,username):
    
    if request.method=="POST":
        
        username=request.session.get('username','')
        # username=request.POST['username']       # above ,same name more than two iteration with render so creating conflict thats why i used session to hold data
        user=User.objects.get(username=username)                # and session data is stored after confirming otp sent to the gmail
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password==password2:
            user.set_password(password)
            user.save();
            
            del request.session['username']  
            
            messages.info(request,"Sucessfully changed password login now !")
            return redirect('login')
        else:
            messages.info(request,"Password not match")
            return render (request,'confirmpassword.html')
        
    return render (request,'confirmpassword.html',{'username':username})
    
    
def post(request):
    if request.method =="POST":
        title = request.POST.get('title')  # Use get to avoid MultiValueDictKeyError  
        image = request.FILES.get('image')  # Use get to avoid MultiValueDictKeyError  
        description = request.POST.get('description')  # Use get to avoid MultiValueDictKeyError   
        postby = request.POST.get('postby')  # Use get to avoid MultiValueDictKeyError  
            
        if title and description:
            if request.user.is_superuser:
                approvedpost = ApprovedPost(title=title, image=image,description=description,postby=postby)  
                approvedpost.save() ;
                messages.info(request, "Sucessfully Added")
                return redirect('/')
            
            else:
                pendingpost = PendingPost(title=title, image=image,description=description,postby=postby)  
                pendingpost.save() ;
                messages.info(request, "Sucessfully Added! wait for admins approval")
                return redirect('/')
        
    else:  
     return render(request,"post.html")
 
def pendingpost(request):
    pendingposts=PendingPost.objects.all() 
    return render(request,"pendingpost.html",{'pendingposts':pendingposts})


def pendingpostdel(request,id):
    pendingpost=PendingPost.objects.get(id=id)
    pendingpost.delete()
    messages.info(request,"succesfully deleted without posting !")
    return redirect('/')
def pendingpostapprove(request,id):
    pendingpost=PendingPost.objects.get(id=id)
    user=User.objects.get(username=pendingpost.postby)
    
    title=pendingpost.title
    image=pendingpost.image
    description=pendingpost.description
    postby=pendingpost.postby
    date=pendingpost.date
    
    approvedpost = ApprovedPost(title=title, image=image,date=date,description=description,postby=postby)
    approvedpost.save();
    pendingpost.delete();
    messages.info(request,f"succesfully Provided approval for {postby}'s post  !")
    messages.info(request,"And sent a notification via Email")
    
    subject= "Apporval of post at BLOG page"    #sending a message of post approval
    message=f"Your post at BLOG page.Posted at{pendingpost.date} has been approved by the admin just now!"  
    from_mail=settings.EMAIL_HOST_USER
    recipient=[user.email,] 
    send_mail(subject, message, from_mail, recipient, fail_silently=False)    
    return redirect('/')
  

  
def delete(request,id):
    approvedpost=ApprovedPost.objects.get(id=id)
    approvedpost.delete()
    messages.info(request,"succesfully deleted !")
    return redirect('/')

def edit(request,id):
    approvedposts=ApprovedPost.objects.all()
    for approvedpost in approvedposts:
        approvedpost
        
        if request.method =="POST":
            approvedpost=ApprovedPost.objects.get(id=id)
            
            title = request.POST.get('title')  # Use get to avoid MultiValueDictKeyError  
            image = request.FILES.get('image')  # Use get to avoid MultiValueDictKeyError  
            description = request.POST.get('description')  # Use get to avoid MultiValueDictKeyError  
            
            approvedpost.title=title
            approvedpost.image=image
            approvedpost.description=description
            
            approvedpost.save();
            messages.info(request,"succesfully edited item !")
            
            return redirect('/')
        
    return render(request,'edit.html',{'approvedpost':approvedpost})


        

   

    
