from django import forms
from shop.models import Option

class AddProductForm(forms.Form):
    option_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField() # 제품 수량
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    # 상세페이지: 제품 수량 선택 추가 할때 마다 현재 장바구니 수량 더해짐 is_update = False
    # 장바구니페이지: 수량변경은 현재 수량에 반영  is_update = True