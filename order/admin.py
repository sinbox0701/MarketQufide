from django.contrib import admin
import csv
import datetime
from django.http import HttpResponse

# 주문 목록을 CSV로 저장하는 함수
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv') # HttpResponse 객체
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name) # attatchment로 설정하면 파일 다운가능
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV' # 관리자 페이지에 함수 추가할때 기능 이름

from django.urls import reverse
from django.utils.safestring import mark_safe

def order_detail(obj): # 주문 내역 상세보기
    return mark_safe('<a href="{}">Detail</a>'.format(reverse('orders:admin_order_detail', args=[obj.id])))

order_detail.short_description = 'Detail'

#def order_pdf(obj): # PDF로 보기
#    return mark_safe('<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id])))

#order_pdf.short_description = 'PDF'

# mark_safe는 HTML 출력에 이용

from .models import OrderItem, Order

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'orderno', 'email', 'addr1', 'zip', 'addr2', 'paid',
                    order_detail, 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
