from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.template import loader

from explomail.models import Mail, Client
from explomail.serializer import MailSerializer, ClientSerializer
from .forms import SearchForm

import explotext

####
# Browser views
####

def index(request):
    """
    Returns the http response for the main page
    """

    template = loader.get_template('explomail/index.html')
    context = {}

    return HttpResponse(template.render(context, request))

def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            mails_list = Mail.objects.all()
            # Make a query object to collect search criteria
            query = Q()
            if request.POST["client"]:
                client_search = request.POST["client"]
                query = query & Q(sender__icontains=client_search) | Q(receiver__icontains=client_search)

                sender_search = ""
                receiver_search = ""
            else:
                client_search = ""

            if request.POST["text"]:
                body_search = request.POST["text"]
                query = query & Q(text__icontains=body_search)
            else:
                body_search = ""

            # Apply the query
            mails_list = \
                Mail.objects.filter(
                    query
                )

            # Do some statistics
            nr_of_hits = len(mails_list)

            clients = set([m.client_code for m in mails_list])
            nr_of_clients = len(clients)

            dates = []
            ave_search_mail_length = 0
            plot_data = []
            for m in list(mails_list):
                print(m.date)
                pattern_text, polarity, subjectivity, assessments, all_words_found = \
                    explotext.sentiment(m.text, css_class = "sentiment")
                plot_data.append([polarity, subjectivity])
                dates.append(m.date)
                ave_search_mail_length += len(m.text)

            if len(mails_list)> 0:
                ave_search_mail_length = int(ave_search_mail_length / len(mails_list))
            else:
                ave_search_mail_length = 0

            # Load the html template
            template = loader.get_template('explomail/list_mails.html')
            context = {
                'list_mails': mails_list,
                'search_results': True,
                'body_search': body_search,
                'client_search': client_search,
                'plot_data': plot_data,
                'stats': True,
                'nr_of_hits': nr_of_hits,
                'ave_search_mail_length': ave_search_mail_length,
                'client_codes': clients,
                'nr_of_clients': nr_of_clients,
            }
            return HttpResponse(template.render(context, request))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'explomail/search_text.html', {'form': form})


def client_list(request):
    try:
        clients = Client.objects.all()
        
        info_list = []
        plot_data = []
        client_codes = []
        for c in clients:
            mails = c.mail_set.all()

            mail_length = [len(m.text) for m in mails]
            mail_length = int(sum(mail_length)/float(len(mail_length)))

            plot_data.append([len(mails), mail_length])
            info_list.append({"name": c.name, \
                "id": c.id,\
                "ave_length": mail_length, \
                "nr_mails":len(mails)})
            client_codes.append(c.name)

    except Client.DoesNotExist:
        return HttpResponse(status=404)

    template = loader.get_template('explomail/list_clients.html')
    context = {
        'clients': clients,
        'info_list': info_list,
        'plot_data': plot_data,
        'client_codes': client_codes
    }
    return HttpResponse(template.render(context, request))


def client_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        client = Client.objects.get(pk=pk)
        mails = client.mail_set.all()
        #print(mails)
        order, mail_length, data = [], [], []

        for m in mails:
            if m.sender == m.client_code:
                order.append(m.chronological_order)
                mail_length.append(len(m.text))
                data.append([m.chronological_order, len(m.text)])
        ave_mail_length = int(sum(mail_length)/float(len(mail_length)))

    except Client.DoesNotExist:
        return HttpResponse(status=404)

    template = loader.get_template('explomail/details_client.html')
    context = {
        'client': client,
        'mails': mails,
        'data': data,
        'order': order,
        'mail_length': mail_length,
        'ave_mail_length': ave_mail_length
    }
    return HttpResponse(template.render(context, request))



def mail_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        mail = Mail.objects.get(pk=pk)
    except Mail.DoesNotExist:
        return HttpResponse(status=404)

    
    pattern_text, polarity, subjectivity, assessments, all_words_found = \
        explotext.sentiment(mail.text, css_class = "sentiment")

    pattern_text = "<style type=\"text/css\"> \
          .sentiment { \
            color: red; \
          }</style>"+pattern_text

    template = loader.get_template('explomail/details_mail.html')
    context = {
        'mail': mail,
        'mail_pattern': pattern_text,
        'polarity':round(polarity, 2),
        'subjectivity':round(subjectivity, 2),
        'assessments':assessments,
        'all_words_found':all_words_found

    }
    return HttpResponse(template.render(context, request))


################################################
# Api views: CLIENTS
################################################
@csrf_exempt
def client_api_pk(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Mail.DoesNotExist:
        return HttpResponse(status=404)

    serializer = ClientSerializer(client)
    return JsonResponse(serializer.data)

@csrf_exempt
def client_api(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        client.delete()
        return HttpResponse(status=204)

@csrf_exempt
def client_search_name_api(request, search_string):
    try:
        
        clients = Client.objects.all().filter(name__icontains=search_string)
    except Client.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ClientSerializer(clients, many=True)
        return JsonResponse(serializer.data, safe=False)

################################################
# Api views: MAILS
################################################
@csrf_exempt
def mail_api(request):
    if request.method == 'GET':
        mail = Mail.objects.all()
        serializer = MailSerializer(mail, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        mail.delete()
        return HttpResponse(status=204)

@csrf_exempt
def mail_search_text_api(request, search_string):
    try:
        mails = Mail.objects.all().filter(text__icontains=search_string)
    except Mail.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = MailSerializer(mails, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def api_search(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        mails_list = Mail.objects.all()
        # Make a query object to collect search criteria
        query = Q()
        if "sender" in data.keys():
            sender_search = data["sender"]
            query = query & Q(sender__icontains=sender_search)
        if "receiver" in data.keys():
            receiver_search = data["receiver"]
            query = query & Q(receiver__icontains=receiver_search)
        if "text" in data.keys():
            body_search = data["text"]
            query = query & Q(text__icontains=body_search)

        # Apply the query
        mails_list = \
            Mail.objects.filter(
                query
            )

        serializer = MailSerializer(mails_list, many=True)
        return JsonResponse(serializer.data, safe=False)
