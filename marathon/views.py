from django.views.generic import TemplateView


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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['products'] = Product.objects.all()[:6]
    #     return context
