from django.shortcuts import render

def loginView(request):
    if request.method == 'POST':
        user_info = request.POST.get('user_info', None)
        pswd = request.POST.get('pswd', None)

        print("******************************")
        print(f'{user_info} - {pswd}')
    return render(request, 'user/login.html')


