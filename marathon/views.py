from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.list import ListView
from faker import Faker
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

import random

from .models import *
from .forms import *

fake = Faker('ru_RU')


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        self.request.session[0] = "barr"
        sessionid = self.request.COOKIES.get("sessionid")

        context = super().get_context_data(**kwargs)

        return context


class IndexView(BaseView):
    template_name = "index.html"


class RegisterAsRunnerView(BaseView):
    template_name = "register_as_runner.html"


class AdminView(BaseView):
    template_name = "admin.html"


class RunnerView(BaseView):
    template_name = "runner.html"


class CoordinatorView(BaseView):
    template_name = "coordinator.html"


class MySponsorView(BaseView):
    template_name = "my_sponsor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = User.objects.get(pk=self.request.user.pk)
        print(user.uuid)
        print(user.runner_set.all())
        runner = Runner.objects.get(user_id=user.uuid)
        print(runner)
        charitable_organization = CharitableOrganization.objects.get(id=runner.charitable_organization_id)
        # context['news'] = New.objects.all().order_by("-date")[:3]
        return context


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='ADMIN').exists():
                    return redirect("menu_admin")
                elif user.groups.filter(name='Runner').exists():
                    return redirect("menu_runner")
                elif user.groups.filter(name='Coordinator').exists():
                    return redirect("menu_coordinator")
            else:
                messages.error(request, 'Неверный логин или пароль!',
                               extra_tags='alert alert-danger alert-dismissible fade show'
                               )

    return render(request, "login.html", {"form": form})


# class LoginView(BaseView):
#     template_name = "login.html"


class RegisterView(BaseView):
    template_name = "register.html"


class SponsorView(BaseView):
    template_name = "sponsor.html"


class AboutView(BaseView):
    template_name = "about.html"


class BMIView(BaseView):
    template_name = "bmi.html"


class BMRView(BaseView):
    template_name = "bmr.html"


class CharitableOrganizationView(ListView):
    model = CharitableOrganization
    template_name = "charitable_organization.html"
    context_object_name = 'charitable_organizations'


class GenerateFakeDataApiView(APIView):

    def get(self, request):
        self.create_user()
        self.create_other_models()
        return Response({"result": "success"})

    def create_user(self):
        for i in range(20):
            first_name = fake.first_name_male() if fake.random_element(
                elements=(True, False)) else fake.first_name_female()
            last_name = fake.last_name_male() if first_name[-1] == 'й' else fake.last_name_female()
            middle_name = fake.middle_name_male() if first_name[-1] == 'й' else fake.middle_name_female()
            runner_role = Group.objects.get(name="Runner")
            user = User(
                username=f"runner_{i}@m.ru",
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                email=f"runner_{i}@m.ru",
                gender='male' if random.choice((True, False)) else 'female',
                date_of_birth=fake.date(),
                cityzenship="РФ",
                is_superuser=False,
                is_staff=False,
            )
            user.set_password(f"runner_{i}")
            user.save()
            user.groups.add(runner_role)
            print(f"User {user.first_name} {user.last_name} created!")

    def create_other_models(self):
        users = User.objects.all()

        category_runners = CategoryRunner.objects.all()
        marathons = Marathon.objects.all()
        kit_options = KitOption.objects.all()
        charitable_organizations = CharitableOrganization.objects.all()

        for _ in range(20):
            runner = Runner(user=random.choice(users), category_runner=random.choice(category_runners),
                            charitable_organization=random.choice(charitable_organizations)).save()
            sponsor = Sponsor(card=fake.credit_card_full(), number_card=fake.credit_card_number(),
                              cvc=fake.credit_card_security_code(), validity_period=fake.future_date()).save()

        runners = Runner.objects.all()
        sponsors = Sponsor.objects.all()
        for runner in runners:
            runner_and_sponsor = RunnerAndSponsor(runner=runner, sponsor=random.choice(sponsors),
                                                  contribution=random.uniform(50, 200)).save()
            marathon_result = MarathonResult(runner=runner, marathon=random.choice(marathons),
                                             kit_option=random.choice(kit_options), common_place=random.uniform(1, 10),
                                             place_by_category=random.uniform(1, 10),
                                             is_confirmed_payment=random.choice((True, False)),
                                             distance_passing_time=random.randint(5, 60),
                                             is_completed=random.choice((True, False))).save()

            print(f"All objects in iteration {_} created!")
