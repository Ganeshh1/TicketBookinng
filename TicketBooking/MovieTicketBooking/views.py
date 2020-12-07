from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Movies,Theater,ShowTiming
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,MovieCreateForm
from django.contrib.auth import authenticate,login,logout
from datetime import datetime 
from django.contrib.auth.decorators import login_required
# class Based View 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView,CreateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

current_show = None
current_TheaterName = None
current_show_time = None
curret_movie_name = None
Final_movie = None

class Home(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name ='redirect_to'
    template_name = 'MovieTicketBooking/home1.html'

    def get_context_data(self,**kargs):
        context = super().get_context_data(**kargs)
        context['movies'] = Movies.objects.all()
        context['Theater'] = Theater.objects.all()
        context['Show'] = ShowTiming.objects.all()
        context['latest_movies'] = Movies.objects.order_by('-id')[0:3]
        return context


@method_decorator(login_required, name='dispatch')
class TheaterDisplay(View):
    template_name = 'MovieTicketBooking/theaters.html'
    
    def get(self,request,*args,**kargs):
        context = {
        'movies':Movies.objects.filter(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        }
        return render(request,'MovieTicketBooking/theaters.html',context)


    def post(self,request,*args,**kargs):
        global current_TheaterName
        name = request.POST.get('Theater_name')
        current_TheaterName = str(name)
        return redirect('movies/')
        


@method_decorator(login_required, name='dispatch')
class Disp(View):
    template_name = 'MovieTicketBooking/Movies.html'

    def get(self,request,*args,**kargs):
        global current_show,current_TheaterName,curret_movie_name
        theater = Theater.objects.get(name=current_TheaterName)
        movie = Movies.objects.filter(theater_name=y) 
        curret_movie_name = movie
        current_TheaterName = theater
        context = {
        'movies':Movies.objects.filter(theater_name = theater),
        'timing':ShowTiming.objects.all(),
        }
        return render(request,self.template_name,context)

    def post(self,request,*args,**kargs):
        global current_show,current_TheaterName,curret_movie_name
        name = request.POST.get('name')
        movie_name = Movies.objects.get(name = name,theater_name = current_TheaterName)
        current_show = ShowTiming.objects.filter(movie = movie_name,showtime__gte = datetime.now())
        context = {
        'movie':movie_name,
        'timing':current_show,
        }
        return render(request,'MovieTicketBooking/show.html',context)



@method_decorator(login_required, name = 'dispatch')    
class Show(View):
    template_name = 'MovieTicketBooking/show.html'

    def get(self,request,*agrs,**kargs):
        global current_show,curret_movie_name,Final_movie
        context={
        'movies':Movies.objects.get(name = curret_movie_name),
        'show':ShowTiming.objects.all(),
        }
        return render(request,self.template_name,context)

    def post(self,request,*args,**kargs):
        global current_show,curret_movie_name,Final_movie
        ticket_timing = int(request.POST['number'])
        shows = ShowTiming.objects.get(id = ticket_timing)#doubte
        context={
        'show':shows,
        }
        Final_movie=shows 
        if(Final_movie.count <= 0):
            return render(request,'MovieTicketBooking/error.html',{})
        return render(request,'MovieTicketBooking/conform.html',context)

@method_decorator(login_required, name = 'dispatch') 
class Confirm(View):
    template_name = 'MovieTicketBooking/error.html'
    def post(self,request,*args,**kargs):
        global Final_movie
        count = int(request.POST['count'])
        Count_final = Final_movie.count
        Final_movie.count -= count
        if(Final_movie.count < 0):
            Final_movie.count = Count_final
            return render(request,self.template_name,{})
        messages.warning(request,"Tickets Booked Succeesfully!")
        Final_movie.save()
        context = {
        'movies':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'TickectCount':ShowTiming.objects.all(),
        }
        return render(request,'MovieTicketBooking/Message.html',context)

class Register(FormView):
    template_name = 'MovieTicketBooking/Register.html'
    form_class = CreateUserForm
    success_url = '/login/'

    def get_context_data(self,**kargs):
        context = super().get_context_data(**kargs)
        context['form'] = CreateUserForm()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'Account Created!')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        response = super().form_invalid(form)
        messages.warning(self.request,'Enter the Data Properly')
        return response


class LoginPage(View):
    template_name = 'MovieTicketBooking/login.html'

    def get(self,request,*args,**krgs):
        return render(self.request,self.template_name,{})

    def post(self,request,*args,**krgs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if( user is not None):
            if(user.is_staff):
                context = {
                'movie':Movies.objects.all(),
                'Theater':Theater.objects.all(),
                'show':ShowTiming.objects.all(),
                'admin':True
                }
                return render(request,'MovieTicketBooking/adminpage.html',context)
            else:    
                login(request,user)
                return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
            return render(request,'MovieTicketBooking/login.html')


def logoutPage(request):
    logout(request)
    messages.info(request,'Logged Out ')
    return redirect('login')

@method_decorator(login_required, name = 'dispatch')
class AddMovie(View):
    template_name = 'MovieTicketBooking/addmovie.html'

    def get(self,request,*args,**krgs):
        context = {
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,
        }
        return render(request,self.template_name,context)

    def post(self,request,*args,**krgs):
        moviename = request.POST['moviename']
        time = request.POST['timing']
        theatername = request.POST['theatername'] 
        count = request.POST['count']
        time = str(time)
        time = time.split('T')
        datetime = time[0]+' '+time[1]+':00+00:00'
        newtheater = Theater.objects.get_or_create(name=theatername)[0]
        newtheater.save()
        newmovie = Movies.objects.get_or_create(name=moviename,theater_name=newtheater)[0]
        newmovie.save()
        newshow = ShowTiming.objects.get_or_create(movie=newmovie,showtime=datetime,count=count)[0] 
        newshow.save()
        messages.success(request,'Movie added Succeessfully!')
        context = {
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,    
        }
        return render(request,'MovieTicketBooking/adminpage.html',context)

@method_decorator(login_required, name = 'dispatch')
class UpdateMovie(View):
    template_name = 'MovieTicketBooking/updatemovie.html'

    def get(self,request,*args,**krgs):
        context = {
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,
        }
        return render(request,self.template_name,context)

    def post(self,request,*args,**krgs):
        movieid = request.POST['show_name']
        update_movie = ShowTiming.objects.get(id=movieid)
        moviename = request.POST['moviename']
        time = request.POST['timing']
        time = str(time) 
        time = time.split('T')
        datetime = time[0]+' '+time[1]+':00+00:00'
        theatername = request.POST['theatername']
        count = request.POST['count']
        updatetheater = Theater.objects.get_or_create(name=update_movie.movie.theater_name.name)[0]
        updatetheater.name = theatername
        updatetheater.save()
        updatemovie = Movies.objects.get_or_create(name=update_movie.movie.name,theater_name=updatetheater)[0]
        updatemovie.name = moviename
        updatemovie.save()
        update_movie = ShowTiming.objects.get(id=movieid)
        update_movie.movie = updatemovie
        update_movie.showtime = datetime
        update_movie.count = count
        update_movie.save()
        messages.success(request,'Movie Update Succeessfully!')
        context = {
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,
        }
        return render(request,'MovieTicketBooking/adminpage.html',context)

@method_decorator(login_required, name = 'dispatch')
class RemoveMovie(View):
    template_name = 'MovieTicketBooking/removemovie.html'

    def get(self,request,*args,**krgs):
        context = {
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,
        }
        return render(request,self.template_name,context)

    def post(self,request,*args,**krgs):
        name = request.POST['no']
        removemovie = ShowTiming.objects.get(id=name)
        removemovie.delete()
        messages.success(request,'Movie Removed Succeessfully!')
        context = {
        'movie':Movies.objects.all(),
        'Theater':Theater.objects.all(),
        'Show':ShowTiming.objects.all(),
        'admin':True,
        }
        return render(request,'MovieTicketBooking/adminpage.html',context)
