In admin site:
user: admin
pw: 123456

my_csv_uploader_app_api_key: 9c514b6cead3fca2b6e7078a39899139-us21

response = client.ping.get()
{'health_status': "Everything's Chimpy!"}


response2 = client.lists.get_all_lists()
for list in response2['lists']:
    print(list['name'], list['id'])
