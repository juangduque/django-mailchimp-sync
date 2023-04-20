from django.shortcuts import render
from .forms import UploadNewFileForm
import csv

def upload_csv(request):
    if request.method == 'POST':
        form = UploadNewFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Read the CSV file into a list of rows
            rows = []
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            headers = next(reader) # Get the headers
            for row in reader:
                rows.append(row)
            # Render the template with the headers and rows
            return render(request, 'csv_table.html', {'headers': headers, 'rows': rows})
    else:
        form = UploadNewFileForm()
    return render(request, 'upload.html', {'form': form})