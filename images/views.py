from django.shortcuts import render, redirect
from .forms import ImageCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            print (cd['url'])
            # create a new images instance but prevent the object from being save to database
            new_item = form.save(commit=False)
            print(new_item)
            # assign current user to the new images object
            new_item.user = request.user
            # save the new images object to database
            new_item.save()
            # remind images add successfully
            messages.success(request, 'Image add successfully')
            # redirct to canonical url of new page
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm()
    return render(request, 'images/image/create.html', {'form': form, 'section': 'images'})