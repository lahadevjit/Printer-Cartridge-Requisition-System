# yourapp/context_processors.py

def employee_name(request):
    name = request.session.get("emp_name", None)
    return {
        'employee_name': name
    }
