from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone

from .forms import ProjectForm
from .models import Project
from users.models import UserProfile


class ProjectsView(View):
    def get(self, request):
        return render(request, "projects/projects.html", {})
        """
        items = Item.objects.all().order_by("-date_updated")
        
        user_items = None
        if request.user.is_authenticated:
            user_items = items.filter(assigned=request.user.userprofile)

        return render(request, "items/items.html", {
            "items": items,
            "user_items": user_items if user_items else None,
        })
        """


class ProjectDetailView(View):
    def get(self, request, pk=-1):
        if pk == -1:
            form = ProjectForm()
            instance = form.instance
        else:
            instance = Project.objects.get(pk=pk)
            form = ProjectForm(instance=instance)

        return render(request, "projects/project_detail.html" , {
            "form": form,
            "editing": True if pk != -1 else False,
        })

    def post(self, request, pk=-1):
        try:
            user = UserProfile.objects.get(user=request.user)
        except:
            user = UserProfile.objects.get(user__username="default")

        if pk != -1 and "button_delete" in request.POST:
            Project.objects.get(pk=pk).delete()
            return redirect("items")
        else:
            form = ProjectForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                if pk != -1:
                    instance.pk = pk
                instance.user = user
                instance.date_created = timezone.now()
                instance.save()
                return redirect("projects")

        return render(request, "projects/project_detail.html" , {
            "form": form,
        })