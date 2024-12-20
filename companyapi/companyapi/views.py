from django.http import HttpResponse , JsonResponse

def home_page(request):
    print("home page requeste")
    friends =[
        'surya',
        'yazu',
        'subham'
    ]
    #return HttpResponse("<h1> This is home page </h1>")
    return JsonResponse(friends,safe=False)