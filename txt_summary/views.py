from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests,urllib3
from bs4 import BeautifulSoup
from .farwell import *
from .lstm_summary import *
from .tokens import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from text_summarizer.settings import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage

# Create your views here.

def index(request):
    
    return render(request, 'index.html', {})

def signup(request):
    
    if request.method == 'POST':
        
        un = request.POST.get('username')
        print(un,end='\n')
        fn = request.POST.get('fname')
        ln = request.POST.get('lname')
        email = request.POST.get('email')
        passw = request.POST.get('pass1')
        passwc = request.POST.get('pass2')
        
        if User.objects.filter(email=email):
            
            messages.error(request,message="Email Already Exists")
            return redirect('index')
        
        if passw!=passwc:
            
            messages.error(request,message="pass conf err")
            return redirect('index')
        
        Uu = User.objects.create_user(username=un,email=email,password=passw)
        Uu.first_name = fn
        Uu.last_name = ln
        Uu.is_active = False
        Uu.save()
        
        
        
        messages.success(request,message="you did it and now there is your account has been created")
        
        cs = get_current_site(request)  
        subject = 'Welcoming and Activating Your Account'
        message = render_to_string('email_conf.html',{'name':Uu.first_name+Uu.last_name,
                                                      'domain':cs.domain,
                                                      'uid':urlsafe_base64_encode(force_bytes(Uu.pk)),
                                                      'token':generate_token.make_token(Uu)})
        
        final_email = EmailMessage(subject,message,EMAIL_HOST_USER,[EMAIL_HOST_USER])
        final_email.fail_silently=True
        final_email.send()
        # send_mail(subject, message, from_email, recipient_list)
        return render(request,'login.html',{'message':"Please Activate Your Account"})
    
    return render(request, 'signup.html', {})

def activate(request,token,uidb64):
    
        
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        Uu=User.objects.get(pk=uid)
        
    except:
        
        Uu = None
        
    if Uu is not None and generate_token.check_token(Uu,token):
        Uu.is_active = True
        Uu.save()
        return HttpResponse('Activated Successfully')
        
    else:
        render(request,'fail.html')
        
def logain(request):
    
    if request.method == 'POST':
        
        un = request.POST.get('username')
        password = request.POST.get('password')

        Uu=authenticate(username=un,password=password)
        if Uu is not None :
            login(request,Uu)
            messages.success(request,message="you did it and now you logged in")
            return render(request,'prog.html',{'message':"hello world"})
        else:
            messages.error(request,"wrong credentials")
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})
        # return redirect('login')
        
    
    


def signout(request):
    
    logout(request)
    return redirect('index')


def get_params_abstract(request):
    
    return render(request, 'parameter_selection_abstract.html', {'message':"hello world abstract"})

def get_params_abstract(request):
    
    return render(request, 'parameter_selection_abstract.html', {'message':"hello world abstract"})



def get_params_abstract(request):

    return render(request, 'parameter_selection_abstract.html', {'message':"hello world abstract"})

def get_params_abstract2(request):
    
    return render(request, 'parameter_selection_abstract2.html', {'message':"hello world abstract"})

def get_params(request):

    return render(request, 'parameter_selection.html', {'message':"hello world"})





def lsa1(doc ,num_sentences = 2,num_topics = 3,sv_threshold = 0.5):
    sum_texts=''
    for docy in doc:
        snt =doc_to_sent(docy)
        norm_snt=normalize_all_document(snt)
        dt_matrix ,td_matrix , vocab=Tfidf_Vectorizer (norm_snt)
        summarized_text=Latent_Semantic_Analysis(td_matrix,snt,num_sentences ,num_topics,sv_threshold )+'\n'
        sum_texts=sum_texts+summarized_text
    return  {'message': sum_texts}


