from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.views.generic import DetailView
from django.core.files.storage import FileSystemStorage

from taggit.models import Tag
from users.models import UserProfile
from projects.models import Project

from .models import Item, File, Comment
from .forms import ItemForm, CommentForm


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


class ItemDetailView(View):
    def get(self, request, pk=-1):
        comment_form = None
        comments = []
        if pk == -1:
            form = ItemForm()
            instance = form.instance
        else:
            instance = Item.objects.get(pk=pk)
            form = ItemForm(instance=instance)
            comment_form = CommentForm()
            comments = Comment.objects.filter(item=instance).order_by("date_created")

            if instance.project:
                form.fields["project"].initial = [instance.project.pk]
            else:
                form.fields["project"].initial = [""]
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
            "comment_form": comment_form,
            "comments": comments,
            "tags": Tag.objects.all(),
            "editing": True if pk != -1 else False,
            "resolved": instance.resolved,
            "files": [file for file in File.objects.filter(item=instance)],
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
                project = None
                try:
                    project = Project.objects.get(pk=request.POST.get("project"))
                except:
                    pass
                if project:
                    instance.project = project

                instance.save()

                comments = Comment.objects.filter(item=instance).order_by("-date_created")
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
                return redirect("item", pk=instance.pk)

        return render(request, "items/item_detail.html" , {
            "form": form,
            "comments": comments,
            "tags": Tag.objects.all(),
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

def remove(request, id):
    Item.objects.get(id=id).delete()
    return redirect("items")

def remove_file(request, id):
    file_id = request.POST.get("file_id")
    if file_id:
        File.objects.get(pk=file_id).delete()
            
    return redirect(request.META.get('HTTP_REFERER'))

def upload(request, id):
    uploaded_file = request.FILES['file_document']
    fs = FileSystemStorage()
    uploaded_file.name = uploaded_file.name.replace(" ", "")
    name = fs.save(uploaded_file.name, uploaded_file)
    new_file = File()
    new_file.file.name = fs.url(name)
    new_file.item = Item.objects.get(id=id)
    new_file.name = uploaded_file.name
    new_file.save()
    return redirect(request.META.get('HTTP_REFERER'))

def add_relation(request, id):
    item = Item.objects.get(id=id)
    related_item = None
    related_id = None

    try:
        related_id = int(request.POST["related_id"])
    except:
        return redirect(request.META.get('HTTP_REFERER'))

    try:
        related_item = Item.objects.get(id=related_id)
    except:
        return redirect(request.META.get('HTTP_REFERER'))

    if related_item and related_item != item:
        for relation_item in item.get_relations():
            if relation_item == related_item:
                return redirect(request.META.get('HTTP_REFERER'))
        item.add_relation(related_item)
        item.save()
        related_item.add_relation(item)
        related_item.save()
    return redirect(request.META.get('HTTP_REFERER'))
    
def remove_relation(request, id):
    item = Item.objects.get(id=id)
    related_item = None
    related_id = None

    try:
        related_id = int(request.POST["related_id"])
    except:
        return redirect(request.META.get('HTTP_REFERER'))

    try:
        related_item = Item.objects.get(id=related_id)
    except:
        return redirect(request.META.get('HTTP_REFERER'))

    if related_item and related_item != item:
        item.remove_relation(related_item)
        item.save()
        related_item.remove_relation(item)
        related_item.save()
    return redirect(request.META.get('HTTP_REFERER'))

def comment(request, id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = UserProfile.objects.get(user=request.user)
        comment.item = Item.objects.get(id=id)
        comment.save()
    return redirect(request.META.get('HTTP_REFERER'))