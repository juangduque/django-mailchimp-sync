from django.shortcuts import render, redirect
from .forms import UploadNewFileForm
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from io import TextIOWrapper
import csv

API_KEY = "9c514b6cead3fca2b6e7078a39899139-us21"
SERVER_PREFIX = "us21"
LIST_ID = "c71779671d"

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": API_KEY,
    "server": SERVER_PREFIX
})

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        csv_file_wrapper = TextIOWrapper(csv_file, encoding='utf-8')
        # Use Python's built-in CSV library to read the file
        csv_reader = csv.DictReader(csv_file_wrapper)
        headers = csv_reader.fieldnames
        email_header = "email"
        for row in csv_reader:
            email = row.get(email_header)
            merge_fields = {}
            # For each row, extract the necessary fields (e.g. email, first name, last name)
            for header in headers:
                merge_fields[header] = row.get(header)
            try:
                response = client.lists.add_list_member(
                    LIST_ID,
                    {
                        "email_address": email,
                        "status": "subscribed",
                        "merge_fields": merge_fields
                    }
                )
                print("response:")
                print(response)
            except ApiClientError as e:
                # Handle any errors that occur
                print("An error occurred: {}".format(e.text))
                return redirect('upload_error')
        return redirect('success')
    else:
        form = UploadNewFileForm()
    return render(request, 'upload.html', {'form': form})

def connection_check(request):
    is_error = False
    response = None
    try:
        response = client.ping.get()
        response2 = client.lists.get_all_lists()
        for list in response2['lists']:
            print(list['name'], list['id'])
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        is_error = True
    return render(request, 'connection_check.html', {
        'response': response,
        'is_error': is_error,
    })

def success(request):
    return render(request, 'success.html')

def upload_error(request):
    return render(request, 'error_upload.html')