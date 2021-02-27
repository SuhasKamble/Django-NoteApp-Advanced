from django.shortcuts import render, HttpResponse, redirect
from home.models import Note
from django.contrib import messages

# Create your views here.


def Home(request):
    allNotes = Note.objects.all()
    context = {"allNotes": allNotes}
    return render(request, 'home.html', context)


def Search(request):
    query = request.POST.get("query")
    noteTitle = Note.objects.filter(title__icontains=query)
    noteSummary = Note.objects.filter(summary__icontains=query)
    allNotes = noteTitle.union(noteSummary)
    context = {"allNotes": allNotes, "query": query}

    return render(request, 'search.html', context)


def createNote(request):
    if request.method == "POST":
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        slug = summary[0:10]
        slug = slug.split(" ")
        slug = "-".join(slug)
        note = Note(title=title, summary=summary, content=content, slug=slug)
        note.save()
        messages.success(request, 'Note has been successfully added.')
        return redirect('/')

    return render(request, 'createNote.html')


def deleteNote(request):
    if request.method == "POST":
        deleteId = request.POST.get("deleteId")
        Note.objects.filter(id=deleteId).delete()
        messages.success(request, "Note has been successfully deleted")
        return redirect("/")

    return HttpResponse("Not Note")


def editNote(request):
    if request.method == "POST":
        noteId = request.POST.get("editId")
        note = Note.objects.filter(id=noteId).first()
        Note.objects.filter(id=noteId).delete()
        context = {"note": note}
        return render(request, 'createNote.html', context)

    return HttpResponse("This is Edit")


def myNote(request, slug):
    note = Note.objects.filter(slug=slug).first()
    context = {"note": note}
    return render(request, 'note.html', context)
