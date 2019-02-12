from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UploadFileForm, VariablesForm
from .functions import docx_words_replace
from .models import DocFile
from docx import Document
import re
import os


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


def delete_file(request, pk):
    if request.method == 'POST':
        uploaded_file = DocFile.objects.get(pk=pk)
        uploaded_file.delete()
    return redirect('files_list')


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
    temp_list = []
    for variable in variables:
        for var in variable:
            if len(var) > 0:
                temp_list.append(var)
    variables = temp_list
    variables_set = sorted(set(temp_list), key=temp_list.index)
    inputs_list = []
    form_field = VariablesForm(request.POST, variables=variables_set)
    if request.method == 'POST' and form_field.is_valid():
        input_texts = form_field.get_input_text()
        for i, input_text in input_texts:
            inputs_list.append(input_text)
    my_dict = dict(zip(variables_set, inputs_list))
    for word, replacement in my_dict.items():
        word_re = re.compile(word)
        docx_words_replace(document, word_re, replacement)
    regex1 = re.compile(r"{")
    regex2 = re.compile(r"}")
    replace = r""
    docx_words_replace(document, regex1, replace)
    docx_words_replace(document, regex2, replace)
    if len(inputs_list) != 0:
        contract_name = inputs_list[0]
        file_name = '{}.docx'.format(contract_name)
        desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
        document.save(os.path.join(desktop, file_name))
        messages.success(request, 'Saved on Desktop')
    return render(request, 'uploads/file_detail.html', {
        'variables': variables, 'form_field': form_field
    })
