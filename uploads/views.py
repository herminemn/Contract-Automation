from django.shortcuts import render, redirect, get_object_or_404
from django.forms.formsets import formset_factory
from django.template import RequestContext
from django.core.exceptions import ValidationError
from .forms import UploadFileForm, VariablesForm
from .models import DocFile, VarFields
from docxtpl import DocxTemplate
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
    regex = re.compile(r"\{(.*?)\}")
    variables = []
    for paragraph in document.paragraphs:
        match = re.findall(regex, paragraph.text)
        variables.append(match)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                match = re.findall(regex, cell.text)
                variables.append(match)
    document.save('test.docx')
    temp_list = []
    for variable in variables:
        for var in variable:
            if len(var) > 0:
                temp_list.append(var)
    variables = temp_list
    print(variables)
    inputs_list = []
    form_field = VariablesForm(variables=variables)
    if request.method == 'POST':
        input_texts = form_field.get_input_text()
        print(input_texts)

    return render(request, 'uploads/file_detail.html', {
        'variables': variables, 'form_field': form_field
    })


def delete_file(request, pk):
    if request.method == 'POST':
        uploaded_file = DocFile.objects.get(pk=pk)
        uploaded_file.delete()
    return redirect('files_list')


