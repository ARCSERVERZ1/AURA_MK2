from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from DEM.serializers import transactions_data_Serializer
from rest_framework.response import Response
from DEM.models import *
from django.db.models import Sum
import pytz , json
from datetime import datetime, timedelta
from DEM.dem_run import *
import os
from django.db.models import Sum


# Create your views here.
@api_view(['POST'])
def datalog_transaction_table(request, count, user, date):
    if request.method == 'POST':
        print(count)
        print(request.data)
        table_data = transactions_data_Serializer(data=request.data)
        print(table_data)
        if table_data.is_valid():
            if count == 1:
                transactions_data.objects.filter(user=user, date=date).exclude(payment_method='Manual_Entry').delete()
            table_data.save()
            return Response(table_data.data, status=201)
        return Response(table_data.errors, status=400)


def get_month_dates():
    ist_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    today = ist_date.today()
    today = str(today).split(' ')[0]
    startdate = str(today).split('-')
    MonthStartDate = str(startdate[0]) + '-' + str(startdate[1]) + '-01'
    return MonthStartDate,today
    # return '2024-02-01' , '2024-02-29'


def dem_dashboard(request):
    current_user = request.user.username
    # get group data
    month_start_date, today = get_month_dates()
    monthly_table_selecion = 'all-records'
    ist_date = datetime.now(pytz.timezone('Asia/Kolkata'))

    monthly_table = transactions_data.objects.filter(user=current_user, date__range=[month_start_date, today])

    group_data = groupdata.objects.filter(user=current_user)

    result = transactions_data.objects.filter(
        user=current_user , date__range=(month_start_date, today),
    ).exclude(
        category__in=['Investment&Savings', 'DEBT-OUT','Repay']# Exclude rows where category is 'investment'
    ).aggregate(
        total_spent =Sum('amount')  # Aggregate the sum of amounts
    )
    category_data = category.objects.values_list('category',flat = True)

    set_budget = budget.objects.filter(user=current_user , date = str(ist_date.strftime("%B %Y"))).values_list('budget', flat=True)
    try:
        budget_set = set_budget[0] # index out of range handling
    except:
        budget_set = 0


    if request.method == 'POST':
        get_cat_trans = request.POST['get_cat_trans']
        if get_cat_trans != 'all-records':
            monthly_table = transactions_data.objects.filter(user=current_user, date__range=[month_start_date, today],
                                                             category=get_cat_trans)
            monthly_table_selecion = get_cat_trans

    total_spent = result.get('total_spent', 0)
    print("-------------------------",total_spent)

    context = {
        'group_data': group_data,
        'monthly_table': monthly_table,
        'monthly_table_selecion': monthly_table_selecion ,
        'total_spent':total_spent,
        'category_data':category_data,
        'set_budget':budget_set,
        'avail_to_spend':int(budget_set)-total_spent
    }

    return render(request, 'dem_dashboard.html', context)


def non_cat_trans(request):
    current_user = request.user.username
    month_start_date, today = get_month_dates()

    group_data = groupdata.objects.filter(user=current_user)
    monthly_table = transactions_data.objects.filter(user=current_user, date__range=[month_start_date, today],
                                                     category='Others')
    context = {
        'group_data': group_data,
        'monthly_table': monthly_table
    }

    return render(request, 'dem_dashboard.html', context)


@api_view(['GET'])
def plot_graph(requests, group_type):
    current_user = requests.user.username
    month_start_date, today = get_month_dates()
    group_dict = {
        'cate-view': 'category',
        'day-view': 'date',
        'group-view': 'group'
    }
    print(month_start_date , today)
    categorywise_data = transactions_data.objects.filter(date__range=[month_start_date, today], user=current_user).values(
        group_dict[group_type]).annotate(sum_category=Sum('amount'))
    spend_cat, spend_val = [], []
    for i in categorywise_data:
        spend_cat.append(i[group_dict[group_type]])
        spend_val.append(i['sum_category'])
    context = {
        'labels': spend_cat,
        'values': spend_val,
    }
    return JsonResponse(context, safe=False)


