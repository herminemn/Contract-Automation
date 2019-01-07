from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm, EditFileForm
from .models import DocFile
from docx import Document
import re


def files_list(request):
    uploaded_files = DocFile.objects.all()
    return render(request, 'uploads/files_list.html', {
        'uploaded_files': uploaded_files
    })


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('files_list')
    else:
        form = UploadFileForm()
    return render(request, 'uploads/upload.html', {
        'form': form
    })


def edit_file(request, upload_id):
    instance = get_object_or_404(DocFile, id=upload_id)
    document = Document(instance.agreement)
    variables = []
    for paragraph in document.paragraphs:
        match = re.findall(r"\{(.*?)\}", paragraph.text)
        variables.append(match)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                match = re.findall(r"\{(.*?)\}", cell.text)
                variables.append(match)
    if request.method == 'POST':
        input_text = EditFileForm(data=request.POST)
        if input_text.is_valid():
            print(input_text.cleaned_data['text'])
    else:
        input_text = EditFileForm()
    document.save('blue.pdf')
    return render(request, 'uploads/file_detail.html', {
        'variables': variables, 'input_text': input_text
    })



def delete_file(request, pk):
    if request.method == 'POST':
        uploaded_file = DocFile.objects.get(pk=pk)
        uploaded_file.delete()
    return redirect('files_list')


