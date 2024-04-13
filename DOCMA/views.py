from django.shortcuts import render
import os
from datetime import datetime
from .models import *
from django.contrib.auth.models import User, auth


# Create your views here.


def doc_viewer(request, type):
    q1 = docma.objects.filter(type=type)

    static_folder = 'assets/'
    doc_path = 'Documents/' + type
    upload_dir = static_folder + doc_path
    if os.path.exists('AURA_MK2'):
        print("cloud")
        upload_dir = 'AURA_MK2/' + upload_dir
    else:
        print("local")
        pass
    files = os.listdir(upload_dir)
    files = [file for file in files if os.path.isfile(os.path.join(upload_dir, file))]

    viewer = {}
    for i in q1:
        path = []
        print(i.holder, i.refnumber, i.end_date)
        reg_pattern = i.holder + '_' + i.refnumber
        print("id", i.id)
        for file in files:
            if file.find(reg_pattern) != -1:
                path.append([doc_path + '/' + file, file.split('.')[-1]])

        viewer[i.holder] = {
            'doc_id': i.id,
            'refnum': i.refnumber,
            'valid': i.end_date,
            'file_path': path,

        }

    print(viewer)

    context = {
        'data': viewer

    }
    # context = {
    #     'data' : {
    #     'Avinash': {
    #         'refnum': 'EWGPB8035L',
    #         'valid': datetime.now().date(),
    #         'file_path': ['Avinash_EWGPB8035L_1_jpg.jpg', 'Avinash_EWGPB8035L_2_jpg.jpg']},
    #     'Sanjay': {
    #         'refnum': '12345',
    #         'valid': datetime.now().date(),
    #         'file_path': ['Sanjay_12345_1_png.png']}
    #     }
    # }

    return render(request, "Docma_viewer.html", context)


def doc_manger_home(request):
    # document_type = doc_type.objects.values_list('type', flat=True)
    document_type = docma.objects.values_list('type', flat=True).distinct()
    context = {
        'doc_type': document_type
    }
    print(context)
    return render(request, "docma_home.html", context)


def add_document(request):
    document_holders = doc_holder.objects.values_list('Holder', flat=True)
    document_type = doc_type.objects.values_list('type', flat=True)
    print(document_holders, "-----------------------------------------")
    context = {
        'document_holders': document_holders,
        'document_type': document_type
    }

    return render(request, "doc_manager.html", context)


def doc_manager(request):
    document_holders = doc_holder.objects.values_list('Holder', flat=True)
    document_type = doc_type.objects.values_list('type', flat=True)
    print(document_holders, "-----------------------------------------")
    context = {
        'document_holders': document_holders,
        'document_type': document_type
    }

    return render(request, "docma_home.html", context)
    # return render(request, "doc_manager.html" , context)


def doc_manager_save(request):
    if request.method == 'POST':

        docName = request.POST['docName']
        docType = request.POST['docType']
        refNum = request.POST['refNum']
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']

        remarks = request.POST['remarks']
        value = request.POST['value']
        static_folder = 'assets/'
        doc_path = 'Documents/' + docType
        upload_dir = static_folder + doc_path
        print(docName, docType, refNum, sDate, sDate, eDate, remarks, value)
        counter = 0

        if os.path.exists('AURA_MK2'):
            print("cloud")
            upload_dir = 'AURA_MK2/' + upload_dir
        else:
            print("local")
            pass

        for file in request.FILES.getlist('file'):
            counter = counter + 1
            if not os.path.exists(upload_dir): os.makedirs(upload_dir)
            name = docName + '_' + refNum + '_' + str(counter) + '_' + str(file.name).split('.')[-1] + '.' + \
                   str(file.name).split('.')[-1]
            with open(os.path.join(upload_dir, name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        data = docma(holder=docName,
                     refnumber=refNum,
                     document=upload_dir + '/' + docName + refNum + str(counter),
                     end_date=eDate,
                     date=sDate,
                     value=value,
                     type=docType,
                     time_stamp=datetime.now(),
                     remarks=remarks,
                     updated_by=request.user.username
                     )

        if 'file_b' in request.FILES:
            data.document_back = request.FILES['file_b']
        else:
            print("file not present --------------------------")

        data.save()
    return render(request, "doc_manager.html")


def save_uploaded_file(file):
    # Define the directory where you want to save the uploaded files
    upload_dir = 'path/to/save/files/'
    if not os.path.exists(upload_dir): os.makedirs(upload_dir)
    with open(os.path.join(upload_dir, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
