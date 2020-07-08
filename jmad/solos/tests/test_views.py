from django.test import TestCase, RequestFactory

from solos.views import index

class IndexViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test the index view returns a 200 response and uses
        The correct template
        """
        request = self.factory.get('/')
        with self.assertTemplateUsed('solos/index.html'):
            response = index(request)
            self.assertEqual(response.status_code, 200)
