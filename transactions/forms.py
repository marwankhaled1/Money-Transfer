from django import forms


class TransferForm(forms.Form):
    sender_account_id = forms.CharField(label='Sender Account ID',max_length=100,required=True)
    receiver_account_id = forms.CharField(label='Receiver Account ID',max_length=100,required=True)
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2,required=True)


