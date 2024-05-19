import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from accounts.models import Account
from transactions.models import Transfer


@pytest.fixture
def create_accounts(db):
    sender = Account.objects.create(Account_ID='sender123', Balance=1000)
    receiver = Account.objects.create(Account_ID='receiver123', Balance=500)
    return sender, receiver