def update_group(requests):
    if requests.method == 'POST':
        ist_date = datetime.now(pytz.timezone('Asia/Kolkata'))
        # getdata
        group_name = requests.POST['group_name']
        grp_start_date = requests.POST['group_sdate']
        grp_end_date = requests.POST['group_edate']
        current_user = requests.user.username

        # check group conditions
        # if any group falls in the middle overwright
        # half group strat time end time chnages

        # update data for data table
        group_update_set = transactions_data.objects.filter(date__range=[grp_start_date, grp_end_date],
                                                            user=current_user)
        # Update the desired column
        group_update_set.update(group=group_name)

        # then update group table
        data = groupdata(
            user=current_user,
            Time_stamp=ist_date,
            grp_start=grp_start_date,
            grp_end=grp_end_date,
            grp_name=group_name,
            remarks='NA',
            entry_type='Manual'
        )
        data.save()

    return redirect('/dem/')


@api_view(['GET'])
def run_datalog(request, sdate, edate):
    data = {
        "hello": "jarvis"
    }
    print("-----rundata log------------", edate)

    try:
        startdate = datetime.strptime(sdate, "%Y-%m-%d")
        enddate = datetime.strptime(edate, "%Y-%m-%d")
        step = timedelta(days=1)
        while startdate <= enddate:
            print('inside ddatalog')
            current_directory = os.getcwd()
            print("Current directory:", current_directory)
            GetSpendings(request.user.username, ['Phone_pe', 'Axis_credit'],
                         str(startdate.strftime("%Y-%m-%d")), ).get_all_transaction()
            startdate = startdate + step
        return JsonResponse({"hello": "Completed"}, safe=False)

    except Exception as e:
        print(e)
        return JsonResponse({"hello": e}, safe=False)


def delete_log(requests , id):
    try:
        print(f"delete log requested for id : {id}")
        transactions_data.objects.filter(id = id , user= requests.user.username).delete()
        # return dem_dashboard(requests)
        return JsonResponse({'response': 'success'}, safe=False)
    except:
        return JsonResponse({'response':'failed'} , safe=False)


def multiple_edit(request , data , ids):
    print(data , ids)
    id_list_temp = ids.split(',')
    id = []
    for i in id_list_temp:
        id.append(i.split('-')[1])

    data = transactions_data.objects.filter(id__in=id).update(category=data)

    return JsonResponse({'response': 'success'}, safe=False)


def add_new_transaction(request):

    json_data = json.loads(request.body)
    ist_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    print(json_data)
    new_data = transactions_data(
        user=request.user.username,
        date=json_data['date'],
        transaction_type='Sent',
        amount=json_data['amount'],
        sender_bank=json_data['from_bank'],
        receiver_bank=json_data['to_bank'],
        message=json_data['message'],
        category=json_data['category'],
        sub_category=json_data['sub'],
        group=json_data['group'],
        payment_method='Manual_Entry',
        data_ts=ist_date.today(),
    )
    if json_data['action'] == 'new':
        print("new request to save")
        new_data.save()

    elif json_data['action'] == 'edit':
        data = transactions_data.objects.filter(id = json_data['id'])

        data.update(
            date=json_data['date'],
            transaction_type='Sent',
            amount=json_data['amount'],
            sender_bank=json_data['from_bank'],
            receiver_bank=json_data['to_bank'],
            message=json_data['message'],
            category=json_data['category'],
            sub_category=json_data['sub'],
            group=json_data['group'],
            payment_method='Edited',
        )
        print("edit request")

    return JsonResponse({'response': 'success'}, safe=False)

def get_data_by_id(request, id):
    print(f"get data by id for id {id}")
    q1 = transactions_data.objects.filter(id = id)

    print(q1[0].amount)

    data = {
        'id':q1[0].id ,
        'date' : q1[0].date,
        'amount' : q1[0].amount,
        'sender_bank' : q1[0].sender_bank,
        'receiver_bank' : q1[0].receiver_bank,
        'message' : q1[0].message,
        'category' : q1[0].category,
        'sub_category' : q1[0].sub_category,
        'group' : q1[0].group,

    }


    return JsonResponse(data, safe=False)


def set_budget(request ,set_budget):


    ist_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    user = request.user.username
    date = ist_date.strftime("%B %Y")
    #
    #
    print("----------------date",date)

    budget.objects.filter(user=user, date=date).delete()

    budget_data = budget(
        user=user ,
        date = str(date) ,
        budget= int(set_budget),
        updated_time_stamp = ist_date.today()

    )

    budget_data.save()


    data = {
        'response':f"Budget added as {int(set_budget)}",

    }
    print("set budget")
    return JsonResponse(data, safe=False)