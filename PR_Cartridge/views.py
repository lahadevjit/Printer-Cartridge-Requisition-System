from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee
from .forms import CartridgeRequestForm
from .models import CartridgeRequest
from django.utils import timezone
from django.http import JsonResponse
from .models import MISAsset

def user_login(request):
    return render(request, "login_page.html")


def session_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("emp_id"):
            messages.error(request, "")
            return redirect("user_login")
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            employee = Employee.objects.get(emp_id=username)
            if username.lower() == "pdrfadmin":
                if employee.password == password:
                    role = "admin"
                else:
                    messages.error(request, "Invalid password.")
                    return render(request, "login_page.html")
            else:
                is_hod = MISAsset.objects.filter(
                    emp_no=employee.emp_id,
                    usage_status="Common Employee"
                ).exists()
                if is_hod:
                    role = "HOD"
                else:
                    role = "Employee"
                if employee.password != password:
                    messages.error(request, "Invalid password.")
                    return render(request, "login_page.html")
            request.session["emp_id"] = employee.emp_id
            request.session["emp_name"] = employee.emp_name
            request.session["department"] = employee.department
            request.session["designation"] = employee.designation
            request.session["role"] = role.lower()
            messages.success(request, f"Welcome, {employee.emp_name}! You are logged in as {role}.")
            if role == "admin":
                return redirect("issue_requests")
            else:
                return redirect("cartridge_request_create")
        except Employee.DoesNotExist:
            messages.error(request, "Employee ID does not exist.")
    return render(request, "login_page.html")
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("user_login")

