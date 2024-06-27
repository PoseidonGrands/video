from django.shortcuts import render


def index(request):
    print('index...')
    return render(request, 'dashboard/index_base.html')


