from django.test import TestCase, Client
from collegeHub.models import Experiences, Specific, Section, User
from collegeHub.views import create_experience, create_section, create_specific
import requests
# Create your tests here.


class ExperienceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()

    def test_create_experience(self):
        user = self.user
        create_experience(user)
        self.assertEqual(Experiences.objects.filter(pk=1).exists(), True)

    def test_experience_links_to_user(self):
        user = self.user
        create_experience(user)
        # Get user from experience
        self.assertEqual(Experiences.objects.filter(pk=1).get(pk=1).user.username, self.user.username)
        self.assertEqual(Experiences.objects.filter(pk=1).get(pk=1).user.email, self.user.email)
        # Get experience from user
        self.assertEqual(Experiences.objects.filter(pk=1).get(pk=1), self.user.experience)


class SectionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.experience = Experiences.objects.create(user=self.user)
        self.experience.save()

    def test_create_section(self):
        c = Client()
        c.post('/section', data={'name': 'test', 'experience_id': '1'}, content_type='application/json')
        # create_section(request)
        self.assertEqual(Section.objects.filter(pk=1).exists(), True)

    def test_section_links_to_experience(self):
        c = Client()
        c.post('/section', data={'name': 'test', 'experience_id': '1'}, content_type='application/json')

        # Can get experience from section
        self.assertEqual(Section.objects.filter(pk=1).get(pk=1).experiences, self.experience)

    def test_multiple_sections_to_one_experience(self):
        c = Client()
        c.post('/section', data={'name': 'test1', 'experience_id': '1'}, content_type='application/json')
        c.post('/section', data={'name': 'test2', 'experience_id': '1'}, content_type='application/json')
        # Can get experience from section
        self.assertEqual(Section.objects.filter(pk=1).get(pk=1).experiences, self.experience)
        self.assertEqual(Section.objects.filter(pk=2).get(pk=2).experiences.user.username, self.experience.user.username)


class SpecificTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.experience = Experiences.objects.create(user=self.user)
        self.experience.save()
        self.section = Section.objects.create(experiences=self.experience, name='test')
        self.section.save()

    def test_specific_links_to_section(self):
        self.specific = Specific.objects.create(image=None, description='This is a test', bullet_section='this, is, a, test', section=self.section)
        self.specific.save()
        # Can get experience from section
        self.assertEqual(Specific.objects.filter(pk=1).get(pk=1).section, self.section)

    def test_make_list(self):
        self.specific = Specific.objects.create(image=None, description='This is a test',
                                                bullet_section='This, is, a, test', section=self.section)
        self.specific.save()
        list = self.specific.get_bullet_list()
        self.assertEqual(list, ['This', 'is', 'a', 'test'])
