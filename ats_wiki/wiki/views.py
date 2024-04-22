from django.shortcuts import render,redirect, get_object_or_404
from .models import Wiki,FileUpload,CustomUser
from .forms import SearchForm,FileUploadForm,WikiEntryForms
from django.views.generic import ListView
from django.db.models import Count
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.utils.html import strip_spaces_between_tags, strip_tags


def error_404(request, exception):
    return render(request, '404.html')

def error_500(request, *args, **argv):
    return render(request, '500.html')
        
def error_403(request, exception):
    return render(request, '403.html')

def error_400(request,  exception):
    return render(request, '400.html')


def retrieve_information(request):
    entries = Wiki.objects.filter(Approval_Status='approved')
    context = {'entries': entries}
    return render(request, 'ats_wiki/retrieve_information.html', {'entries': entries})



def base_view1(request):
    categories = Wiki.objects.all()
    entries = Wiki.objects.all()
    return render(request, 'ats_wiki/base.html', {'entries': entries, 'categories': categories})

def base_view(request):
    approved_entries = Wiki.objects.filter(Approval_Status='approved')
    context = {'entries': approved_entries}
    return render(request, 'ats_wiki/base.html', context)

def category_filter(request, category):
    entries = Wiki.objects.filter(category=category)
    return render(request, 'ats_wiki/category_filter.html', {'entries': entries, 'category': category})

def search_wiki_entries(request):
    return render(request, 'ats_wiki/search_wiki_entries.html')

def live_search_results(request):
    query = request.GET.get('q')
    if query:
        entries = Wiki.objects.filter(Approval_Status='approved').filter(
            Q(subject__icontains=query) | Q(description__icontains=query)
        )
    else:
        entries = Wiki.objects.none()
    return render(request, 'ats_wiki/live_search_results.html', {'entries': entries})




def item_detail1(request, item_id):
    wiki_entry = get_object_or_404(Wiki, pk=item_id)
    file_uploads = FileUpload.objects.filter(wiki_entry=wiki_entry)
    context = {
        'item': wiki_entry,
        'file_uploads': file_uploads
    }
    return render(request, 'ats_wiki/item_detail copy.html', context)



from .models import FileUpload

def add_information1(request):


    # Fetch all users to populate the 'created_by' field
    users = CustomUser.objects.all()

    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        created_by_id = request.POST.get('created_by')
        approval_status = request.POST.get('approval_status')
        
        # Handle multiple file uploads
        file_uploads = request.FILES.getlist('file_upload')

        try:
            # Create a single Wiki instance
            wiki_entry = Wiki.objects.create(
                subject=subject, 
                description=description, 
                Approval_Status=approval_status,
                Created_by_id=created_by_id
            )
            
            # Link each file upload to the single Wiki instance
            for file_upload in file_uploads:
                file_instance = FileUpload.objects.create(
                    wiki_entry=wiki_entry,
                    file=file_upload
                )

            # Get the email of the user who created the entry
            created_by_email = CustomUser.objects.get(id=created_by_id).email
            item_detail_url = request.build_absolute_uri(reverse('approval', args=[wiki_entry.id]))
            description_new = strip_tags(wiki_entry.description)
            # Sending email
            email_subject = 'New Article for Approval'
            email_message = f'Prakash,\n\nAn article has been submitted for approval.\n\nSubject: {subject}\n\nDescription: {description_new}\n\nApproval Link: {item_detail_url}\n\nRegards,\n{CustomUser.objects.get(id=created_by_id).first_name} {CustomUser.objects.get(id=created_by_id).last_name},\n{CustomUser.objects.get(id=created_by_id).email}'
            #from_email = created_by_email  # Use created_by email as the sender email
            to_email = ['perukulla@atsindia.net','psoopekaar@atsindia.net']
            send_mail(email_subject, email_message, created_by_email, to_email, fail_silently=False)

            messages.success(request, 'Information added successfully.')
        except Exception as e:
            messages.error(request, f'Failed to add information: {str(e)}')
        
        return redirect('add_information1')  # Redirect back to the same page
    
    return render(request, 'ats_wiki/add_information1.html', { 'users': users})


