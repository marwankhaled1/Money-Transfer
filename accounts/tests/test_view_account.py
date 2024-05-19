import pytest
from django.urls import reverse

""""
1. Test View Account
"""

# test Account_Detail
@pytest.mark.django_db
def test_detail_view(client_with_accounts, create_accounts):
    sender, _ = create_accounts
    response = client_with_accounts.get(reverse('account_detail', args=[sender.Account_ID]))
    assert response.status_code == 200
    assert response.context['account'] == sender

@pytest.mark.django_db
def test_detail_view_non_existent_account(client_with_accounts):
    response = client_with_accounts.get(reverse('account_detail', args=[999]))
    assert response.status_code == 404
