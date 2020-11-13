from django.contrib import admin
from employee.models import EmployeeInfo, EmployeeAddress
from employee.forms import EmployeeInfoForm
from employee.resources import EmployeeInfoResource, EmployeeAddressResource
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin


class EmployeeAddressMap(admin.StackedInline):
    model = EmployeeAddress
    min_num = 1
    max_num = 1
    can_delete = False


class DistrictFilter(admin.SimpleListFilter, EmployeeAddress):
    title = 'District'
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        return (
            ("barisal", "Barisal"), ("bhola", "Bhola"), ("jhalokati", "Jhalokati"), ("patuakhali", "Patuakhali"),
            ("pirojpur", "Pirojpur"), ("bandarban", "Bandarban"), ("brahmanbaria", "Brahmanbaria"),
            ("chandpur", "Chandpur"), ("chittagong", "Chittagong"), ("comilla", "Comilla"),
            ("cox-s-bazar", "Cox's Bazar"), ("feni", "Feni"), ("khagrachhari", "Khagrachhari"),
            ("lakshmipur", "Lakshmipur"), ("noakhali", "Noakhali"), ("rangamati", "Rangamati"), ("dhaka", "Dhaka"),
            ("faridpur", "Faridpur"), ("gazipur", "Gazipur"), ("gopalganj", "Gopalganj"), ("jamalpur", "Jamalpur"),
            ("kishoreganj", "Kishoreganj"), ("madaripur", "Madaripur"), ("manikganj", "Manikganj"),
            ("munshiganj", "Munshiganj"), ("mymensingh", "Mymensingh"), ("narayanganj", "Narayanganj"),
            ("narsingdi", "Narsingdi"), ("netrakona", "Netrakona"), ("rajbari", "Rajbari"),
            ("shariatpur", "Shariatpur"), ("sherpur", "Sherpur"), ("tangail", "Tangail"), ("bagerhat", "Bagerhat"),
            ("chuadanga", "Chuadanga"), ("jessore", "Jessore"), ("jhenaidah", "Jhenaidah"), ("khulna", "Khulna"),
            ("kushtia", "Kushtia"), ("magura", "Magura"), ("meherpur", "Meherpur"), ("narail", "Narail"),
            ("satkhira", "Satkhira"), ("bogra", "Bogra"), ("joypurhat", "Joypurhat"), ("naogaon", "Naogaon"),
            ("natore", "Natore"), ("nawabganj", "Nawabganj"), ("pabna", "Pabna"), ("rajshahi", "Rajshahi"),
            ("sirajganj", "Sirajganj"), ("dinajpur", "Dinajpur"), ("gaibandha", "Gaibandha"), ("kurigram", "Kurigram"),
            ("lalmonirhat", "Lalmonirhat"), ("nilphamari", "Nilphamari"), ("panchagarh", "Panchagarh"),
            ("rangpur", "Rangpur"), ("thakurgaon", "Thakurgaon"), ("habiganj", "Habiganj"),
            ("moulvibazar", "Moulvibazar"), ("sunamganj", "Sunamganj"), ("Sylhet", "Sylhet")
        )

    def queryset(self, request, queryset):
        #match with self.value()
        exclu = []
        for obj in queryset:
            add = EmployeeAddress.objects.get(employeeInfo_id=obj.id)
            if add.district != self.value():
                #queryset.filter(id = obj.id)
                #raise Exception(queryset)
                exclu.append(obj.id)
        return  queryset.exclude(id__in=exclu)

#class EmployeeInfoAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
@admin.register(EmployeeInfo)
class EmployeeInfoAdmin(admin.ModelAdmin):
    form = EmployeeInfoForm
    #resource_class = EmployeeAddressResource

    list_display = (
        'name',
        'email',
        'gender',
        'bloodGroup',
        'district',
        'contact',
        'updated',
    )
    def district(self, obj):
        try:
            result = EmployeeAddress.objects.get(employeeInfo=obj)
            return result.district
        except EmployeeAddress.DoesNotExist:
            return ''

    ordering = ('updated', )
    search_fields = ('name', 'email', 'contact')
    list_filter = (
        'gender',
        'bloodGroup',
        # 'district',
        DistrictFilter,
        'updated',
    )
    list_per_page = 10
    empty_value_display = 'None'
    inlines = [EmployeeAddressMap]

#admin.site.register(EmployeeInfo)
#admin.site.register(EmployeeInfo, EmployeeInfoAdmin)