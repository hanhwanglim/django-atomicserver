from django.test import TestCase

from test_app.models import SomeModel


class TestAtomicView(TestCase):
    def setUp(self):
        SomeModel.objects.create(name="Some model 1")

    def test_setup_teardown(self):
        response = self.client.get("/atomic/begin/")
        self.assertEqual(response.status_code, 204)

        SomeModel.objects.create(name="Some model 2")
        self.assertEqual(SomeModel.objects.count(), 2)

        response = self.client.get("/atomic/rollback/")
        self.assertEqual(response.status_code, 204)

        self.assertEqual(SomeModel.objects.count(), 1)
