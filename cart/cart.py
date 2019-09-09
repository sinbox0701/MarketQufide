from decimal import Decimal
from django.conf import settings
from shop.models import Product, Option
from django.shortcuts import get_object_or_404
from coupon.models import *

# session을 사용하는 방식 -> request.session에 데이터를 저장하고 꺼내오기
# session에 값을 저장 -> 키 값 설정 -> settings.py에 CART_ID라는 변수를 만들고 설정된 값을 사용
class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        ##self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        option_ids = self.cart.keys()
        options = Option.objects.filter(id__in=option_ids)

        for option in options:
            self.cart[str(option.id)]['product'] = option.product
            self.cart[str(option.id)]['option'] = option

        for item in self.cart.values():
            item['price'] = Decimal(item['product'].price*(100-item['product'].sale_percent)/100*10/10) + Decimal(item['option'].add_price)
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def add(self, product, option, quantity=1, is_update=False):
        product_id = str(product.id)
        option_id= str(option.id)
        if option_id not in self.cart:
            self.cart[option_id] = {'quantity':0, 'price':str(product.price)}

        if is_update:
            self.cart[option_id]['quantity'] = quantity
        else:
            self.cart[option_id]['quantity'] += quantity
        self.save()

    def save(self): # 상품을 담기
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def remove(self, product, option): # 상품을 지우기
        option_id = str(option.id)
        if option_id in self.cart:
            del(self.cart[option_id])
            self.save()

    def clear(self): # 장바구니 비우기 (주문완료에도 사용예정)
        self.session[settings.CART_ID] = {}
        ##self.session['coupon_id'] = None
        self.session.modified = True

    def get_product_total(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

    '''@property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None'''

    '''def get_discount_total(self):
        if self.coupon:
            if self.get_product_total() >= self.coupon.amount:
                return self.coupon.amount
        return Decimal(0)'''

    def get_total_price(self):
        return self.get_product_total()
