from django.shortcuts import render, redirect
from django.http import Http404
#from django.views.generic import TemplateView
#from django.views import View
from employee.forms import EmployeeInfoForm, EmployeeAddressForm
from employee.models import EmployeeInfo, EmployeeAddress
from employee.resources import EmployeeInfoResource, EmployeeAddressResource
#import sys, os
import os, io, csv, datetime
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib import messages

def http404(request, exception):
    return render(request, '404.html')

#@login_required()
def show(request):
    paginator = Paginator(EmployeeInfo.objects.all().order_by('-updated'), EmployeeInfo.getRowPerPage())
    if EmployeeInfo.getPaginationParameter() in request.GET:
        page_obj = paginator.page(int(request.GET[EmployeeInfo.getPaginationParameter()]))
    else:
        page_obj = paginator.page(1)
    return render(request, 'employee/show.html', {'page_obj' : page_obj, 'employees' : page_obj.object_list})

def add(request):
    if request.method == "POST":
        info_form = EmployeeInfoForm(request.POST)
        address_form = EmployeeAddressForm(request.POST)
        if info_form.is_valid() and address_form.is_valid():
            try:
                employeeInfo = info_form.save()
                employeeAddress = address_form.instance
                employeeAddress.employeeInfo = employeeInfo
                employeeAddress.save()
                return redirect('employee:show')
            except Exception as e:
                info_form.add_error(None, str(e))

    else:
        info_form = EmployeeInfoForm()
        address_form = EmployeeAddressForm()
    return render(request, 'employee/add.html', {'info_form': info_form, 'address_form': address_form})

def edit(request, id):
    # a shorcut for try/catch
    # employee = get_object_or_404(EmployeeInfo, $id)
    try:
        employeeInfo = EmployeeInfo.objects.get(id=id)
        info_form = EmployeeInfoForm(instance=employeeInfo)
        employeeAddress = employeeInfo.getEmployeeAddress()
        address_form = EmployeeAddressForm(instance=employeeAddress if employeeAddress else None)
        #return HttpResponse(info_form.name)
    except EmployeeInfo.DoesNotExist:
        raise Http404("Information does not exist")
    return render(request, 'employee/edit.html', {'employeeInfo': employeeInfo, 'info_form' : info_form, 'address_form': address_form})


def update(request, id):
    try:
        employeeInfo = EmployeeInfo.objects.get(id=id)
    except EmployeeInfo.DoesNotExist:
        raise Http404("Information does not exist")
    info_form = EmployeeInfoForm(request.POST, instance=employeeInfo)
    employeeAddress = employeeInfo.getEmployeeAddress()
    address_form = EmployeeAddressForm(request.POST, instance=employeeAddress if employeeAddress else None)
    if info_form.is_valid() and address_form.is_valid():
        try:
            employeeInfo = info_form.save()
            employeeAddress = address_form.instance
            employeeAddress.employeeInfo = employeeInfo
            employeeAddress.save()
            return redirect('employee:show')
        except Exception as e:
            info_form.add_error(None, str(e))

    return render(request, 'employee/edit.html', {'employeeInfo': employeeInfo, 'info_form' : info_form, 'address_form' : address_form})


def destroy(request, id):
    try:
        employee = EmployeeInfo.objects.get(id=id)
    except EmployeeInfo.DoesNotExist:
        raise Http404("Information does not exist")
    employee.delete()
    return redirect('employee:show')



def download(request, template=''):
    employeeInforResource = EmployeeAddressResource()
    if template != '':
        employeeInforResource.requireOnlyTemplate()
    return employeeInforResource.exportCustom()

def __xprocess_file(data=[]):
        # employee = EmployeeInfo()
        filename = EmployeeInfo.__name__ + '_' + str(datetime.datetime.now()) + '.csv'
        response = HttpResponse('', content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        # writer.writerow(EmployeeInfo.getHeaderMap())
        writer = csv.writer(response)
        writer.writerow(EmployeeInfo.getHeaderMap())
        if (len(data)):
            # write more line if data found
            for row in data:
                writer.writerow(row)
        return response

def xdownload(request):
    return __process_file()

def upload(request):
    template = "employee/upload.html"
    #check if form has been posted
    if request.method == "POST":
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Only CSV file is allowed')
            return render(request, template)
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        omitCounter=0;createdCounter=0;updatedCounter=0
        for column in csv.reader(io_string, delimiter=','):
            #raise Exception(column[1])
            if (column[1] =='' or column[2] == ''or column[3] == ''or column[4] == ''or column[5] == ''or column[6] == ''or column[8] == ''or column[9] == ''or column[10] == ''):
                omitCounter += 1
                # return HttpResponse(column[6])
                # raise Exception(column)
                continue
            id = int(column[0]) if column[0] else None
            try:
                if id:
                    employeeAddress = EmployeeAddress.objects.get(id=id)
                    employeeInfo_id = employeeAddress.employeeInfo_id
                    EmployeeInfo.objects.filter(id=employeeInfo_id).update(name=column[1], email=column[2], contact=column[3], gender=column[4], bloodGroup=column[5])
                    updatedCounter += 1
                else:
                    employeeInfo = EmployeeInfo.objects.create(name=column[1], email=column[2], contact=column[3], gender=column[4], bloodGroup=column[5])
                    employeeInfo_id = employeeInfo.id
                    createdCounter += 1

                exist, new = EmployeeAddress.objects.update_or_create(
                    id=id,
                    defaults={'employeeInfo_id': employeeInfo_id, 'addressLine1': column[6], 'addressLine2': column[7], 'upazilla': column[8], 'district': column[9], 'zip': column[10]}
                )
            except Exception as e:
                omitCounter +=1
                continue
        message = 'File Uploaded and Executed Successfully.'
        if omitCounter:
            message += ' Omitted '+str(omitCounter)+' rows(s).'
        if createdCounter:
            message += ' Created '+str(createdCounter)+' rows(s).'
        if updatedCounter:
            message += ' Updated '+str(updatedCounter)+' rows(s).'
        messages.success(request, message)
        return render(request, template)
    return render(request, template, {
        'upload_message': 'Order of the CSV should be name, email, contact. The gender column should be m/f (male/female). District/blood group name should be in lower case and space would be replaced by "-".',
    })