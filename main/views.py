from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .models import User, Assignment
from .forms import UserRegisterForm, UserLoginForm, AssignmentForm
import hashlib

def default(request):
    return render(request, 'main/default.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = User.objects.filter(username=username, password=hashed_password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['user_type'] = user.user_type
                request.session['is_superuser'] = user.is_superuser
                return redirect('assignments')
            else:
                return render(request, 'main/login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        return User.objects.get(id=user_id)
    return None

def assignments_list(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    if user.is_superuser:
        assignments = Assignment.objects.all()
    else:
        assignments = user.assignments.all()

    return render(request, 'main/assignments_list.html', {'assignments': assignments, 'user_type': user.user_type})

def assignment_detail(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return HttpResponseNotFound("Assignment not found")

    students = assignment.students.all()

    return render(request, 'main/assignment_detail.html', {'assignment': assignment, 'students': students})

def assignment_create(request):
    user = get_current_user(request)
    if not user or not user.is_superuser:
        return redirect('login')

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            form.save_m2m()
            return redirect('assignments')
    else:
        form = AssignmentForm()

    return render(request, 'main/assignment_form.html', {'form': form, 'is_edit': False})

def assignment_update(request, pk):
    user = get_current_user(request)
    if not user or not user.is_superuser:
        return redirect('login')

    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return HttpResponseNotFound("Assignment not found")

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'main/assignment_form.html', {'form': form, 'is_edit': True})

def assignment_delete(request, pk):
    user = get_current_user(request)
    if not user or not user.is_superuser:
        return redirect('login')

    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return HttpResponseNotFound("Assignment not found")

    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')

    return render(request, 'main/assignment_delete_confirm.html', {'assignment': assignment})