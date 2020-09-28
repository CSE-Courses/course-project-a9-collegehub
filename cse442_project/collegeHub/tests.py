from django.test import TestCase
from collegeHub.models import Ex


# Create your tests here.

class BasicTest(TestCase):
    def setUp(self):
        Ex.objects.create(name="mike")

    def test_basic(self):
        print('kill me')
        e = Ex.objects.get(name='mike')
        print(e.name)
#         ex = Ex()
#         ex.name = 'mike'
#         ex.save()
#
#         record = ex.objects.get(pk=1)
#         self.assertEqual(record, ex)

