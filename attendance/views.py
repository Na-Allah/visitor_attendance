# attendance/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Organisation, Visitor, Attendance
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

            # Create attendance
            Attendance.objects.create(
                visitor=visitor,
                organisation=org
            )

            return redirect("success", visitor_id=visitor.id)
    else:
        form = VisitorForm()

    return render(request, "enter_details.html", {"form": form, "org": org})



# Admin: organisation QR generator
def attendance_list(request):
    visitors = Visitor.objects.select_related("organisation").order_by("-visited_at")
    return render(request, "attendance_list.html", {"visitors": visitors})



def admin_org_list(request):
    orgs = Organisation.objects.all()
    return render(request, "admin_org_list.html", {"orgs": orgs})


def generate_qr(request, org_id):
    org = get_object_or_404(Organisation, id=org_id)
    org.qr_code.delete(save=False)  # remove old QR
    org.qr_code = None
    org.save()   # triggers auto-regeneration
    return redirect("admin_org_list")

def success(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    return render(request, "success.html", {"visitor": visitor})
