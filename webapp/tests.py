"""HTTP tests for the JSON-backed Django pages."""

from django.test import SimpleTestCase
from django.urls import reverse


class WebPageTests(SimpleTestCase):
    """Check routing, rendering and the 404 response without a database."""

    def test_home_page_opens(self):
        response = self.client.get(reverse("webapp:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Система учёта посетителей")

    def test_visitor_list_uses_named_namespace(self):
        response = self.client.get(reverse("webapp:visitor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Посетители")

    def test_dynamic_visitor_page_opens(self):
        response = self.client.get(reverse("webapp:visitor_detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_unknown_dynamic_identifier_returns_404(self):
        response = self.client.get(reverse("webapp:visit_detail", args=[999999]))
        self.assertEqual(response.status_code, 404)