def update_information1(request, pk):
    entry = get_object_or_404(Wiki, pk=pk)
    
    if request.method == 'POST':
        form = WikiEntryForms(request.POST, instance=entry)
        file_form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid() and file_form.is_valid():
            form.save()
            file_instance = file_form.save(commit=False)
            file_instance.wiki_entry = entry
            file_instance.save()

            # Handle file clearing
            files_to_clear = request.POST.getlist('file_clear')
            for file_id in files_to_clear:
                FileUpload.objects.filter(id=file_id).delete()

            # Get the email of the user who updated the entry
            Created = entry.Created_by
            updated_by_email = Created.email
            item_detail_url = request.build_absolute_uri(reverse('approval', args=[entry.id]))
            description_new = strip_tags(entry.description)

            # Sending email
            email_subject = 'Article Updated'
            email_message = f'Prakash,\n\nAn article has been updated.\n\nSubject: {entry.subject}\n\nDescription: {description_new}\n\nApproval Link: {item_detail_url}\n\nRegards,\n{Created.first_name} {Created.last_name},\n{updated_by_email}'
            to_email = ['perukulla@atsindia.net','psoopekaar@atsindia.net']
            send_mail(email_subject, email_message, updated_by_email, to_email, fail_silently=False)

            messages.success(request, 'Information updated successfully.')
            return redirect('base_view')
    else:
        form = WikiEntryForms(instance=entry)
        file_form = FileUploadForm()

    # Get all files uploaded for this entry
    uploaded_files = FileUpload.objects.filter(wiki_entry=entry)

    return render(request, 'ats_wiki/update_information copy.html', {'form': form, 'file_form': file_form, 'uploaded_files': uploaded_files})

def approval(request, item_id):
    wiki_entry = get_object_or_404(Wiki, pk=item_id)
    file_uploads = FileUpload.objects.filter(wiki_entry=wiki_entry)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        approval_status = request.POST.get('approval_status')
        comments = request.POST.get('comments')

        wiki_entry.subject = subject
        wiki_entry.description = description
        wiki_entry.Approval_Status = approval_status
        wiki_entry.Comments = comments
        wiki_entry.save()

        if approval_status == 'approved':
            created_by = wiki_entry.Created_by
            subject = wiki_entry.subject
            description = strip_tags(wiki_entry.description)
            item_detail_url = request.build_absolute_uri(reverse('item_detail1', args=[wiki_entry.id]))
            to_email = created_by.email
            email_subject = 'New Article Approved'
            email_message = f"Hello {created_by.first_name} {created_by.last_name},\n\nThe below article has been approved and uploaded.\n\nSubject: {subject}\n\nDescription: {description}\n\nComments: {comments}\n\nRegards,\nPrakkash"
            send_mail(email_subject, email_message, None, [to_email], fail_silently=False)
        else:
            created_by = wiki_entry.Created_by
            subject = wiki_entry.subject
            item_detail_url = request.build_absolute_uri(reverse('update_information1', args=[wiki_entry.id]))
            to_email = created_by.email
            email_subject = 'Article Update Required'
            email_message = f"Hello {created_by.first_name} {created_by.last_name},\n\nThe below article needs further updates as per comments below.\n\nSubject: {subject}\n\nComments: {comments}\n\nUpdate Link: {item_detail_url}\n\nRegards,\nPrakkash"
            send_mail(email_subject, email_message, None, [to_email], fail_silently=False)

        messages.success(request, 'Approval status and comments updated successfully.')
        return redirect('base_view')

    existing_comments = wiki_entry.Comments

    context = {
        'item': wiki_entry,
        'file_uploads': file_uploads,
        'existing_comments': existing_comments,
    }

    return render(request, 'ats_wiki/approval.html', context)

def permanent_delete_file(request):
    if request.method == 'GET':
        file_id = request.GET.get('file_id')
        file_instance = get_object_or_404(FileUpload, id=file_id)
        file_instance.delete()
        return redirect('update_information1', pk=file_instance.wiki_entry.id)
    else:
        # Handle POST requests if needed
        pass