def function4_logic(rt):

    articles=[]
    no = int(rt.GET.get('no')) 
    article_url = rt.GET.get('article_url')  
    
    i=no
    print(i)
    website = article_url
    r = requests.get(website)
    r_html = r.text
    soup = BeautifulSoup(r_html, features="html.parser")
    if website=="https://www.skynewsarabia.com/":
        headlines = soup.find_all('a',{'class':'comp_1_item_inner_cont'})
    elif website=="https://alwatan.sy/" :
        headlines = soup.find_all('a',{'class':'all-over-thumb-link'})
    elif website=="https://www.almayadeen.net/" :
        headlines = soup.find_all('a',{"class":"media-figure"})

    elif website=="https://imn.iq/" :
        headlines = soup.find_all('a',{"class":"img-cont"})

    elif website=="https://www.bbc.com/arabic" :
        headlines = soup.find_all('a',{"class":"focusIndicatorDisplayInlineBlock"})
        
    
    if(i<=len(headlines)):
        samir=[]
        for item in headlines[:i]:

            
            samir.append(website.replace('/arabic','')+item.get('href').replace(website,""))

            # samir.append(website+item.get('href'))

        for url in samir:
            paragraphs=""
            http = urllib3.PoolManager()
            

            html = http.request('GET', url)

            html2=html.data

            htmlParse = BeautifulSoup(html2, 'html.parser')

            for para in htmlParse.find_all("p"):
                # if '::post' in para.get_text():
                    # continue
                paragraphs=paragraphs+para.get_text()
            
            articles.append(paragraphs)
        return articles
            
      
def prog(request):
    print("1")
    response_data = {}
    
    action = request.GET.get('action')
    
    # tts = request.GET.get('textarea')
    

    print("2")
    
    
        
    
    if action =='f4':
        
        global arcs_list
        arcs_list=function4_logic(request)
        response_data = {'message':arcs_list}

        # tts='\n**************************************************************************\n'.join(arcs_list)

    elif action == 'a1':
             
        absprm1 = request.GET.get('absprm1')
        absprm2 = request.GET.get('absprm2')
        absprm3 = request.GET.get('absprm3')
        absprm4 = request.GET.get('absprm4')
        absprm5 = request.GET.get('absprm5')
        absprm6 = request.GET.get('absprm6')
        
        print("assad allah alenrahim")
        print(len(arcs_list))
        print(len(arcs_list))
        print((arcs_list))
        print((arcs_list))
        print("assad allah alenrahim")
        
        response_data = {'message':mbart_summary_list(arcs_list,"https://1c23-34-125-152-123.ngrok-free.app/process",'7','5000','100','3.0','0.5')}

        
    elif action == 'a2':  
        
        abs2prm1 = request.GET.get('abs2prm1')
        abs2prm2 = request.GET.get('abs2prm2')
        abs2prm3 = request.GET.get('abs2prm3')
        abs2prm4 = request.GET.get('abs2prm4')
        abs2prm5 = request.GET.get('abs2prm5')
        abs2prm6 = request.GET.get('abs2prm6')
        print(abs2prm1)
        print(abs2prm2)
        print(abs2prm3)
        
        print(abs2prm1)
        print(abs2prm1)
        response_data = {'message':'hhhhhh'}#mbart_summary_list(arcs_list,"https://1c23-34-125-152-123.ngrok-free.app/process",'7','5000','100','3.0','0.5')}
    
    elif action == 'f1':

        param1 = request.GET.get('param1')
        param2 = request.GET.get('param2')
        param3 = request.GET.get('param3')
        response_data = lsa_list(arcs_list,num_sentences = int(param1),num_topics = int(param2),sv_threshold = float(param3)) 
        # response_data={'message':tts+'        '+param1+'       '+param2}
        # response_data = lsa(tts)
        
    elif action == 'f7':

        param1 = request.GET.get('param1')
        response_data = sents_simi_list(arcs_list,num_sentences = int(param1))

    # elif action == 'f3':
    #     response_data = mbart_summary_list(arcs_list,"https://1d62-34-28-227-51.ngrok-free.app/process",'7','5000','100','3.0','0.5')

    elif action == 'f6':

        t1 = request.GET.get('textarea2')
        t2 = request.GET.get('textarea3')
        res = evaluate(t1,t2)
        response_data = {'message':res}
        
    print(response_data)
 
    return render(request, 'prog.html', response_data)





