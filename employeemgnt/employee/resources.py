from employee.models import EmployeeInfo, EmployeeAddress
from import_export import resources, fields
import csv, datetime
from import_export.widgets import ForeignKeyWidget
from django.http import HttpResponse
#from django.contrib import messages

class EmployeeInfoResource(resources.ModelResource):
    __onlyTemplate=False
    district = fields.Field(
        column_name='district2',
        attribute='EmployeeAddress',
        widget=ForeignKeyWidget(EmployeeAddress, 'district')
    )
    class Meta:
        model = EmployeeInfo
        #fields = ('id', 'name', 'email', 'contact')
        exclude = ('created', 'updated')
        #import_id_fields = ('id')
        #export_order = ('')

    def requireOnlyTemplate(self):
        self.__onlyTemplate=True
        return

    def isRequiredOnlyTemplate(self):
        return self.__onlyTemplate

    def get_export_headers(self):
        return super().get_export_headers()

    def __process_file(self, data=[]):
        # employee = EmployeeInfo()
        filename = EmployeeInfo.__name__ + '_' + str(datetime.datetime.now()) + '.csv'
        response = HttpResponse('', content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        # writer.writerow(EmployeeInfo.getHeaderMap())
        writer = csv.writer(response)
        writer.writerow(self.get_export_headers())
        #raise Exception(self.get_export_headers())
        if (len(data)):
            # write more line if data found
            for row in data:
                writer.writerow(row)
        return response

    def exportCustom(self, queryset=None, *args, **kwargs):
        if self.isRequiredOnlyTemplate():
            dataset = []
        else:
            dataset = super().export()
        # raise Exception(dataset[0])
        return self.__process_file(dataset)
class EmployeeAddressResource(resources.ModelResource):
    __onlyTemplate=False
    name = fields.Field(
        column_name='name',
        attribute='employeeInfo',
        widget=ForeignKeyWidget(EmployeeInfo, 'name')
    )
    email = fields.Field(
        column_name='email',
        attribute='employeeInfo',
        widget=ForeignKeyWidget(EmployeeInfo, 'email')
    )
    contact = fields.Field(
        column_name='contact',
        attribute='employeeInfo',
        widget=ForeignKeyWidget(EmployeeInfo, 'contact')
    )
    gender = fields.Field(
        column_name='gender',
        attribute='employeeInfo',
        widget=ForeignKeyWidget(EmployeeInfo, 'gender')
    )
    bloodGroup = fields.Field(
        column_name='bloodGroup',
        attribute='employeeInfo',
        widget=ForeignKeyWidget(EmployeeInfo, 'bloodGroup')
    )
    class Meta:
        model = EmployeeAddress
        #fields = ('id', 'name', 'email', 'contact')
        exclude = ('created', 'updated', 'employeeInfo')
        #import_id_fields = ('id')
        export_order = ('id', )

    def requireOnlyTemplate(self):
        self.__onlyTemplate=True
        return

    def isRequiredOnlyTemplate(self):
        return self.__onlyTemplate

    def get_export_headers(self):
        return super().get_export_headers()

    def __process_file(self, data=[]):
        # employee = EmployeeInfo()
        filename = EmployeeInfo.__name__ + '_' + str(datetime.datetime.now()) + '.csv'
        response = HttpResponse('', content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        # writer.writerow(EmployeeInfo.getHeaderMap())
        writer = csv.writer(response)
        writer.writerow(self.get_export_headers())
        #raise Exception(self.get_export_headers())
        if (len(data)):
            # write more line if data found
            for row in data:
                writer.writerow(row)
        return response

    def exportCustom(self, queryset=None, *args, **kwargs):
        if self.isRequiredOnlyTemplate():
            dataset = []
        else:
            dataset = super().export()
        # raise Exception(dataset[0])
        return self.__process_file(dataset)

