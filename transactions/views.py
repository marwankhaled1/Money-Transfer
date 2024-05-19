from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TransferForm
from .models import Account, Transfer

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TransferForm
from .models import Account, Transfer

def transfer_money(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        print("does form is valid:" ,form.is_valid())
        # check if form is valid
        if form.is_valid():
            sender_account_id = form.cleaned_data["sender_account_id"]
            receiver_account_id = form.cleaned_data["receiver_account_id"]
            amount = form.cleaned_data["amount"]
        

            # the db not empty
            if Account.objects.exists():
                
                # try to check sender and receiver in db or not 
                try:
                    sender_account = Account.objects.get(Account_ID=sender_account_id)
                except Account.DoesNotExist:
                    messages.error(request, "Sender account ID does not exist.")
                    return redirect("transfer_money")

                try:
                    receiver_account = Account.objects.get(Account_ID=receiver_account_id)
                except Account.DoesNotExist:
                    messages.error(request, "Receiver account ID does not exist.")
                    return redirect("transfer_money")
                


                # check the amout of money and not negative or zero
                if amount <= 0:
                    messages.error(request, "Amount must be a positive number.")
                elif sender_account.Balance < amount:
                    messages.error(request, "Insufficient balance.")
                else:
                    sender_account.Balance -= amount
                    sender_account.save()

                    receiver_account.Balance += amount
                    receiver_account.save()

                    Transfer.objects.create(
                        sender=sender_account, receiver=receiver_account, amount=amount
                    )

                    messages.success(request, "Money transferred successfully.")
                    return redirect("transfer_money")
            
            # empty db
            else:
                messages.error(request, "No accounts found in the database. Please upload data first.")
    
        # not valid data or empty 
        else:   
            messages.error(request, "Please fill out all fields with Correct Data.")
            return redirect("transfer_money")
    
    else:
        form = TransferForm()
    return render(request, "transfer.html", {"form": form})

