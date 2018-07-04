from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import datetime
from models import Bill, BillDetail

class CheckoutForm(forms.Form):

    full_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(required=True)
    note = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CheckoutForm, self).__init__(*args, **kwargs)

    def save(self):
        full_name = self.cleaned_data.get('full_name')
        phone = self.cleaned_data.get('phone')
        address = self.cleaned_data.get('address')
        note = self.cleaned_data.get('note')
        user = self.request.user
        total =  self.request.session['CART']['total_price']

        bill = Bill(full_name=full_name, phone=phone, address=address, note=note, total=total, user_id=user.id)
        bill.save()

        self.save_bill_detail(bill=bill)

    def save_bill_detail(self, bill):
        for item in self.request.session['CART']['items']:
            quantity = item['quantity']
            unit_price = item['price']
            product_id = item['id']
            bill_id = bill.id
            bill_detail = BillDetail(quantity=quantity, unit_price=unit_price, product_id=product_id, bill_id=bill_id)
            bill_detail.save()