from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.symptom.models import EncryptedFile, Customer
from apps.symptom.utils import encrypt_file, decrypt_file
from apps.symptom.form import FileUploadForm
from django.http import HttpResponse

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_type = form.cleaned_data['file_type']
            belongs_to = form.cleaned_data['belongs_to']
            process_start_date = form.cleaned_data['process_start_date']

            # Leer y encriptar el archivo
            encrypted_data = encrypt_file(file.read())

            # Guardar el archivo encriptado
            encrypted_file = EncryptedFile(
                file=file,
                file_type=file_type,
                uploaded_by=request.user,
                belongs_to=belongs_to,
                encrypted_file=encrypted_data,
                process_start_date=process_start_date
            )
            encrypted_file.save()
            return redirect('list_files')
    else:
        form = FileUploadForm()
    return render(request, 'pages/customers/actions/components/customerFileList.html', {'form': form})

@login_required
def list_files(request):
    files = EncryptedFile.objects.filter(belongs_to=request.user)
    return render(request, 'pages/cryptography/list_files.html', {'files': files})

@login_required
def download_file(request, file_id):
    encrypted_file = EncryptedFile.objects.get(id=file_id)
    decrypted_data = decrypt_file(encrypted_file.encrypted_file)

    response = HttpResponse(decrypted_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{encrypted_file.file.name}"'
    return response