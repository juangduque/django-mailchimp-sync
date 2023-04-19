from django.shortcuts import render
from .forms import UploadNewFileForm

def upload_csv(request):
    if request.method == 'POST':
        form = UploadNewFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    else:
        form = UploadNewFileForm()
    return render(request, 'upload.html', {'form': form})