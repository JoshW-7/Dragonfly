from django.shortcuts import render
from django.views import View

from taggit.models import Tag

from users.models import UserProfile

from .models import Item
from .forms import ItemForm


class ItemsView(View):
    def get(self, request):
        items = Item.objects.all()
        
        user_items = None
        if request.user.is_authenticated:
            user_items = items.filter(user=request.user.userprofile)

        return render(request, "items/items.html", {
            "items": items,
            "user_items": user_items if user_items else None,
        })


class NewView(View):
    def get(self, request):
        form = ItemForm()
        return render(request, "items/new.html" , {
            "form": form,
            "tags": Tag.objects.all(),
        })

    def post(self, request):
        user = UserProfile.objects.get(user=request.user)
        form = ItemForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            tags = [field.split("_")[1] for field in request.POST if field.startswith("tag_")]
            for tag in tags:
                instance.tags.add(tag)
            instance.save()

        return render(request, "items/new.html" , {
            "form": form,
            "tags": Tag.objects.all(),
        })