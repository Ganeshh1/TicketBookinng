from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Movies,Theater,ShowTiming
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm 
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from datetime import datetime 
from django.contrib.auth.decorators import login_required
# Create your views here.

current_show = None
current_TheaterName=None
current_show_time=None
curret_movie_name=None
Final_movie=None

@login_required
def home(request):
    context={
        'movies':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'latest_movies':Movies.objects.all()[:],
        # Verify Here 
       
        
    }
    return render(request,'MovieTicketBooking/home1.html',context)

@login_required
def Theater_Display(request):
    global current_TheaterName
    if request.method=='POST':
        name=request.POST.get('Theater_name')
        current_TheaterName=str(name)
        return redirect('movies/')

    context={
        'movies':Movies.objects.filter(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
    }
    return render(request,'MovieTicketBooking/theaters.html',context)


@login_required
def Disp(request):
    global current_show,current_TheaterName,curret_movie_name
    theater=Theater.objects.get(name=current_TheaterName)
    movie=Movies.objects.filter(theater_name=theater) 
    curret_movie_name=movie
    if request.method =='POST':
        name=request.POST.get('name')
        movie_name=Movies.objects.get(name=name,theater_name=y)
        current_show=ShowTiming.objects.filter(movie=movie_name,showtime__gte=datetime.now())
        context={
        'movie':movie_name,
        'timing':current_show,
        }
        return render(request,'MovieTicketBooking/show.html',context)

    context={
        'movies':Movies.objects.filter(theater_name=theater),
        'timing':ShowTiming.objects.all(),
         }
    return render(request,'MovieTicketBooking/Movies.html',context)
   
    

@login_required
def Show(request):
    global current_show,curret_movie_name,Final_movie
    if request.method=='POST':
        ticket_timing=int(request.POST['number'])
        show=ShowTiming.objects.get(id=ticket_timing)#doubte
        context={        
        'show':show,
         }
        Final_movie=show 
        if(Final_movie.count<=0):
            return render(request,'MovieTicketBooking/error.html',{})
        return render(request,'MovieTicketBooking/conform.html',context)

    context={
        'movies':Movies.objects.get(name=curret_movie_name),
        'show':ShowTiming.objects.all(),
    }
    return render(request,'MovieTicketBooking/show.html',context)

@login_required
def Confirm(request):
    global Final_movie
    if request.method=='POST':
        count=int(request.POST['count'])
        final_count=Final_movie.count
        Final_movie.count-=count
        if(Final_movie.count<0):
            Final_movie.count=final_count
            return render(request,'MovieTicketBooking/error.html',{})
        messages.warning(request,"Tickets Booked Succeesfully!")
        Final_movie.save()
        context={
                'movies':Movies.objects.all(),
                'Theater':Theater.objects.all(),
                'TickectCount':ShowTiming.objects.all(),
        }

        return render(request,'MovieTicketBooking/Message.html',context)


def register(request):
    form =CreateUserForm()
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request,'Account Created!')
            return redirect('login')
    context={
        'form':form        
        }
    return render(request,'MovieTicketBooking/Register.html',context)


def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(request,username=username,password=password)
        if( user is not None):
            if(user.is_staff):
                context={
                'movie':Movies.objects.all(),
                'Theater':Theater.objects.all(),
                'show':ShowTiming.objects.all(),
                }
                return render(request,'MovieTicketBooking/adminpage.html',context)
            else:    
                login(request,user)
                return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
            return render(request,'MovieTicketBooking/login.html')
    context={

    }
    return render(request,'MovieTicketBooking/login.html')

def logoutPage(request):
    logout(request)
    messages.info(request,'Logged Out ')
    return redirect('login')

def Addmovie(request):
    if request.method =='POST':
        flag_movie,flag_theater,flag_show=False,False,False
        moviename=request.POST['moviename']
        time=request.POST['time']
        date=request.POST['date']
        datetime=date+' '+time+':00+00:00'
        theatername=request.POST['theatername']
        count=request.POST['count']
        print(moviename,time,date,theatername,count)
        newtheater=Theater.objects.get_or_create(name=theatername)[0]
        newtheater.save()
        newmovie=Movies.objects.get_or_create(name=moviename,theater_name=newtheater)[0]
        newmovie.save()
        newshow=ShowTiming.objects.get_or_create(movie=newmovie,showtime=datetime,count=count)[0]
        newshow.save()
        messages.success(request,'Movie added Succeessfully!')
        context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
         'admin':True,
            }
        return render(request,'MovieTicketBooking/adminpage.html',context)

    context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
         'admin':True,
    }
    return render(request,'MovieTicketBooking/addmovie.html',context)

def Updatemovie(request):
    if request.method=='POST':
        movieid=request.POST['show_name']
        update_movie=ShowTiming.objects.get(id=movieid)
        moviename=request.POST['moviename']
        time=request.POST['time']
        date=request.POST['date']
        datetime=date+' '+time+':00+00:00'
        theatername=request.POST['theatername']
        count=request.POST['count']
        print(moviename,time,date,theatername,count)
        print(update_movie)
        updatetheater=Theater.objects.get_or_create(name=update_movie.movie.theater_name.name)[0]
        updatetheater.name=theatername
        updatetheater.save()
        updatemovie=Movies.objects.get_or_create(name=update_movie.movie.name,theater_name=updatetheater)[0]
        updatemovie.name=moviename
        updatemovie.save()
        update_movie=ShowTiming.objects.get(id=movieid)
        update_movie.movie=updatemovie
        update_movie.showtime=datetime
        update_movie.count=count
        update_movie.save()
        messages.success(request,'Movie Update Succeessfully!')
        context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
         'admin':True,
            }
        return render(request,'MovieTicketBooking/adminpage.html',context)

        
    context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,
    }
    return render(request,'MovieTicketBooking/updatemovie.html',context)
def RemoveMovie(request):
    if request.method=='POST':
        name=request.POST['no']
        removemovie=ShowTiming.objects.get(id=name)
        removemovie.delete()
        messages.success(request,'Movie Removed Succeessfully!')
        context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
         'admin':True,
            }
        return render(request,'MovieTicketBooking/adminpage.html',context)

        
    context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,
    }
    return render(request,'MovieTicketBooking/removemovie.html',context)
