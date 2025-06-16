import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CSVUploadForm
from .models import User
from .serializers import UserSerializer

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Only CSV files are allowed.')
                return render(request, 'users/csv_upload.html', {'form': form})

            decoded_file = csv_file.read().decode('utf-8').splitlines()

            reader = csv.DictReader(decoded_file)

            valid_records = []
            rejected_records = []
            total_data = 0

            for row in reader:
                total_data += 1
                serializer = UserSerializer(data=row)
                
                if serializer.is_valid():
                    valid_records.append(User(**serializer.validated_data))
                else:
                    error_msg = format_errors(serializer.errors)
                    rejected_records.append({'row': row, 'reason': error_msg})

            User.objects.bulk_create(valid_records, ignore_conflicts=True)

            summary = {
                'total_data': total_data,
                'total_success': len(valid_records),
                'total_rejected': len(rejected_records),
                'rejected_records': rejected_records,
            }

            messages.success(request, 'CSV file uploaded successfully.')
            return render(request, 'users/csv_upload.html', {'form': form, 'summary': summary})
    else:
        form = CSVUploadForm()
    return render(request, 'users/csv_upload.html', {'form': form})


def format_errors(errors):
    messages = []
    for field, error_list in errors.items():
        for error in error_list:
            messages.append(f"{field}: {error}")
    return ", ".join(messages)

def list_users(request):

    users = User.objects.all()

    if filter_name := request.GET.get('name', '').strip():
        users = users.filter(name__icontains=filter_name)
    if filter_email := request.GET.get('email', '').strip():
        users = users.filter(email__icontains=filter_email)

    return render(request, 'users/users_list.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('list_users')