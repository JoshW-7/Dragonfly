from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.views.generic import DetailView

from taggit.models import Tag

from users.models import UserProfile

from .models import Item
from .forms import ItemForm


class ItemsView(View):
    def get(self, request):
        items = Item.objects.all().order_by("-date_updated")
        
        user_items = None
        if request.user.is_authenticated:
            user_items = items.filter(assigned=request.user.userprofile)

        return render(request, "items/items.html", {
            "items": items,
            "user_items": user_items if user_items else None,
        })

def resolve(request, id):
    item = Item.objects.get(id=id)
    item.resolved = True
    item.save(update_time=False)
    return redirect(request.META.get('HTTP_REFERER'))

def unresolve(request, id):
    item = Item.objects.get(id=id)
    item.resolved = False
    item.save(update_time=False)
    return redirect(request.META.get('HTTP_REFERER'))


class ItemDetailView(View):
    def get(self, request, pk=-1):
        if pk == -1:
            form = ItemForm()
            instance = form.instance
        else:
            instance = Item.objects.get(pk=pk)
            form = ItemForm(instance=instance)

            form.fields["priority"].initial = [instance.priority]
            form.fields["assigned_to"].initial = [instance.assigned]
            tags = [tag for tag in instance.tags.all()]
            for tag in tags:
                tag = str(tag)
                if tag == "feature":
                    form.fields["tag_feature"].widget.attrs["checked"] = True
                if tag == "bug":
                    form.fields["tag_bug"].widget.attrs["checked"] = True
                if tag == "task":
                    form.fields["tag_task"].widget.attrs["checked"] = True
 
        return render(request, "items/item_detail.html" , {
            "form": form,
            "tags": Tag.objects.all(),
            "editing": True if pk != -1 else False,
            "resolved": instance.resolved,
        })

    def post(self, request, pk=-1):
        try:
            user = UserProfile.objects.get(user=request.user)
        except:
            user = UserProfile.objects.get(user__username="default")

        if pk != -1 and "button_delete" in request.POST:
            Item.objects.get(pk=pk).delete()
            return redirect("items")
        elif pk != -1 and "button_resolve" in request.POST:
            instance = Item.objects.get(pk=pk)
            instance.resolved = True
            instance.save()
            return redirect("items")
        elif pk != -1 and "button_unresolve" in request.POST:
            instance = Item.objects.get(pk=pk)
            instance.resolved = False
            instance.save()
            return redirect("items")
        else:
            form = ItemForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                if pk != -1:
                    instance.pk = pk
                instance.user = user
                instance.date_created = timezone.now()
                instance.priority = request.POST.get("priority")
                instance.save()
                current_tags = [tag for tag in instance.tags.all()]
                tags = [field.split("_")[1] for field in request.POST if field.startswith("tag_")]
                for tag in current_tags:
                    if tag not in tags:
                        instance.tags.remove(tag)
                for tag in tags:
                    instance.tags.add(tag)
                
                
                user_name = request.POST.get("assigned_to")
                user_profile = UserProfile.objects.get(user__username=user_name)
                if user_profile:
                    instance.assigned = user_profile
                else:
                    instance.assigned = UserProfile.objects.get(user__username="default")
                instance.save()
                return redirect("items")

        return render(request, "items/item_detail.html" , {
            "form": form,
            "tags": Tag.objects.all(),
        })