import pytest
from django.urls import reverse

""""
1. Test List Accounts
"""

# test Cases for AccountList
@pytest.mark.django_db
def test_list_view(client_with_accounts):
    response = client_with_accounts.get(reverse('account_list'))
    assert response.status_code == 200
    assert len(response.context['accounts']) == 2  # Initial 2 accounts
