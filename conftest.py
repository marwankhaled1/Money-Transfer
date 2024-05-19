import pytest
from accounts.models import Account

@pytest.fixture
def create_accounts(db):
    sender = Account.objects.create(Account_ID='sender123', Name='Sender', Balance=1000)
    receiver = Account.objects.create(Account_ID='receiver123', Name='Receiver', Balance=500)
    return sender, receiver

@pytest.fixture
def client_with_accounts(client, create_accounts):
    return client
