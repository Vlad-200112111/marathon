from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.list import ListView
from faker import Faker
import random

from .models import *

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


class LoginView(BaseView):
    template_name = "login.html"


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
            print(f"User {user.first_name} {user.last_name} created!")

    def create_other_models(self):
        users = User.objects.all()

        category_runners = CategoryRunner.objects.all()
        charitable_organizations = CharitableOrganization.objects.all()
        marathons = Marathon.objects.all()
        kit_options = KitOption.objects.all()

        for _ in range(20):
            runner = Runner(user=random.choice(users), category_runner=random.choice(category_runners)).save()
            sponsor = Sponsor(card=fake.credit_card_full(), number_card=fake.credit_card_number(),
                              cvc=fake.credit_card_security_code(), validity_period=fake.future_date()).save()

        runners = Runner.objects.all()
        sponsors = Sponsor.objects.all()
        for runner in runners:
            runner_and_sponsor = RunnerAndSponsor(runner=runner, sponsor=random.choice(sponsors),
                                                  contribution=random.uniform(50, 200)).save()
            marathon_result = MarathonResult(runner=runner, marathon=random.choice(marathons),
                                             charitable_organization=random.choice(charitable_organizations),
                                             kit_option=random.choice(kit_options), common_place=random.uniform(1, 10),
                                             place_by_category=random.uniform(1, 10),
                                             is_confirmed_payment=random.choice((True, False)),
                                             distance_passing_time=random.randint(5, 60),
                                             is_completed=random.choice((True, False))).save()

            print(f"All objects in iteration {_} created!")
