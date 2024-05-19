import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from accounts.models import Account
import pandas as pd
from io import BytesIO
import json

""" 
1. Test Upload file with csv format
2. Test Upload file with xsl format
3. Test Upload file with json format
4. Test Upload file with unsupported format
5. Test Upload with incorrect structure
 
"""

# supported formats
@pytest.mark.django_db
def test_upload_valid_csv(client_with_accounts):
    initial_account_count = Account.objects.count()
    print(f"Initial account count: {initial_account_count}")
    
    csv_content = """ID,Name,Balance
1,ahmed,1000
2,ali,1300
"""
    csv_file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
    response = client_with_accounts.post(reverse('upload_file'), {'file': csv_file})
    
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert any("Data successfully uploaded to the database." in str(message) for message in messages)

   # debug accounts
    accounts = Account.objects.all()
    for account in accounts:
        print(f"Account ID: {account.Account_ID}, Name: {account.Name}, Balance: {account.Balance}")
    

    final_account_count = Account.objects.count()
    print(f"Final account count: {final_account_count}")
    assert final_account_count == initial_account_count + 2



@pytest.mark.django_db
def test_upload_valid_xls(client_with_accounts):
    initial_account_count = Account.objects.count()
    print(f"Initial account count: {initial_account_count}")
    
    df = pd.DataFrame({
        'ID': [1, 2],
        'Name': ['ahmed', 'ali'],
        'Balance': [1000, 1300]
    })
    xls_buffer = BytesIO()
    df.to_excel(xls_buffer, index=False)
    xls_buffer.seek(0)
    
    xls_file = SimpleUploadedFile("test.xls", xls_buffer.read(), content_type="application/vnd.ms-excel")
    response = client_with_accounts.post(reverse('upload_file'), {'file': xls_file})
    
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert any("Data successfully uploaded to the database." in str(message) for message in messages)

    # Debug accounts
    accounts = Account.objects.all()
    for account in accounts:
        print(f"Account ID: {account.Account_ID}, Name: {account.Name}, Balance: {account.Balance}")
    
    final_account_count = Account.objects.count()
    print(f"Final account count: {final_account_count}")
    assert final_account_count == initial_account_count + 2



@pytest.mark.django_db
def test_upload_valid_json(client_with_accounts):
    initial_account_count = Account.objects.count()
    print(f"Initial account count: {initial_account_count}")
    
    # Create a JSON file in memory
    json_content = json.dumps([
        {"ID": 1, "Name": "ahmed", "Balance": 1000},
        {"ID": 2, "Name": "ali", "Balance": 1300}
    ])
    json_file = SimpleUploadedFile("test.json", json_content.encode('utf-8'), content_type="application/json")
    response = client_with_accounts.post(reverse('upload_file'), {'file': json_file})
    
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert any("Data successfully uploaded to the database." in str(message) for message in messages)

    # Debug accounts
    accounts = Account.objects.all()
    for account in accounts:
        print(f"Account ID: {account.Account_ID}, Name: {account.Name}, Balance: {account.Balance}")
    
    final_account_count = Account.objects.count()
    print(f"Final account count: {final_account_count}")
    assert final_account_count == initial_account_count + 2



#unsupported format  
@pytest.mark.django_db
def test_upload_unsupported_format(client_with_accounts):
    unsupported_content = "unsupported content"
    unsupported_file = SimpleUploadedFile("test.txt", unsupported_content.encode('utf-8'), content_type="text/plain")
    response = client_with_accounts.post(reverse('upload_file'), {'file': unsupported_file})
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert any("Unsupported file format" in str(message) for message in messages)

# incorrect structure
@pytest.mark.django_db
def test_upload_missing_columns(client_with_accounts):
    csv_content = """ID,Name1,Alice2,Bob"""
    csv_file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
    response = client_with_accounts.post(reverse('upload_file'), {'file': csv_file})
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert any("Required columns (ID, Name, Balance) not found in the file." in str(message) for message in messages)

