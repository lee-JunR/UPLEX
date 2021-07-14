from django.http import HttpResponse
from django.shortcuts import render
import json, requests

# Create your views here.
def web_request(method_name, url, dict_data, is_urlencoded=True):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
    method_name = method_name.upper()  # 메소드이름을 대문자로 바꾼다
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')

    if method_name == 'GET':  # GET방식인 경우
        response = requests.get(url=url, params=dict_data)
    elif method_name == 'POST':  # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})

    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else:  # 문자열 형태인 경우
        return {**dict_meta, **{'text': response.text}}

def login(request):
    if request.method == 'POST':
        print('리퀘스트 로그'+str(request.body))
        id = request.POST.get('userid','')
        pw = request.POST.get('userpw','')
    return render(request, "accounts/login.html")

def signup(request):
    if request.method == 'POST':
        print('리퀘스트 로그' + str(request.body))
        username = request.POST.get('userid', '')
        password = request.POST.get('userpw', '')
        pw2 = request.POST.get('userpw2', '')
        print(username, password, pw2)
        if password == pw2:
            json_signup = {}
            json_signup["username"] = username
            json_signup["password"] = password
            url = 'http://211.250.90.12:3030/api/auth/register/'  # 접속할 사이트주소 또는 IP주소를 입력한다
            data = json_signup  # 요청할 데이터
            # data = {"username":"test123","password":"testword123"}
            print(data)
            response = web_request(method_name='POST', url=url, dict_data=data)
            return HttpResponse('success')
    return render(request, "accounts/signup.html")
