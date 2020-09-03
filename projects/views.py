from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone


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


class NewProjectView(View):
    def get(self, request):

        """
        form = ItemForm()
        return render(request, "items/new.html" , {
            "form": form,
            "tags": Tag.objects.all(),
        })
        """

    def post(self, request):
        """
        try:
            user = UserProfile.objects.get(user=request.user)
        except:
            user = UserProfile.objects.get(user__username="default")
        form = ItemForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.date_created = timezone.now()
            instance.save()
            tags = [field.split("_")[1] for field in request.POST if field.startswith("tag_")]
            for tag in tags:
                instance.tags.add(tag)
            user_name = request.POST.get("assigned_to")
            user_profile = UserProfile.objects.get(user__username=user_name)
            instance.assigned = user_profile
            instance.save()
            return redirect("items")

        return render(request, "items/new.html" , {
            "form": form,
            "tags": Tag.objects.all(),
        })
        """
        pass