from django.http import QueryDict

SERVER_TYPE_CLIENT = 1
SERVER_TYPE_CENTRAL = 2

def get_PUT_data(request):
    data = QueryDict(request.body)
    return data