@session_login_required
def cartridge_request_create(request):
    if request.session.get("role") == "admin":
        messages.error(request, "Unauthorized access.")
        return redirect("issue_requests")

    emp_id = request.session.get("emp_id")
    if not emp_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect("user_login")

    try:
        employee = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found.")
        return redirect("user_login")

    if request.method == "POST":
        form = CartridgeRequestForm(request.POST,employee=employee)
        if form.is_valid():
            request_obj = form.save()
            if request_obj.hod_name:
                try:
                    hod_employee = Employee.objects.get(emp_name=request_obj.hod_name)
                    hod_email = hod_employee.emp_email
                except Employee.DoesNotExist:
                    hod_email = None

                if hod_email:
                    from django.core.mail import send_mail
                    from django.conf import settings

                    send_mail(
                        subject='New Cartridge Request Pending Your Approval',
                        message=f"""
        Dear {request_obj.hod_name},

        A new cartridge request has been submitted by {request_obj.employee_name} ({request_obj.employee_no}).

        Printer No: {request_obj.printer_no}
        Department: {request_obj.department}
        Designation: {request_obj.designation}
        Contact: {request_obj.contact_no}

        Please log in to the Cartridge Portal to review and approve this request.

        Thanks,
        Cartridge Requisition System
        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[hod_email],
                        fail_silently=False,
                    )
            return redirect("cartridge_request_list")
    else:
        form = CartridgeRequestForm(initial={
            "employee_no": employee.emp_id,
            "employee_name": employee.emp_name,
            "department": employee.department,
            "designation": employee.designation,
        },employee=employee)

        # Optional: disable employee fields
        form.fields["employee_no"].widget.attrs["readonly"] = True
        form.fields["employee_name"].widget.attrs["readonly"] = True
        form.fields["department"].widget.attrs["readonly"] = True
        form.fields["designation"].widget.attrs["readonly"] = True

    return render(request, "Home.html", {
        "employee_name": employee.emp_name,
        "emp_id": employee.emp_id,
        "department": employee.department,
        "designation": employee.designation,
        "form": form,
    })
@session_login_required
def cartridge_request_list(request):
    role = request.session.get("role")
    emp_id = request.session.get("emp_id")
    emp_name = request.session.get("emp_name")
    if role == "hod":
        requests = CartridgeRequest.objects.filter(
            Q(employee_no=emp_id)
        ).order_by("-sl_no")
    else:
        requests = CartridgeRequest.objects.filter(employee_no=emp_id).order_by("-sl_no")
    return render(request, "cartridge_request_list.html", {"requests": requests})
from django.shortcuts import get_object_or_404
@session_login_required
def cancel_request(request, sl_no):
    if request.method == "POST":
        req = get_object_or_404(CartridgeRequest, sl_no=sl_no)
        if req.status == "HOD Approved":
            messages.error(request, "This request is already approved and cannot be canceled.")
            return redirect("cartridge_request_list")
        req.delete()
        messages.success(request, "Request canceled successfully.")
        return redirect("cartridge_request_list")
    else:
        return redirect("cartridge_request_list")


@session_login_required
def approve_requests(request):
    if request.session.get("role") != "hod":
        messages.error(request, "Unauthorized access.")
        return redirect("cartridge_request_create")

    emp_name = request.session.get("emp_name")

    pending_requests = CartridgeRequest.objects.filter(
        status="Pending",
        hod_name__iexact=emp_name.strip()
    ).exclude(usage_status="Self").order_by("-sl_no")

    approved_requests = CartridgeRequest.objects.filter(
        status="HOD Approved",
        hod_name__iexact=emp_name.strip()
    ).exclude(usage_status="Self").order_by("-sl_no")

    return render(
        request,
        'approve_requests.html',
        {
            'pending_requests': pending_requests,
            'approved_requests': approved_requests
        }
    )


# def approve_requests(request):
#     if request.session.get("role") != "hod":
#         messages.error(request, "Unauthorized access.")
#         return redirect("cartridge_request_create")
#     role = request.session.get("role")
#     emp_id = request.session.get("emp_id")
#     emp_name = request.session.get("emp_name")
#
#
#     pending_requests = CartridgeRequest.objects.filter(
#         status="Pending",hod_name__iexact=emp_name.strip()
#     ).exclude(usage_status="Self").order_by("-sl_no")
#     return render(request, 'approve_requests.html', {'requests': pending_requests})

@session_login_required
def approve_single_request(request, pk):
    cartridge_request = get_object_or_404(CartridgeRequest, pk=pk)
    cartridge_request.status = "HOD Approved"
    cartridge_request.approved_date=timezone.now()
    cartridge_request.save()
    return redirect('approve_requests')

from django.db.models import Q

@session_login_required
def issue_requests(request):
    if request.session.get("role") != "admin":
        messages.error(request, "Unauthorized access.")
        return redirect("cartridge_request_create")
    pending_requests = CartridgeRequest.objects.filter(
        (
                Q(status="HOD Approved") |
                Q(usage_status="Self")
        ) &
        ~Q(status="IS issued the request")
    ).order_by("-sl_no")
    return render(request, 'issue_request.html', {'requests': pending_requests})

@session_login_required
def issue_single_request(request, pk):
    if request.session.get("role") != "admin":
        messages.error(request, "Unauthorized access.")
        return redirect("cartridge_request_create")

    cartridge_request = get_object_or_404(CartridgeRequest, pk=pk)
    cartridge_request.status = "IS issued the request"
    cartridge_request.issue_date = timezone.now()
    cartridge_request.save()
    return redirect('issue_requests')


@session_login_required
def get_hod_name_by_printer(request):
    printer_no = request.GET.get("printer_no", "").strip()

    if not printer_no:
        return JsonResponse({"hod_name": ""})

    try:
        asset = MISAsset.objects.get(printer_no=printer_no)
        if asset.usage_status == "Common Employee":
            return JsonResponse({
                "hod_name": asset.emp_name
            })
        else:
            return JsonResponse({"hod_name": ""})
    except MISAsset.DoesNotExist:
        return JsonResponse({"hod_name": ""})

from django.http import JsonResponse
from .models import MISAsset

def get_printer_details(request):
    printer_no = request.GET.get("printer_no", "").strip()
    result = {
        "usage_status": "",
        "hod_name": ""
    }
    if printer_no:
        try:
            asset = MISAsset.objects.get(printer_no=printer_no)
            result["usage_status"] = asset.usage_status
            if asset.usage_status == "Common Employee":
                result["hod_name"] = asset.emp_name
        except MISAsset.DoesNotExist:
            # Leave blank fields if not found
            result = {
                "usage_status": "",
                "hod_name": ""
            }
    return JsonResponse(result)


# @session_login_required
# def report_all_list(request):
#     if request.session.get("role") != "admin":
#         messages.error(request, "Unauthorized access.")
#         return redirect("cartridge_request_create")
#     requests = CartridgeRequest.objects.all().order_by("-sl_no")
#     return render(request, "report.html", {"requests": requests})


@session_login_required
def report_all_list(request):
    if request.session.get("role") != "admin":
        messages.error(request, "Unauthorized access.")
        return redirect("cartridge_request_create")
    printer_no = request.GET.get("printer_no", "")
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")
    filters = Q()
    if printer_no:
        filters &= Q(printer_no__icontains=printer_no)
    if from_date:
        filters &= Q(request_date__gte=from_date)

    if to_date:
        filters &= Q(request_date__lte=to_date)
    requests = CartridgeRequest.objects.filter(filters).order_by("-sl_no")
    context = {
        "requests": requests,
        "printer_no": printer_no,
        "from_date": from_date,
        "to_date": to_date,
    }
    return render(request, "report.html", context)



@session_login_required
def validate_printer_no(request):
    printer_no = request.GET.get("printer_no", "").strip()
    emp_id = request.session.get("emp_id")

    if not printer_no:
        return JsonResponse({
            "valid": False,
            "message": "Printer number cannot be empty."
        })

    try:
        asset = MISAsset.objects.get(printer_no=printer_no)
    except MISAsset.DoesNotExist:
        return JsonResponse({
            "valid": False,
            "message": "Invalid printer number."
        })

    if asset.usage_status == "Self":
        if asset.emp_no != emp_id:
            return JsonResponse({
                "valid": False,
                "message": f"This printer does not belongs to you ."
            })

    return JsonResponse({
        "valid": True,
        "message": "Printer is valid."
    })

from django.contrib.auth.decorators import login_required
# @login_required
# def home_view(request):
#     emp_id = request.session.get("emp_id", None)
#
#     if not emp_id:
#         messages.error(request, "Session expired. Please log in again.")
#         return redirect("user_login")
#
#     try:
#         employee = Employee.objects.get(emp_id=emp_id)
#     except Employee.DoesNotExist:
#         messages.error(request, "Employee not found.")
#         return redirect("user_login")
#
#     if request.method == "POST":
#         form = CartridgeRequestForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Request submitted successfully!")
#             return redirect("cartridge_request_list")
#     else:
#         form = CartridgeRequestForm(initial={
#             "employee_no": employee.emp_id,
#             "employee_name": employee.emp_name,
#             "department": employee.department,
#             "designation": employee.designation,
#         })
#
#         # Optional: make fields read-only
#         form.fields["employee_no"].disabled = True
#         form.fields["employee_name"].disabled = True
#         form.fields["department"].disabled = True
#         form.fields["designation"].disabled = True
#
#     return render(request, "Home.html", {
#         "employee_name": employee.emp_name,
#         "form": form,
#     })

