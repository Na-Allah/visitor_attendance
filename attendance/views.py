# attendance/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Organisation, Visitor
from .forms import VisitorForm

def confirm_org(request, org_id):
    org = get_object_or_404(Organisation, id=org_id)
    return render(request, "confirm_org.html", {"org": org})

def enter_details(request, org_id):
    org = get_object_or_404(Organisation, id=org_id)

    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.organisation = org
            visitor.save()
            return redirect("success", visitor_id=visitor.id)
    else:
        form = VisitorForm()

    return render(request, "enter_details.html", {"form": form, "org": org})

def success(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    return render(request, "success.html", {"visitor": visitor})


# Admin: organisation QR generator
def admin_org_list(request):
    orgs = Organisation.objects.all()
    return render(request, "admin_org_list.html", {"orgs": orgs})
