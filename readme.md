## Sync your contacts to mailchimp

This is an application to sync your contacts with a csv file as input. Additionally you can also download your contact in .csv format too. This synchronization only works with the fields contained in the csv file passed as [input data](https://docs.google.com/spreadsheets/d/1Zg9C68SxuiZjzsj_Ym5Qh_G-FepfHTfCK0bKyMWLseA/edit#gid=566210249) due to limitations discussed later. I recommend using the files that exist in the csv_loader_files folder. One is the entire file, the other is a slice of this used for test.

### About the project
The application was made in Django (Python) and Bootstrap with some dinamic properties in the html templates.

#### Run the project locally
1.  make sure that you have python and pip installed:
```
python --version
pip --version
```

2. Create and activate a virtual environment:
```
python -m venv venv # In windows
.\venv\Scripts\activate
```
For mac I recommend to read [this guide](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)

3. install the required packages listed in requirements.txt:
```
pip install -r requirements.txt
```

4. Change to the project's directory:
```
cd mailchimpsync
```

5. Migrate the database using:
```
python ./manage.py migrate
```

6. Run a development server:
```
python ./manage.py runserver
```

**And it's done! You should see that the project is running in your terminal**

#### Superuser credentials for admin site
If you want to navigate through the admin site, go to /admin. You can create a new superuser or use the following existence credentials:
**user:** admin
**pw:** 123456

### Considerations

#### Mailchimp service
Mailchimp needs us to have an active account to be able to use it and also the API. Under the free use layer we have limited capacities, these capacities conditioned the development of this application.
##### Limitations:
- It is possible to use only one list of contact.
- Determined quantity of daily operations.
- Some operations are only allowed in other tiers.

#### Mailchimp development
To work with the API is necessary to create an API key, for more information [read this](https://mailchimp.com/es/help/about-api-keys/).
Use the api key to config the client and make the operations that you need.
##### Merge fields
Merge fields let you save custom information about contacts, which can then be used to personalize campaigns. The checks for these are very strict (More info in [here](https://mailchimp.com/developer/marketing/docs/merge-fields/)).

So for this development it is necessary to have into account that we only have one list and the merge fields should have a tag well defined and known.

##### Disclaimer
I am going to publish the api key and the list id of my mailchimp account only for learning purposes. I am not responsible if the improper use of this fact by someone else may affect third parties.
It is possible to use this project with your own credentials just replace the variables specified further with your own credentials and should work.

### The development
First I have to say that i spent several time of this development by trying to understand how mailchimp upload the contact by a csv file as input in the manual approach.
In mailchimpsync\uploadcsv\views.py it is the main core logic for all the application. In there you will see 4 constants declared:
```
API_KEY = YOUR_API_KEY
SERVER_PREFIX = YOUR_SERVER_PREFIX
LIST_ID = YOUR_LIST_ID
DEBUG = True / False
```
API_KEY, SERVER_PREFIX and LIST_ID are fields provided for mailchimp.
DEBUG is for enable some logs throug the application.

To get the list id you can use the following code:
```
response2 = client.lists.get_all_lists()
for list in response2['lists']:
    print(list['name'], list['id'])
```

To check the connection you can run the following code:
```
response = client.ping.get()
{'health_status': "Everything's Chimpy!"}
```

#### The design
Given that the name of the headers of the file is not previously known and these must be validated to create the corresponding tags of the merge fields, 

The first thing i tried was to try creating a new list given the input csv file,Next I leave an example of the possible implementation:

```
def create_new_list():
    try:
        new_list = client.lists.create_list(
            {
                "name": "contact list name",
                "permission_reminder": "permission_reminder",
                "email_type_option": True,
                "contact": {
                    "company": "company",
                    "address1": "address1",
                    "city": "city",
                    "country": "country"
                },
                "campaign_defaults": {
                    "from_name": "from_name",
                    "from_email": "Maud_Lehner27@gmail.com",
                    "subject": "subject",
                    "language": "language"
                }
            }
        )

        print(new_list)
    except ApiClientError as error:
        print("Error: {}".format(error.text))

        # # Add a contact to the new list
        # list_id = new_list["id"]
        # contact_data = {
        #     "email_address": "example@example.com",
        #     "status": "subscribed",
        #     "merge_fields": {
        #         "FNAME": "John",
        #         "LNAME": "Doe"
        #     }
        # }

        # response = client.lists.add_list_member(list_id, contact_data)
        # print(response)
```

##### My merge fields
Since the update is done with the tags of the merge fields of the project, I thought first of making a system for mapping the data that comes from the csv file against the fields of the.

The file headers of the file as set:
```
{
    'First name'
    'Last/Organization/Group/Household name'
    'System record ID'
    'Date changed'
    'Email Addresses\\Email address'
    'Email Addresses\\Date changed'
    'Todays Visitors Attribute\\Value'
    'Todays Visitors Attribute\\Date changed'
    'Addresses\\Address line 1'
    'Addresses\\Address line 2'
    'Addresses\\City'
    'Addresses\\ZIP'
    'Addresses\\State abbreviation'
    'Addresses\\Country abbreviation'
    'Phones\\Number'
    'Phones\\Date changed'
}
```
Printing the following member fetched I realized that the sync should be done with the merge field tags, and is for this reason that the headers only work for this sync file:
```
[{'email_address': 'jturner@socialgoodsoftware.com', 'merge_fields': {'FNAME': '', 'LNAME': '', 'ADDRESS': '', 'PHONE': '', 'BIRTHDAY': '', 'MMERGE6': '', 'MMERGE7': '', 'MMERGE8': '', 'MMERGE9': '', 'MMERGE10': '', 'MMERGE11': '', 'MMERGE12': '', 'MMERGE13': '', 'MMERGE14': '', 'MMERGE15': '', 'MMERGE16': ''}}]
```

I wanted to map the mailchimp header against the merge field tags, but I realized that the operation is complex.
I created the following data structures to understand how I should map the input data and leave it ready to create a new user
```
mailchimp_name_tag_map = {
    "Email Address": "EMAIL",
    "First Name": "FNAME",
    "Last Name": "LNAME",
    "Full address": "MMERGE15",
    "Address - Combined": "ADDRESS",
    "Phone Number": "PHONE",
    "phone creation timestamp": "MMERGE6",
    "Country": "MMERGE7",
    "State abreviation": "MMERGE8",
    "ZIP code": "MMERGE9",
    "System record ID": "MMERGE10",
    "Date changed": "MMERGE11",
    "Email change timestamp": "MMERGE12",
    "Today visitors attribute": "MMERGE13",
    "Today visitors Attribute change timestamp": "MMERGE14",
    "Phone change timestamp": "MMERGE16",
}
```
```
csv_file_headers = [
    'First name', #0
    'Last/Organization/Group/Household name', #1
    'System record ID', #2
    'Date changed', #3
    'Email Addresses\\Email address', #4
    'Email Addresses\\Date changed', #5
    'Todays Visitors Attribute\\Value', #6
    'Todays Visitors Attribute\\Date changed', #7
    'Addresses\\Address line 1', #8
    'Addresses\\Address line 2', #9
    'Addresses\\City', #10
    'Addresses\\ZIP', #11
    'Addresses\\State abbreviation', #12
    'Addresses\\Country abbreviation', #13
    'Phones\\Number', #14
    'Phones\\Date changed' #15
]
```
```
fields_to_data = {
    "Email Address": csv_file_headers[4],
    "First Name": csv_file_headers[0],
    "Last Name": csv_file_headers[1],
    "Full address": csv_file_headers[8] + " " + csv_file_headers[9] + " " + csv_file_headers[10] + " " + csv_file_headers[12] + " " + csv_file_headers[11] + " " + csv_file_headers[13],
    "Phone Number": csv_file_headers[14],
    "Country": csv_file_headers[13],
    "State abreviation": csv_file_headers[12],
    "ZIP code": csv_file_headers[11],
    "System record ID": csv_file_headers[2],
    "Date changed": csv_file_headers[3],
    "Email change timestamp": csv_file_headers[5],
    "Today visitors attribute": csv_file_headers[6],
    "Today visitors Attribute change timestamp": csv_file_headers[7],
    "Phone change timestamp": csv_file_headers[15],
}
```
In the end, I chose to do a direct mapping (You can find it in mailchimpsync\uploadcsv\utils.py the functions is called map_csv_row_to_merge_fields) without so many complications, which limits the fact that new contacts can be created based on only this data from the file.

For future possible improvements we can use this mapping system to upload any type of file regardless of headers.

#### Dealing with errors
The following are logs of errors that happened during the development, some of them could be managed and others are specific to the limitations of mailchimp:

###### Member Exists
To avoid this  error It is validated if the email is already on the list
```
An error occurred: {"title":"Member Exists","status":400,"detail":"rick@socialgoodsoftware.com is already a list member. Use PUT to insert or update list members.","instance":"7f15febe-615f-be8b-9d2b-3e83a243c5f0"}
```

###### Invalid Resource
Mailchimp blocks the register of an email if has several entries registered by them. To solve this i just changed the email. Wait for some time also works.
It's also worth noting that repeatedly attempting to add the same email address in a short period of time may trigger Mailchimp's abuse prevention measures and result in your account being suspended or terminated.
```
An error occurred: {"type":"https://mailchimp.com/developer/marketing/docs/errors/","title":"Invalid Resource","status":400,"detail":"jturne@socialgoodsoftware.com has signed up to a lot of lists very recently; we're not allowing more signups for now","instance":"cd25c7ac-d736-0ab1-78eb-e819d764e827"}
```

###### Resource Not Found
The health of the connection is good but mailchimp prevents us from continuing to trade, most likely because we have exceeded the daily trading quota.
```
An error occurred when checking the existence of contact: {"type":"https://mailchimp.com/developer/marketing/docs/errors/","title":"Resource Not Found","status":404,"detail":"The requested resource could not be found.","instance":"523ddb0e-b9c6-6ebc-a6a2-b69ef91861ce"}
```

###### Key revoked
The error message indicates that the API key being used has been disabled. This could be due to various reasons, such as:

1. The API key has been revoked or invalidated by the user who owns it.
2. The API key was not generated with the proper permissions to perform the requested operation.
3. The API key has been disabled by Mailchimp due to a violation of their terms of service or other policy.
To resolve the issue, you can try the following:

Double-check that you are using the correct API key. Make sure that you have copied and pasted it correctly, and that it is not expired or revoked ([Read more](https://mailchimp.com/es/help/about-api-keys/)).
```
An exception occurred: {"type":"https://mailchimp.com/developer/marketing/docs/errors/","title":"API Key Invalid","status":401,"detail":"API key has been disabled","instance":"802fd30d-9ef1-eaae-3cd5-b779f8aee541"}
```

### My contribution
This project is licensed by [MIT](https://opensource.org/license/mit/). you can copy it, modify it and use it as you wish as long as its purpose is not malicious.

You can contact me and make suggestions of any kind at juangduqued@gmail.com.
