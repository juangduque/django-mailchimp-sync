from django.shortcuts import render
from .forms import UploadNewFileForm
import csv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": "9c514b6cead3fca2b6e7078a39899139-us21",
    "server": "us21"
})

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

def connection_check(request):
    is_error = False
    response = None
    try:
        response = client.ping.get()
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        is_error = True
    return render(request, 'connection_check.html', {
        'response': response,
        'is_error': is_error,
    })