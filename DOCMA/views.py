from django.shortcuts import render
import os
from datetime import datetime
from .models import *
from django.http import JsonResponse
import json, os
from django.contrib.auth.models import User, auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
import string, random


# Create your views here.


def encrypt_value(value):
    x = 0
    rand = str(random.randint(1000000, 9999999))
    rand = [i for i in rand]
    for index, digit in enumerate(rand):
        if index in [2, 5, 8]:
            rand.insert(index, str(value)[x])
            x = x + 1
    return ''.join([i for i in rand])


def doc_viewer(request, type):
    q1 = docma.objects.filter(type=type)

    static_folder = 'assets/'
    doc_path = 'Documents/' + type
    upload_dir = static_folder + doc_path
    # if os.path.exists('AURA_MK2'):
    #     print("cloud")
    #     upload_dir = 'AURA_MK2/' + upload_dir
    # else:
    #     print("local")
    #     pass

    if os.path.exists('Local'):
        print("Local")
    else:
        upload_dir = 'AURA_MK2/' + upload_dir
        print("cloud")
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

        viewer[str(i.holder) + str(i.id)] = {
            'doc_id': i.id,
            'refnum': i.refnumber,
            'valid': i.end_date,
            'file_path': path,
        }

    print(viewer)

    context = {
        'data': viewer

    }

    return render(request, "Docma_viewer.html", context)


@login_required()
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


@login_required()
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

        if os.path.exists('Local'):
            print("Local")
        else:
            upload_dir = 'AURA_MK2/' + upload_dir
            print("cloud")
            pass

        for file in request.FILES.getlist('file'):
            counter = counter + 1
            if not os.path.exists(upload_dir): os.makedirs(upload_dir)
            name = docName + '_' + refNum + '_' + str(counter) + '_' + str(file.name).split('.')[-1] + '.' + \
                   str(file.name).split('.')[-1]
            with open(os.path.join(upload_dir, name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        enc_value = ''
        if docType == 'Bank_Cards':
            enc_value = encrypt_value(value)
        else:
            enc_value = value

        data = docma(holder=docName,
                     refnumber=refNum,
                     document=upload_dir + '/' + docName + refNum + str(counter),
                     end_date=eDate,
                     date=sDate,
                     value=enc_value,
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


def test(request):
    return render(request, "test.html")


def add_doc_type(request, new_doc_type):
    print(doc_type)
    document_type = doc_type.objects.values_list('type', flat=True)
    print("--------------", document_type)
    if new_doc_type not in document_type:
        print("-----insode---------", document_type)
        new = doc_type(
            type=new_doc_type
        )
        new.save()
        context = {
            'result': 'data added:  ' + str(new_doc_type)
        }
    else:
        context = {
            'result': 'duplicate data:  ' + str(new_doc_type)
        }

    print("addd doc")
    return JsonResponse(context, safe=False)


def delete_data_by_id(requests, id):
    try:
        q1 = docma.objects.filter(id=id)
        old_data = {}
        for i in q1:
            old_data = {
                'doc_id': i.id,
                'holder': i.holder,
                'refnum': i.refnumber,
                'valid': i.end_date,
                'file_path': i.document,
                'type': i.type
            }
        static_folder = 'assets/'
        doc_path = 'Documents/' + old_data['type']
        upload_dir = static_folder + doc_path

        if os.path.exists('Local'):
            print("Local-here")
        else:
            upload_dir = 'AURA_MK2/' + upload_dir
            print("cloud")
            pass
        print("-------------", upload_dir)
        files = os.listdir(upload_dir)
        files = [file for file in files if os.path.isfile(os.path.join(upload_dir, file))]
        reg_pattern = old_data['holder'] + '_' + old_data['refnum']
        for file in files:
            if file.find(reg_pattern) != -1:
                os.remove(upload_dir + '/' + file)

        docma.objects.filter(id=id).delete()

        context = {'result': 'True'}
    except:
        context = {'result': 'False'}
    return JsonResponse(context, safe=False)


def get_data_by_id(request, id):
    print(f"get data by id for id {id}")
    q1 = docma.objects.filter(id=id)
    data = {
        'id': q1[0].id,
        'name': q1[0].holder,
        'type': q1[0].type,
        'ref': q1[0].refnumber,
        'sdate': q1[0].date,
        'edate': q1[0].end_date,
        'value': q1[0].value,
        'remarks': q1[0].remarks
    }

    return JsonResponse(data, safe=False)


def add_edit_document(requests):
    new_data = json.loads(requests.body)
    print(new_data)

    q1 = docma.objects.filter(id=new_data['id'])
    old_data = {}
    for i in q1:
        old_data = {
            'doc_id': i.id,
            'holder': i.holder,
            'refnum': i.refnumber,
            'valid': i.end_date,
            'file_path': i.document,
            'type': i.type
        }
    static_folder = 'assets/'
    doc_path = 'Documents/' + old_data['type']
    upload_dir = static_folder + doc_path
    new_doc_path = static_folder + 'Documents/' + new_data['type']

    if os.path.exists('Local'):
        print("Local-here")
    else:
        upload_dir = 'AURA_MK2/' + upload_dir
        new_doc_path = 'AURA_MK2/' + new_doc_path
        print("cloud")
        pass
    print(upload_dir)

    # save in db
    data = docma.objects.filter(id=new_data['id'])

    enc_value = ''
    if new_data['type'] == 'Bank_Cards':
        enc_value = encrypt_value(new_data['value'])
    else:
        enc_value = new_data['value']

    data.update(
        holder=new_data['name'],
        refnumber=new_data['ref'],
        document=upload_dir + '/' + new_data['name'] + new_data['ref'],
        end_date=new_data['edate'],
        date=new_data['sdate'],
        value=enc_value,
        type=new_data['type'],
        time_stamp=datetime.now(),
        remarks=new_data['remarks'],
        updated_by=requests.user.username
    )

    print("data updated for docma")

    files = os.listdir(upload_dir)
    files = [file for file in files if os.path.isfile(os.path.join(upload_dir, file))]
    reg_pattern = old_data['holder'] + '_' + old_data['refnum']
    for file in files:
        if file.find(reg_pattern) != -1:
            current_filename = file
            print("cuurent file name :", current_filename)
            split_name = current_filename.split('_')
            new_filename = new_data['name'] + '_' + new_data['ref'] + '_' + split_name[2] + '_' + split_name[3]
            if not os.path.exists(new_doc_path): os.mkdir(new_doc_path)
            os.rename(upload_dir + '/' + current_filename, new_doc_path + '/' + new_filename)

    return JsonResponse({'data': 'ok'}, safe=False)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rag_for_docma(requests):
    print("-----------------------------------------------")
    q1 = docma.objects.all()
    data = list(docma.objects.values())
    for i in q1:
        print(i.refnumber)
    return JsonResponse(data, safe=False)


def home_menu_req():
    # document_type = doc_type.objects.values_list('type', flat=True)
    menu_but = home_menu.objects.all().order_by('app_priority')
    return menu_but
