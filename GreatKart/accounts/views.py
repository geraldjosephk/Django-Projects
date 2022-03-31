from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    """
    Function to register new users after verification.
    Validates user data submitted in registration form, creates user in database and saves.
    Sends an encoded activation token to user email.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # store data according to field type
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            # split email address to show first letters before the @ and assign as username
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.save()

            # User authentication
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect("/accounts/login/?command=verification&email=" + email)
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


def login(request):
    """
    Function to login user and redirect them to the home page.
       Accepts email and password post requests. Matches email and
       passwords to users in database. If user exists in database,
       login and redirect to home page. Otherwise, user prompted to login again
    """
    if request.method == "POST":
        email = request.POST.get("email")  # get email imput posted
        password = request.POST.get("password")

        user = auth.authenticate(
            email=email, password=password
        )  # check if email and password is active
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("dashboard")  # redirect to home page
        else:
            messages.error(request, "Invalid Login credentials")
            return redirect("login")
    return render(request, "accounts/login.html")


# to logout, user must be already login
@login_required(login_url="login")
def logout(request):
    """
    Function to logout user and redirect them to login page.
    The user must be already logged in
    """
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")


def activate(request, uidb64, token):
    """
    Function flags user account to active.
    Accepts user request,uidb64 and user token as arguments.
    Decodes the user token and matches uid with primary key.
    If user does not activate the token, the user account is not activated.
    Otherwise, user account is activated as 'is_active' in Django Admin.
    The user is redirected to the login page.
    If user takes long to use the token, or uses a non-authentic link,
    the user is redirected to the register page.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect("login")

    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "accounts/dashboard.html")
