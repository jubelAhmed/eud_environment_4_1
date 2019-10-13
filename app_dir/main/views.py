from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from django.db.models import Q
from app_dir.main import function_writer, block_generator, form_creator
from app_dir.main.generated_functions import *
import ast
import copy

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib import messages
import logging


def register(request):
    if request.session.get('username') is None:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                request.session['username'] = username
                print(username)
                login(request, user)
                return redirect('main:login')
            else:
                for msg in form.error_messages:
                    print(form.error_messages[msg])
                return render(request=request, template_name='register.html', context={"form": form})
        form = UserCreationForm
        return render(request=request, template_name='register.html', context={"form": form})
    else:
        return redirect('main:home_url')


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data= request.POST);
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            logging.info("username", username)
            request.session['username'] = username
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                _id = request.user.id
                request.session['user_id'] = _id
                messages.info(request, f"You are now logged in as {username}")
                return redirect('main:home_url')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Unexpected things happened")

    form = AuthenticationForm
    return render(request= request,template_name='login.html', context={"form": form})


def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:register")


def save_composition(request):
    if request.method == 'POST':
        post_text = request.POST.get('code')
        response_data = {}
        user = request.user
        post = SaveComposition(user=user, username=user.username, code=post_text)
        post.save()
        response_data['result'] = 'Create post successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def home(request):
    all_service = requests.get("http://127.0.0.1:8000/api/service_registry/").json()

    if len(all_service) > 0:
        last_service = all_service[-1]
        read_file = open('registry.txt', 'r')
        a = read_file.read()
        read_file.close()
        name_id = last_service['name']
        sensor_tag = name_id
        name_id = name_id.replace(".", "_")

        if int(a) < last_service['id']:
            write_file = open('registry.txt', 'w+')
            write_file.write(str(last_service['id']))
            write_file.close()
            if last_service['service_type'] == 'sensor':
                function_writer.sensor_function_writer(name_id, sensor_tag)
                block_generator.block_generator(name_id, last_service['service_type'])
                form_creator.sensor_interface_creator(name_id)

            elif last_service['service_type'] == 'actuator':
                function_writer.actuator_function_writer(name_id, sensor_tag)
                block_generator.block_generator(name_id, last_service['service_type'])
                form_creator.actuator_interface_creator(name_id)

            elif last_service['service_type'] == 'api':
                last_api = API.objects.get(name=name_id)
                api_name = last_api.name
                api_link = last_api.api
                api_fields = last_api.fields
                api_connection = last_api.connection
                api_name = api_name.replace(".", "_")
                function_writer.api_function_writer(api_name, api_link, api_fields)
                block_generator.api_block_generator(api_name, 'api', api_fields, api_connection)
                form_creator.api_form_creator(api_name, api_fields)
                form_creator.url_creator(api_name)
                form_creator.post_function_creator(api_name, api_link, api_fields)

            elif last_service['service_type'] == 'interactive':
                last_interactive = Interactive.objects.get(name=name_id)
                interactive_name = last_interactive.name
                interactive_fields = last_interactive.fields
                interactive_name = interactive_name.replace(".", "_")
                function_writer.interactive_function_writer(interactive_name, interactive_fields)
                block_generator.interactive_block_generator(interactive_name, 'interactive', interactive_fields)

    # MailBox Creator
    mailboxes = MailBox.objects.all()
    mailbox_len = mailboxes.count()
    if mailbox_len > 0:
        last_mailbox = mailboxes[mailbox_len - 1]
        read_mailbox = open('mailbox.txt', 'r')
        mailbox_a = read_mailbox.read()
        read_mailbox.close()
        mailbox_name = last_mailbox.name
        mailbox_tag = last_mailbox.api
        mailbox_name = mailbox_name.replace(".", "_")
        if int(mailbox_a) < last_mailbox.id:
            write_file = open('mailbox.txt', 'w+')
            write_file.write(str(last_mailbox.id))
            write_file.close()
            function_writer.mailbox_function_writer(mailbox_name, mailbox_tag.name)
            block_generator.block_generator(mailbox_name, 'mailbox')

    return render(request, 'index.html')


class ActuatorAPI(viewsets.ModelViewSet):
    queryset = Actuator.objects.all()
    serializer_class = ActuatorSerializer


class SensorAPI(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class ServiceRegistryAPI(viewsets.ModelViewSet):
    queryset = ServiceRegistry.objects.all()
    serializer_class = ServiceRegistrySerializer


class MailBoxAPI(viewsets.ModelViewSet):
    queryset = MailBox.objects.all()
    serializer_class = MailBoxSerializer


class APInterfaceAPI(viewsets.ModelViewSet):
    queryset = API.objects.all()
    serializer_class = APISerializer


class InteractiveAPI(viewsets.ModelViewSet):
    queryset = Interactive.objects.all()
    serializer_class = InteractiveSerializer


class SaveCompositionAPI(viewsets.ModelViewSet):
    queryset = Interactive.objects.all()
    serializer_class = SaveCompositionSerializer


class ActuatorListApiView(generics.ListAPIView):
    serializer_class = ActuatorSerializer

    def get_queryset(self):
        qs = Actuator.objects.all()
        query = self.request.GET.get("q")

        if query is not None:
            qs = qs.filter(
                Q(topic__icontains=query)
            ).distinct().order_by('-time')[:1]

        return qs


def convert_expr_expression(expr):
    expr.lineno = 0
    expr.col_offset = 0
    result = ast.Expression(expr.value, lineno=0, col_offset=0)

    return result


def exec_with_return(code):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        return eval(compile(convert_expr_expression(last_ast.body[0]), "<ast>", "eval"), globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"), globals())


def eud_code(request):
    if request.is_ajax():
        code = request.POST['code']
        result = exec_with_return(code)
    else:
        return HttpResponse('Use ajax format!')

    return JsonResponse({'code': result})
