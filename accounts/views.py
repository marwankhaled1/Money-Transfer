from django.shortcuts import render
from .forms import UploadFileForm
from .models import Account
from django.views.generic import ListView,DetailView
from django.contrib import messages
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_format = file.name.split('.')[-1]

            if file_format == 'csv':
                df = pd.read_csv(file)
            elif file_format in ['xls', 'xlsx']:
                df = pd.read_excel(file)
            elif file_format == 'json':
                json_data = file.read().decode('utf-8')
                df = pd.read_json(json_data)
            else:
                messages.error(request, 'Unsupported file format')
                return render(request, 'accounts/upload.html', {'form': form})

            if not {'ID', 'Name', 'Balance'}.issubset(df.columns):
                messages.error(request, 'Required columns (ID, Name, Balance) not found in the file.')
                return render(request, 'accounts/upload.html', {'form': form})

            
            df.columns = df.columns.str.strip()
            existing_accounts = Account.objects.in_bulk(field_name='Account_ID')

            accounts_to_update = []
            accounts_to_insert = []

            for index, row in df.iterrows():
                account_id = str(row['ID']).strip()
                name = str(row['Name']).strip()
                balance = float(row['Balance'])

                if account_id in existing_accounts:
                    account = existing_accounts[account_id]
                    account.Name = name
                    account.Balance = balance
                    accounts_to_update.append(account)
                else:
                    accounts_to_insert.append(Account(Account_ID=account_id, Name=name, Balance=balance))

            if accounts_to_update:
                Account.objects.bulk_update(accounts_to_update, ['Name', 'Balance'])
            if accounts_to_insert:
                Account.objects.bulk_create(accounts_to_insert)

            messages.success(request, 'Data successfully uploaded to the database.')
        else:
            messages.error(request, 'Invalid form submission. Please check your file.')

    else:
        form = UploadFileForm()
    return render(request, 'accounts/upload.html', {'form': form})



class AccountListView(ListView):
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 10



class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounts/account_detail.html'
    context_object_name = 'account'