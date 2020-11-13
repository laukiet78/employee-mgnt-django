from django.db import models
#from _datetime import datetime

#DISTRICT = ("barisal", "Barisal"),("bhola", "Bhola"),("jhalokati", "Jhalokati"),("patuakhali", "Patuakhali"),("pirojpur", "Pirojpur"),("bandarban", "Bandarban"),("brahmanbaria", "Brahmanbaria"),("chandpur", "Chandpur"),("chittagong", "Chittagong"),("comilla", "Comilla"),("cox-s-bazar", "Cox's Bazar"),("feni", "Feni"),("khagrachhari", "Khagrachhari"),("lakshmipur", "Lakshmipur"),("noakhali", "Noakhali"),("rangamati", "Rangamati"),("dhaka", "Dhaka"),("faridpur", "Faridpur"),("gazipur", "Gazipur"),("gopalganj", "Gopalganj"),("jamalpur", "Jamalpur"),("kishoreganj", "Kishoreganj"),("madaripur","Madaripur"),("manikganj", "Manikganj"),("munshiganj", "Munshiganj"),("mymensingh","Mymensingh"),("narayanganj", "Narayanganj"),("narsingdi", "Narsingdi"),("netrakona", "Netrakona"),("rajbari", "Rajbari"),("shariatpur", "Shariatpur"),("sherpur", "Sherpur"),("tangail", "Tangail"),("bagerhat", "Bagerhat"),("chuadanga", "Chuadanga"),("jessore", "Jessore"),("jhenaidah", "Jhenaidah"),("khulna", "Khulna"),("kushtia", "Kushtia"),("magura", "Magura"),("meherpur", "Meherpur"),("narail", "Narail"),("satkhira", "Satkhira"),("bogra", "Bogra"),("joypurhat", "Joypurhat"),("naogaon", "Naogaon"),("natore", "Natore"),("nawabganj", "Nawabganj"),("pabna", "Pabna"),("rajshahi", "Rajshahi"),("sirajganj", "Sirajganj"),("dinajpur", "Dinajpur"),("gaibandha", "Gaibandha"),("kurigram", "Kurigram"),("lalmonirhat", "Lalmonirhat"),("nilphamari", "Nilphamari"),("panchagarh", "Panchagarh"),("rangpur", "Rangpur"),("thakurgaon", "Thakurgaon"),("habiganj", "Habiganj"),("moulvibazar", "Moulvibazar"),("sunamganj", "Sunamganj"),("Sylhet", "Sylhet")

# Create models here.
class EmployeeInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=14)
    gender = models.CharField(max_length=1, choices=[('m', 'Male'),('f', 'Female')], default='m')
    bloodGroup = models.CharField(max_length=3, choices=[('a+', 'A+'),('a-', 'A-'),('b+', 'B+'),('b-', 'B-'),('ab+', 'AB+'),('ab-', 'AB-'),('o+', 'O+'),('o-', 'O-')], default='a+')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #models.FileField('file')
    #user previously, now using import-export
    # @staticmethod
    # def getHeaderMap():
    #     return ['id','name', 'email', 'contact']
    @staticmethod
    def getPaginationParameter():
        return 'page'
    @staticmethod
    def getRowPerPage():
        return 10
    __employeeAddress = None

    def getEmployeeAddress(self):
        if self.__employeeAddress is None:
            try:
                self.__employeeAddress = EmployeeAddress.objects.get(employeeInfo_id=self.id)
            except:
                self.__employeeAddress = False

        return self.__employeeAddress

    class Meta:
        db_table = "EmployeeInfo"

class EmployeeAddress(models.Model):
    employeeInfo = models.OneToOneField(EmployeeInfo, on_delete=models.CASCADE)
    addressLine1 = models.CharField(max_length=255)
    addressLine2 = models.CharField(max_length=255, null=True, blank=True)
    upazilla = models.CharField(max_length=255)
    district = models.CharField(
        choices=[("barisal", "Barisal"),("bhola", "Bhola"),("jhalokati", "Jhalokati"),("patuakhali", "Patuakhali"),("pirojpur", "Pirojpur"),("bandarban", "Bandarban"),("brahmanbaria", "Brahmanbaria"),("chandpur", "Chandpur"),("chittagong", "Chittagong"),("comilla", "Comilla"),("cox-s-bazar", "Cox's Bazar"),("feni", "Feni"),("khagrachhari", "Khagrachhari"),("lakshmipur", "Lakshmipur"),("noakhali", "Noakhali"),("rangamati", "Rangamati"),("dhaka", "Dhaka"),("faridpur", "Faridpur"),("gazipur", "Gazipur"),("gopalganj", "Gopalganj"),("jamalpur", "Jamalpur"),("kishoreganj", "Kishoreganj"),("madaripur","Madaripur"),("manikganj", "Manikganj"),("munshiganj", "Munshiganj"),("mymensingh","Mymensingh"),("narayanganj", "Narayanganj"),("narsingdi", "Narsingdi"),("netrakona", "Netrakona"),("rajbari", "Rajbari"),("shariatpur", "Shariatpur"),("sherpur", "Sherpur"),("tangail", "Tangail"),("bagerhat", "Bagerhat"),("chuadanga", "Chuadanga"),("jessore", "Jessore"),("jhenaidah", "Jhenaidah"),("khulna", "Khulna"),("kushtia", "Kushtia"),("magura", "Magura"),("meherpur", "Meherpur"),("narail", "Narail"),("satkhira", "Satkhira"),("bogra", "Bogra"),("joypurhat", "Joypurhat"),("naogaon", "Naogaon"),("natore", "Natore"),("nawabganj", "Nawabganj"),("pabna", "Pabna"),("rajshahi", "Rajshahi"),("sirajganj", "Sirajganj"),("dinajpur", "Dinajpur"),("gaibandha", "Gaibandha"),("kurigram", "Kurigram"),("lalmonirhat", "Lalmonirhat"),("nilphamari", "Nilphamari"),("panchagarh", "Panchagarh"),("rangpur", "Rangpur"),("thakurgaon", "Thakurgaon"),("habiganj", "Habiganj"),("moulvibazar", "Moulvibazar"),("sunamganj", "Sunamganj"),("Sylhet", "Sylhet")],
        max_length=255,
    )
    zip = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #user previously, now using import-export
    # @staticmethod
    # def getHeaderMap():
    #     return ['id','name', 'email', 'contact']
    @staticmethod
    def getPaginationParameter():
        return 'page'

    @staticmethod
    def getRowPerPage():
        return 10
    class Meta:
        db_table = "EmployeeAddress"