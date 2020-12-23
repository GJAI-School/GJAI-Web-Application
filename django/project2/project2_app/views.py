from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def result(request):
    content = request.POST['content']
    result1 = len(content)
    result2 = content.replace(' ','')
    result2 = len(result2)
    return render(request, 'result.html', {'include_space' : result1, 'not_include_space' : result2})