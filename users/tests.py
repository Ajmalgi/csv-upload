from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from users.models import User


class UploadCSVTests(TestCase):
    def setUp(self):
        self.upload_url = reverse('upload_csv')

    def test_valid_csv_upload(self):
        csv_content = (
            "name,email,age,phone_number,gender,address\n"
            "Ajmal,ajmal@example.com,25,1234567890,Male,India\n"
            "Rahim,rahim@example.com,30,9876543210,Male,Delhi\n"
        )
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")
        response = self.client.post(self.upload_url, {'csv_file': csv_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CSV file uploaded successfully.')
        self.assertEqual(User.objects.count(), 2)

    def test_invalid_email(self):
        csv_content = (
            "name,email,age,phone_number,gender,address\n"
            "Ajmal,not-an-email,25,1234567890,Male,India\n"
        )
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")
        response = self.client.post(self.upload_url, {'csv_file': csv_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_age(self):
        csv_content = (
            "name,email,age,phone_number,gender,address\n"
            "Ajmal,ajmal@example.com,130,1234567890,Male,India\n"
        )
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")
        response = self.client.post(self.upload_url, {'csv_file': csv_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_empty_name(self):
        csv_content = (
            "name,email,age,phone_number,gender,address\n"
            ",ajmal@example.com,25,1234567890,Male,India\n"
        )
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")
        response = self.client.post(self.upload_url, {'csv_file': csv_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_duplicate_email_skipped(self):
        csv_content = (
            "name,email,age,phone_number,gender,address\n"
            "Ajmal,ajmal@example.com,25,1234567890,Male,India\n"
        )
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")
        self.client.post(self.upload_url, {'csv_file': csv_file}, follow=True)

        csv_file_duplicate = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")
        response = self.client.post(self.upload_url, {'csv_file': csv_file_duplicate}, follow=True)

        self.assertEqual(User.objects.count(), 1)

    def test_empty_file_upload(self):
        empty_csv = SimpleUploadedFile("empty.csv", b"", content_type="text/csv")
        response = self.client.post(self.upload_url, {'csv_file': empty_csv}, follow=True)
        self.assertContains(response, 'The submitted file is empty.')
        self.assertEqual(User.objects.count(), 0)

    def test_non_csv_file_rejected(self):
        txt_file = SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")
        response = self.client.post(self.upload_url, {'csv_file': txt_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Only CSV files are allowed.')
