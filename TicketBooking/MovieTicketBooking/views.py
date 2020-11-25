from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Movies,Theater,TotalCount,ShowTiming
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
        'latest_movies':Movies.objects.all()[:],
        
       
        
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
        'TickectCount':TotalCount.objects.all(),
    }
    return render(request,'MovieTicketBooking/theaters.html',context)


@login_required
def Disp(request):
    global current_show,current_TheaterName,curret_movie_name
    theater=Theater.objects.get(name=current_TheaterName)
    movie=Movies.objects.filter(theater_name=theater) 
    print(current_TheaterName)
    curret_movie_name=movie
    

    if request.method =='POST':
        
        print(request.POST)
        moviename=request.POST.get('name')
        print(current_show)
        movie_name=Movies.objects.get(name=moviename)
        current_show=ShowTiming.objects.filter(movie=movie_name,showtime__gte=datetime.now())
        context={
        'movie':movie_name,
        'timing':current_show,
        }

        return render(request,'MovieTicketBooking/show.html',context)

    context={
        'movies':Movies.objects.filter(theater_name=y),
        'timing':ShowTiming.objects.all(),
         }
    return render(request,'MovieTicketBooking/Movies.html',context)
   
    

@login_required
def Show(request):
    global current_show,curret_movie_name,Final_movie
    
    if request.method=='POST':
        print(request.POST)
        ticket_timing=request.POST['number']
        show=TotalCount.objects.get(Tickets=ShowTiming.objects.get(id=ticket_timing ))
        print(show)
        context={
        
        'show':show,
         }
        Final_movie=show 
        if(Final_movie.count<=0):
            return render(request,'MovieTicketBooking/error.html',{})

        return render(request,'MovieTicketBooking/conform.html',context)

    context={
        'movies':Movies.objects.get(name=curret_movie_name),
        'show':TotalCount.objects.filter(),
    }
    return render(request,'MovieTicketBooking/show.html',context)

@login_required
def Confirm(request):
    global Final_movie
    print(Final_movie)
    if request.method=='POST':
        count=int(request.POST['count'])
        print(count,Final_movie.count)
        count_final=Final_movie.count
        Final_movie.count-=count
        if(Final_movie.count<0):
            Final_movie.count=count_final
            return render(request,'MovieTicketBooking/error.html',{})
        messages.warning(request,"Tickets Booked Succeesfully!")
        Final_movie.save()
        context={
                'movies':Movies.objects.all(),
                'Theater':Theater.objects.all(),
                'TickectCount':TotalCount.objects.all(),
        }

        return render(request,'MovieTicketBooking/Message.html',context)



def register(request):
    form =CreateUserForm()
    print(form)
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        print(request.POST)
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
                'movies':Movies.objects.all(),
                'Theater':Theater.objects.all(),
                'TickectCount':TotalCount.objects.all(),
                }
                return render(request,'MovieTicketBooking/adminpage.html',context)
            else:    
                login(request,user)
                return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
            return render(request,'MovieTicketBooking/login.html',context)
    context={

    }
    return render(request,'MovieTicketBooking/login.html',context)

def logoutPage(request):
    logout(request)
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
        for theater in Theater.objects.all():
            if(theatername==theater.name):
                flag_theater=True
        if(flag_theater):
            newtheater=Theater.objects.get(name=theatername)
        else:
            newtheater=Theater(name=theatername)
            newtheater.save()
        for movie in Movies.objects.all():
            if(moviename==movie.name):
                flag_movie=True
        if(flag_movie):
            newmovie=Movies.objects.get(name=moviename)
        else:
            newmovie=Movies(name=moviename,theater_name=newtheater)
            newmovie.save()
        for showtimes in ShowTiming.objects.all():
            if(datetime==showtimes.showtime):
                flag_show=True
        if(flag_show):
            newshow=ShowTiming.objects.get(showtime=datetime)
        else:
            newshow=ShowTiming(movie=newmovie,showtime=datetime)
            newshow.save()
        newshowtime=TotalCount(Tickets=newshow,count=count)
        newshowtime.save()
        messages.success(request,'Movie added Succeessfully!')
        context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'TickectCount':TotalCount.objects.all(),
         'admin':True,
            }
        return render(request,'MovieTicketBooking/adminpage.html',context)

    context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'TickectCount':TotalCount.objects.all(),
         'admin':True,
    }
    return render(request,'MovieTicketBooking/addmovie.html',context)

def Updatemovie(request):
    context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'TickectCount':TotalCount.objects.all(),
        'admin':True,
    }
    return render(request,'MovieTicketBooking/updatemovie.html',context)

def RemoveMovie(request):
    if request.method=='POST':
        name=request.POST['name']
        removemovie=Movies.objects.get(name=name)
        removemovie.delete()
        messages.success(request,'Movie Removed Succeessfully!')
        context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'TickectCount':TotalCount.objects.all(),
         'admin':True,
            }
        return render(request,'MovieTicketBooking/adminpage.html',context)

        
    context={
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'TickectCount':TotalCount.objects.all(),
        'admin':True,
    }
    return render(request,'MovieTicketBooking/removemovie.html',context)
