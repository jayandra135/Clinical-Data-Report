from django.shortcuts import render
from capp.models import Patient, ClinicalData
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from capp.forms import ClinicalDataForm
from django.shortcuts import redirect,render
# Create your views here.
class PatientListView(ListView):
    model=Patient

class PateintCreateView(CreateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstname','lastname','age')

class PateintUpdateView(UpdateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstname','lastname','age')

class PateintDeleteView(DeleteView):
    model=Patient
    success_url=reverse_lazy('index')

def addData(request,**kwargs):
    form = ClinicalDataForm()
    patient  =Patient.objects.get(id=kwargs['pk'])
    if request.method=='POST':
        form=ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request,'capp/clinicaldata_form.html',{'form':form,'patient':patient})


def anaylze(request,**kwargs):
    data = ClinicalData.objects.filter(patient_id=kwargs['pk'])
    responseData = []
    for eachEntry in data:
        if eachEntry.componentName == 'hw':
            heightAndWeight = eachEntry.componentValue.split('/')
            if len(heightAndWeight) > 1:
                feeToMetres = float(heightAndWeight[0]) * 0.4536
                BMI = (float(heightAndWeight[1]))/(feeToMetres*feeToMetres)
                bmiEntry = ClinicalData()
                bmiEntry.componentName='BMI'
                bmiEntry.componentValue=BMI
                responseData.append(bmiEntry)
        responseData.append(eachEntry)


    return render(request,'capp/generatereport.html',{'data':responseData})
