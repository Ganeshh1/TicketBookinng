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
        # Verify Here 
       
        
    }
    return render(request,'MovieTicketBooking/home1.html',context)

@login_required
def Theater_Display(request):
    global current_TheaterName
    if request.method=='POST':
        print('helloooooooooooo')
        name=request.POST.get('Theater_name')
        current_TheaterName=str(name)
        print('1st',current_TheaterName)
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
    print('here',current_show,current_TheaterName)
    y=Theater.objects.get(name=current_TheaterName)
    x=Movies.objects.filter(theater_name=y) 
    print(current_TheaterName)
    print('He',x)
    print('Chudura',y)
    curret_movie_name=y
    

    if request.method =='POST':
        
        print(request.POST)
        name=request.POST.get('name')
        print(current_show)
        print(name)
        movie_name=Movies.objects.get(name=name)
        print(movie_name)
        current_show=ShowTiming.objects.filter(movie=movie_name,showtime__gte=datetime.now())
        print(current_show)

        print(movie_name,'MOVIENAME**************')
        # current_show = movie_name
        # context={
        #     'movies':Movies.objects.filter(theater_name=Theater.objects.get(name=str(name[0]))),
        #     'timing':ShowTiming.objects.all(),
        #         }
        #     return render(request,'MovieTicketBooking/Movies.html',context)

        context={
        'movie':movie_name,
        'timing':current_show,
        
         }

        # current_show_time=ShowTiming.objects.filter(showtime=current_show)
        # print(context['movies'])
        # print(context['timing'])
        # print(current_show_time)
        return render(request,'MovieTicketBooking/show.html',context)

    context={
        'movies':Movies.objects.filter(theater_name=y),
        'timing':ShowTiming.objects.all(),
         }
    return render(request,'MovieTicketBooking/Movies.html',context)
   
    

@login_required
def Show(request):
    global current_show,curret_movie_name,Final_movie
    print(current_show,'000000000000000',curret_movie_name)
    
    if request.method=='POST':
        print(request.POST)
        ticket_timing=request.POST['number']
        a=TotalCount.objects.get(Tickets=ShowTiming.objects.get(id=ticket_timing ))#doubte
        print(a)
        context={
        
        'show':a,
         }
        Final_movie=a 
        if(Final_movie.count<=0):
            return render(request,'MovieTicketBooking/error.html',{})

        print(context)
        # return HttpResponse('Hello')
        return render(request,'MovieTicketBooking/conform.html',context)

    context={
        'movies':Movies.objects.get(name=curret_movie_name),
        'show':TotalCount.objects.filter(),
    }
    # print(context['movies'])
    print(current_show,'0000000')
    print(context['Theater'])
    # print(context['show'])
    return render(request,'MovieTicketBooking/show.html',context)

@login_required
def Confirm(request):
    global Final_movie
    print(Final_movie)
    if request.method=='POST':
        count=int(request.POST['count'])
        print(count,Final_movie.count)
        a=Final_movie.count
        Final_movie.count-=count
        if(Final_movie.count<0):
            Final_movie.count=a
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
        print('sajndlajksnlasndl',username,password)

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
        moviename=request.POST['moviename']
        time=request.POST['time']
        date=request.POST['date']
        datetime=date+' '+time+':00+00:00'
        theatername=request.POST['theatername']
        count=request.POST['count']
        print(moviename,time,date,theatername,count)
        newtheater=Theater(name=theatername)
        newtheater.save()
        newmovie=Movies(name=moviename,theater_name=newtheater)
        newmovie.save()
        newshow=ShowTiming(movie=newmovie,showtime=datetime)
        newshow.save()
        newshowtime=TotalCount(Tickets=newshow,count=count)
        newshowtime.save()
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
