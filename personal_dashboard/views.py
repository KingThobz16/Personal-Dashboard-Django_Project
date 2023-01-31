from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia

# Create your views here.
def home(request):
    return render(request, 'personal_dashboard/home.html')


# 
# 
# 
"""Notes related views"""
# Note creating View
def notes(request):
    # Check if the request is post and create note
    if request.method == ('POST'):
        form = NotesForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            # save information on Notes table
            notes.save()
        # To display success or error message at the top of the page
        messages.success(request, f'Note Added by {request.user.username} Successfully!')
    else:
        form = NotesForm()
    
    # filtering notes by logged in user
    notes = Notes.objects.filter(user=request.user)
    context = {
        'notes' : notes,
        'form' : form,
    }
    return render(request, 'personal_dashboard/notes.html', context) 

# Note detail page
class NotesDetailView(generic.DetailView):
    model = Notes
    
    

# Note deleting view
def delete_note(request, pk=None):
    # In the Notes database table, delete the note with the id=pk
    Notes.objects.get(id=pk).delete()
    # redirect to notes page
    return redirect('personal_dashboard-notes')
    

# 
# 
# 
# 
# 
# 
"""Homework related views"""
# Homework view
def homework(request):
    # Check if the request is post and create homework
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            try:
                finished = request.POST('is_finished')
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished,
            
        )
        homeworks.save()
        messages.success(request, 'Homework added successfully')
    else:
        form = HomeworkForm()
    
    # filtering homework by logged in user
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
        
    context = {
        'homeworks' : homeworks,
        'homework_done' : homework_done,
        'form' : form,
    }
    
    return render(request, 'personal_dashboard/homework.html', context)


# To update homework and mark it finished or not finished
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    # Save information in database and redirect to homework
    homework.save()        
    return redirect('personal_dashboard-homework')
    
    
    
# Delete homework view
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('personal_dashboard-homework')
    
    

# 
# 
# 
# 
# 
# 
"""Youtube related views"""
# Youtube creating view
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        # get the search text data from the request
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form' : form,
                'results' : result_list
            }
            
        return render(request, 'personal_dashboard/youtube.html', context)
        
           
    else:
        form = DashboardForm()
        
    form = DashboardForm()
    context = {
        'form' : form,
    }
    return render(request,  'personal_dashboard/youtube.html', context)

# 
# 
# 
# 
# 
# 
# 
# 
# 
"""todo related views"""
# todo creating view
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            try:
                finished = request.POST('is_finished')
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished,
        )
        todos.save()
        messages.success(request, 'Todo added successfully')
    else:
        form = TodoForm()
        
    todos = Todo.objects.filter(user=request.user)
    
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
        
    context = {
        'todos' : todos,
        'form' : form,
        'todos_done' : todos_done
    }
    return render(request, 'personal_dashboard/todo.html', context)

# To update homework and mark it finished or not finished
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    # Save information in database and redirect to homework
    todo.save()        
    return redirect('personal_dashboard-todo')

# Delete todo view
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('personal_dashboard-todo')


# 
# 
# 
# 
# 
# 
# 
# 
# 
"""books related views"""
# books creating view
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        # get the search text data from the request
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        res = requests.get(url)
        answer = res.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'description' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink'),
                
            }
            result_list.append(result_dict)
            context = {
                'form' : form,
                'results' : result_list
            }
            
        return render(request, 'personal_dashboard/books.html', context)
        
           
    else:
        form = DashboardForm()
        
    form = DashboardForm()
    context = {
        'form' : form,
    }
    return render(request,  'personal_dashboard/books.html', context)

# 
# 
# 
# 
# 
# 
# 
# 
# 
"""Dictionary related views"""
# Dictionary creating view
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        # get the search text data from the request
        text = request.POST['text']
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        res = requests.get(url)
        answer = res.json()
        result_list = []

        try:
            phonetics = answer[0]['phonetics'][0]['text'],
            audio = answer[0]['phonetics'][1]['audio'],
            definition = answer[0]['meanings'][0]['definitions'][0]['definition'],
            example = answer[0]['meanings'][0]['definitions'][0]['example'],
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms'],
            context = {
                'form' : form,
                'input' : text,
                'phonetics' : phonetics,
                'definition' : definition,
                'example' : example,
                'synonyms' : synonyms,
                 
            }
        except:
            context = {
                'form' : form,
                'input' : text,                 
            }
        return render(request, 'personal_dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form' : form,             
        }       
            
    return render(request, 'personal_dashboard/dictionary.html', context)

# 
# 
# 
# 
# 
# 
# 
# 
# 
"""Wiki related views"""
# Wiki creating view
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text);
        context = {
            'form' : form,
            'title' : search.title,
            'link' : search.url,
            'details' : search.summary,  
        }
        
        return render(request, 'personal_dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form' : form
        }
    return render(request, 'personal_dashboard/wiki.html', context)

# 
# 
# 
# 
# 
# 
# 
# 
# 
"""conversion related views"""
# conversion creating view
def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form' : form,
                'm_form' : measurement_form,
                'input' : True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                # Checking if the following input is not null and is an integer
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input) * 3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input) / 3} yard'
                        
                context = {
                    'form' : form,
                    'm_form' : measurement_form,
                    'input' : True,
                    'answer' : answer
                }
                
                
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form' : form,
                'm_form' : measurement_form,
                'input' : True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                # Checking if the following input is not null and is an integer
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input) * 0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} foot = {int(input) * 2.2062} yard'
                        
                context = {
                    'form' : form,
                    'm_form' : measurement_form,
                    'input' : True,
                    'answer' : answer
                }
                    
    else:
        form = ConversionForm()
        context = {
            'form' : form,
            'input' : False,
        }
    
    return render(request, 'personal_dashboard/conversion.html', context)