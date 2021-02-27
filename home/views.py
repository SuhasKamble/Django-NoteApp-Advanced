from django.shortcuts import render, HttpResponse, redirect
from home.models import Note
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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


def handleSignin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get("pass2")

        if len(username) < 2 or len(fname) < 2 or len(lname) < 2 or len(
                email) < 3:
            messages.error(
                request, "Something went wrong, Please fill the for correctly")
            return redirect('/')

        if pass1 != pass2:
            messages.error(
                request,
                "Password do not match, Please fill the for correctly")
            return redirect('/')

            newUser = User.objects.create_user(username, email, pass1)
            newUser.first_name = fname
            newUser.last_name = lname
            newUser.save()
            messages.success(request, "You have been successfully signup")
            return redirect("/")
    return HttpResponse("This is handle signin")


def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logges in")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials, Please try again!")
            return redirect('/')

    return HttpResponse("This is handle login")


def handleLogout(request):
    logout(request)
    messages.success(request, "You have been successfully logged Out")
    return redirect('/')
    return redirect('/')
