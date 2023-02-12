# -*- encoding: utf-8 -*-


from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def WhatsappMessageWebhook(request):
    dtobj1 = datetime.datetime.utcnow()  # utcnow class method
    dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method
    dtobj_india = dtobj3.astimezone(
    pytz.timezone("Asia/Calcutta"))  # astimezone method 
    dtobj_india = dtobj_india.strftime("%H:%M:%S")
    dtobj_indiaa = str(dtobj_india)
# WHATSAPP_URL = "https://graph.facebook.com/v15.0/107095272246745/messages"
    if request.method == 'GET':
        Verify_token = "2d790a4d-7c9c-4e23-9c9c-5749c5fa7fdb"
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == Verify_token:
            return HttpResponse(challenge,status=200)
        else:
            return HttpResponse('error', status = 403)

    if request.method == "POST":
        data = json.loads(request.body)   
        print("data",data)
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try: 

                    for entry in data ['entry'] : 
                        phoneNumber = entry['changes'] [0] ['value']['metadata']['display_phone_number'] 
                        phoneId = entry['changes'] [0] ['value']['metadata']['phone_number_id'] 
                        profileName = entry['changes'] [0] ['value']['contacts'][0]['profile']['name'] 
                        whatsAppId = entry['changes'] [0]  ['value']['contacts'][0]['wa_id'] 
                        fromId = entry['changes'] [0] ['value']['messages'][0]['from'] 
                        messageId = entry['changes'][0]['value']['messages'][0]['id'] 
                        timestamp = entry['changes'][0]['value']['messages'][0]['timestamp'] 
                        text = entry['changes'][0]['value']['messages'][0]['text']['body'] 
                        # phoneNumber= "918875091601" 
                        message = 'RE : {}was received'.format(text) 
                        new_user_check = Whatsapp_data.objects.filter(Q(user_id=phoneId)).exists()
                        latest_row = Whatsapp_data.objects.filter(user_id=phoneId).latest('id')
                        latest_row2 = Whatsapp_data.objects.filter(user_id=phoneId).order_by('-id')[0]
                        add_record=Whatsapp_data.objects.create(time = dtobj_indiaa, msg_id=messageId,username=profileName,user_id=phoneId ,mobile_number=whatsAppId,response_from_user=text,New_user_check=new_user_check,We_responded_check=False)

                        value = latest_row.response_from_user
                        value2 = latest_row2.response_from_user
                        # objects = Whatsapp_data.objects.all()

                        # for obj in objects:
                        #     print(obj.__dict__)
                        # print("last response",value)
                        # print("last response222",value2)
                        phoneNumber = whatsAppId 
                        
                        if(value == "1" ):
                            print("running 1")
                            try:

                                # result = wiki_content(text)
                                # result = wikipedia.page(text)
                                # result =  result.content
                                # message = result
                                wiki = wikipediaapi.Wikipedia("en")
                                page = wiki.page(text)

                                print(page.summary)
                                message = page.summary
                                # paragraphs = result.split("\n")
                                # first_two_paragraphs = "\n".join(paragraphs[:2])
                                # message = first_two_paragraphs
                                message = message[:4000]
                                print(message)
                                sendWhatsappMessage_chain(phoneNumber,message)
                            except Exception as e:
                                message="Sorry to inform you, Something went wrong!!"
                                sendWhatsappMessage_chain(phoneNumber,message)
                                print(e, "wiki")

                        if(value == "2" ):

                            print("running 2")
                            URL = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
                            response = requests.get(URL).json()
                            print(response)
                            try:
                                word_data = response[0]
                                word = word_data["word"]
                                phonetics = word_data["phonetics"]
                                meanings = word_data["meanings"]
                                result = "Word: " + word_data['word'] + "\n\n"
                                for meaning in word_data['meanings']:
                                    result += "Part of speech: " + meaning['partOfSpeech'] + "\n"
                                    result += "Definitions: \n"
                                    for definition in meaning['definitions']:
                                        result += " - " + definition['definition'] + "\n"
                                    result += "\n"
                            except:
                                result = "Title: " + response['title'] + "\n"
                                result += "Message: " + response['message'] + "\n"
                                result += "Resolution: " + response['resolution']
                                message = result
                                print(message)
                                sendWhatsappMessage_chain(phoneNumber,message)         
                            try:

                                url = "http://127.0.0.1:3001/"

                                payload = json.dumps({
                                "word": text
                                })
                                headers = {
                                'Content-Type': 'application/json',
                                'Cookie': 'csrftoken=HnZ0xkkPTtNNKL0xMWEnFEhZ3ZcbXbxRs87wLRTFeUeR1HJ6OYcR5N4RWYSb5HoJ'
                                }

                                res = requests.request("POST", url, headers=headers, data=payload)
                            # Assuming the JSON string is stored in a variable called 'res.text'

                                # Parse the JSON string into a dictionary
                                data = json.loads(res.text)

                                # Extract the 'sentence' key and its value from the dictionary
                                sentences = data['sentence']

                                # Loop through the sentences and print each one

                                sentence_format = "Sentence {}: {}\n"

                                sentence_string = ""
                                for i, sentence in enumerate(sentences):
                                    sentence_string += sentence_format.format(i+1, sentence)

                                print(sentence_string)
                                message = sentence_string
                                sendWhatsappMessage_chain(phoneNumber,message)                            
                            except Exception as e:
                                print("ERROR : "+str(e))             
                                message = f'Sorry, Didnt find this word, Please give us another chance'
                                print(message)
                                sendWhatsappMessage_chain(phoneNumber,message)        
                            message = f'Thank you {profileName} for using our service, Send Hi to start again'
                            print(message)
                            sendWhatsappMessage_chain(phoneNumber,message)        
                            # message = f'You have chosen Option: {text}, Please write the work you want to learn today'     
                   
                        if(value == "3" ):

                            print("running 3")
                            word_id=text
                            try:
                                app_id = 'adafa854'
                                app_key = 'a82bf341640fd31d670f17bee543aa91'
                                endpoint = "entries"
                                language_code = "en-us"
                                fields = 'definitions'
                                strictMatch = 'false'
                                url = "https://od-api.oxforddictionaries.com/api/v2/"+ endpoint+"/"+language_code+"/"+word_id  + '?fields=' + fields + '&strictMatch=' + strictMatch;
                                headers = {"app_id": app_id, "app_key": app_key,"word_id":word_id, 'units': 'imperial'}
                                response = requests.get(url, headers=headers)
                                lookup = response.json()
                                word = lookup['results'][0]['id']
                                wordtype = lookup['results'][0]['lexicalEntries'][0]['lexicalCategory']['id']
                                defin = lookup['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
                                final_str = "Word: %s \nType: %s \nDefinition: %s." % (word, wordtype, defin)
                            except:  
                                final_str = 'There was a problem retrieving that information. \n Please try searching for another word.'
                                print(final_str)
                                sendWhatsappMessage_chain(phoneNumber,final_str)       
                            try:

                                url = "http://127.0.0.1:3001/"

                                payload = json.dumps({
                                "word": text
                                })
                                headers = {
                                'Content-Type': 'application/json',
                                'Cookie': 'csrftoken=HnZ0xkkPTtNNKL0xMWEnFEhZ3ZcbXbxRs87wLRTFeUeR1HJ6OYcR5N4RWYSb5HoJ'
                                }

                                res = requests.request("POST", url, headers=headers, data=payload)
                            # Assuming the JSON string is stored in a variable called 'res.text'

                                # Parse the JSON string into a dictionary
                                data = json.loads(res.text)

                                # Extract the 'sentence' key and its value from the dictionary
                                sentences = data['sentence']

                                # Loop through the sentences and print each one

                                sentence_format = "Sentence {}: {}\n"

                                sentence_string = ""
                                for i, sentence in enumerate(sentences):
                                    sentence_string += sentence_format.format(i+1, sentence)

                                print(sentence_string)
                                message = sentence_string
                                sendWhatsappMessage_chain(phoneNumber,message)                            
                            except Exception as e:
                                print("ERROR : "+str(e))    

                            message = final_str
                            print(message)
                            sendWhatsappMessage_chain(phoneNumber,message)                            
                            message = f'Thank you {profileName} for using our service, Send Hi to start again'
                            print(message)
                            # message = f'You have chosen Option: {text}, Please write the work you want to learn today'                    
                        else:
                            print("running else")
                            if(text == "1"):
                                print("running text 1")
                                message =   f'Hi {profileName},Your have chosen 1. Article Search, \n Please provide the word you want article on!! '
                                sendWhatsappMessage_chain(phoneNumber,message)
                            elif(text == "2"):
                                print("running text 2")
                                message =   f'Hi {profileName}, ,Your have chosen 2. English Dictionary Search, \n Please provide the word you want learn today!! \n  '
                                sendWhatsappMessage_chain(phoneNumber,message)
                            elif(text == "3"):
                                print("running text 2")
                                message =   f'Hi {profileName}, ,Your have chosen 3. Oxford English Dictionary Search, \n Please provide the word you want learn today!! \n  '
                                sendWhatsappMessage_chain(phoneNumber,message)
                            else:
                                print("running text else else")
                                message =   f'Hi {profileName}, We are currently offering 2 options \n 1. Article Search 2. English Dictionary Search,3 . Oxford English Dictionary Search, \n Please press the number as per your choice '
                                sendWhatsappMessage_chain(phoneNumber,message)
                            

                        # sendWhastAppMessage (phoneNumber, message)
                        # sendWhatsappMessage(phoneNumber,message)

                except Exception as e:
                    print("ERROR : "+str(e))

        return HttpResponse('success', status = 200)

    WHATSAPP_TOKEN = "Bearer EAAOljqZAaJREBACMAS1TZB0sYGqiByrZBpTKykmkIKjpkzD5qp8MHDihqUPRUJ5TZAdLDhWZAGKPWgKHGdX3QEYisF3S4CD7RHCm3KJqvIldbKc1pBv8FP0ZBJ8fnZCtkRXfsP8i8SPjosZC6Wq00anNGBZA9EraL8rpjT38YZB3Jt1g9FXnz5ZCPcfpsKDCLRlv0g9lIF9YZAyuYwZDZD"
    phoneNumber = "918875091601"
    url = "https://graph.facebook.com/v15.0/107095272246745/messages/"

    payload = json.dumps({
    "messaging_product": "whatsapp",

    "recipent_type": "individual",
    "to": phoneNumber,
    # "type": "template",
    # "template":{"name":"hello_world", "language": { "code": "en_US" } }
    "type": "text",
    "text":{"body":"Sending Automated Message","preview_url":False}
    })
    headers = {
    'Authorization': WHATSAPP_TOKEN,
    'Content-Type': 'application/json'
    }
     

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return render(request, 'counter/index.html')



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
