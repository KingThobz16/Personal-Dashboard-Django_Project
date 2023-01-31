from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='personal_dashboard-home'),
    # Notes section urls
    path('notes/', views.notes, name='personal_dashboard-notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete-note'),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name='notes-detail'),
    
    # Homework section urls
    path('homework/', views.homework, name='personal_dashboard-homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),

    # Youtube section urls
    path('youtube/', views.youtube, name='personal_dashboard-youtube'),
 
    # Todo section urls
    path('todo/', views.todo, name='personal_dashboard-todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update-todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),

    # Books section urls
    path('books/', views.books, name='personal_dashboard-books'),

    # dictionary section urls
    path('dictionary/', views.dictionary, name='personal_dashboard-dictionary'),

    # Wiki section urls
    path('wiki/', views.wiki, name='personal_dashboard-wiki'),

    # Wiki section urls
    path('conversion/', views.conversion, name='personal_dashboard-conversion'),
 

]