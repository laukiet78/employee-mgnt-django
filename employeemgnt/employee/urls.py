from django.urls import path
from django.conf.urls import handler400
#from . import views
from employee import views as EmployeeView

app_name = 'employee'

urlpatterns = [
    path('add/', EmployeeView.add, name='add'),
    path('show/', EmployeeView.show, name='show'),
    path('edit/<int:id>', EmployeeView.edit, name='edit'),
    path('update/<int:id>', EmployeeView.update, name='update'),
    path('delete/<int:id>', EmployeeView.destroy, name='delete'),
    path('upload/', EmployeeView.upload, name='upload'),
    path('download/', EmployeeView.download, name='download'),
    path('download/<str:template>', EmployeeView.download, name='download'),
    #path('$/', views.show, name='show'),
]
handler404 = 'employee.views.http404'
