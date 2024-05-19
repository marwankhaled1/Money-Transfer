import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from accounts.models import Account
from transactions.models import Transfer


""" 
1.check successful transfer 
2.check insufficient_balance
3.check invalid_sender_account
4.check invalid_receiver_account(client)
5.check empty_fields(

"""


# check successful transfer 
@pytest.mark.django_db
def test_successful_transfer(client, create_accounts):
    sender, receiver = create_accounts
    response = client.post(reverse('transfer_money'), {
        'sender_account_id': 'sender123',
        'receiver_account_id': 'receiver123',
        'amount': 200
    })
    assert response.status_code == 302  # redirect
    assert response.url == reverse('transfer_money') 

    # Follow the redirect
    response = client.get(response.url)
    assert response.status_code == 200

    # check balances
    sender.refresh_from_db()
    receiver.refresh_from_db()
    assert sender.Balance == 800
    assert receiver.Balance == 700


@pytest.mark.django_db
def test_insufficient_balance(client, create_accounts):
    sender, receiver = create_accounts
    response = client.post(reverse('transfer_money'), {
        'sender_account_id': 'sender123',
        'receiver_account_id': 'receiver123',
        'amount': 2000
    })
    assert response.status_code == 200  # no redirect

    # Check messages
    messages = list(get_messages(response.wsgi_request))
    assert any("Insufficient balance." in str(message) for message in messages)



@pytest.mark.django_db
def test_invalid_sender_account(client):
    receiver = Account.objects.create(Account_ID='receiver123', Balance=500)
    response = client.post(reverse('transfer_money'), {
        'sender_account_id': 'invalid123',
        'receiver_account_id': 'receiver123',
        'amount': 200
    })
    assert response.status_code == 302  
    assert response.url == reverse('transfer_money')  

    # Follow the redirect
    response = client.get(response.url)
    assert response.status_code == 200

    # check messages
    messages = list(get_messages(response.wsgi_request))
    assert any("Sender account ID does not exist." in str(message) for message in messages)



@pytest.mark.django_db
def test_invalid_receiver_account(client):
    sender = Account.objects.create(Account_ID='sender123', Balance=1000)
    response = client.post(reverse('transfer_money'), {
        'sender_account_id': 'sender123',
        'receiver_account_id': 'invalid123',
        'amount': 200
    })
    assert response.status_code == 302  
    assert response.url == reverse('transfer_money')  

    # follow the redirect
    response = client.get(response.url)
    assert response.status_code == 200

    # check messages
    messages = list(get_messages(response.wsgi_request))
    assert any("Receiver account ID does not exist." in str(message) for message in messages)



@pytest.mark.django_db
def test_empty_fields(client):
    response = client.post(reverse('transfer_money'), {
        'sender_account_id': '',
        'receiver_account_id': '',
        'amount': ''
    })
    assert response.status_code == 302  
    assert response.url == reverse('transfer_money')  

    #follow the redirect
    response = client.get(response.url)
    assert response.status_code == 200

    #check messages
    messages = list(get_messages(response.wsgi_request))
    assert any("Please fill out all fields with Correct Data." in str(message) for message in messages)