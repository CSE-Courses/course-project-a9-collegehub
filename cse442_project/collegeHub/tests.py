from django.test import TestCase, Client
from collegeHub.models import Experiences, Specific, Section, User, UserProfile, Education, Skill, Event, Project
from collegeHub.views import create_experience
import requests
# Create your tests here.


class ExperienceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.UserProfile = UserProfile.objects.create(user=self.user)
        self.UserProfile.save()

    def test_create_experience(self):
        user = self.UserProfile
        create_experience(user)
        self.assertEqual(Experiences.objects.filter(pk=1).exists(), True)

    def test_experience_links_to_user(self):
        user = self.UserProfile
        create_experience(user)
        # Get user from experience
        self.assertEqual(Experiences.objects.filter(pk=1).get(pk=1).profile.user.username, self.user.username)
        self.assertEqual(Experiences.objects.filter(pk=1).get(pk=1).profile.user.email, self.user.email)
        # Get experience from user
        self.assertEqual(Experiences.objects.filter(pk=1).get(pk=1), self.UserProfile.experience)

class EventTest(TestCase):
    def setup(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.UserProfile = UserProfile.objects.create(user=self.user)
        self.UserProfile.save()
        self.event = Event.objects.create(profile=self.UserProfile)
        self.experience.save()


class SectionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.UserProfile = UserProfile.objects.create(user=self.user)
        self.UserProfile.save()
        self.experience = Experiences.objects.create(profile=self.UserProfile)
        self.experience.save()

    def test_section_links_to_experience(self):
        self.section = Section.objects.create(name='test_name', experiences=self.experience)
        self.section.save()

        # Can get experience from section
        self.assertEqual(Section.objects.filter(pk=1).get(pk=1).experiences, self.experience)

    def test_multiple_sections_to_one_experience(self):
        self.section1 = Section.objects.create(name='test_1', experiences=self.experience)
        self.section1.save()
        self.section2 = Section.objects.create(name='test_2', experiences=self.experience)
        self.section2.save()

        # Can get experience from section
        self.assertEqual(Section.objects.filter(pk=1).get(pk=1).experiences.profile.user.username, self.experience.profile.user.username)
        self.assertEqual(Section.objects.filter(pk=2).get(pk=2).experiences.profile.user.username, self.experience.profile.user.username)


class SpecificTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.UserProfile = UserProfile.objects.create(user=self.user)
        self.UserProfile.save()
        self.experience = Experiences.objects.create(profile=self.UserProfile)
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


class EducationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.userProfile.save()

    def test_education_links_to_profile(self):
        self.education = Education.objects.create(profile=self.userProfile)
        self.education.save()

        # Can get experience from section
        self.assertEqual(Education.objects.filter(pk=1).get(pk=1).profile, self.userProfile)

    def test_multiple_education_to_one_profile(self):
        self.education = Education.objects.create(profile=self.userProfile)
        self.education.save()
        self.education = Education.objects.create(profile=self.userProfile)
        self.education.save()

        # Can get experience from section
        self.assertEqual(Education.objects.filter(pk=1).get(pk=1).profile.user.username,
                         self.userProfile.user.username)
        self.assertEqual(Education.objects.filter(pk=2).get(pk=2).profile.user.username,
                         self.userProfile.user.username)


class SkillTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.userProfile.save()

    def test_skill_links_to_profile(self):
        self.skill = Skill.objects.create(profile=self.userProfile)
        self.skill.save()

        # Can get experience from section
        self.assertEqual(Skill.objects.filter(pk=1).get(pk=1).profile, self.userProfile)

    def test_multiple_skill_to_one_profile(self):
        self.skill = Skill.objects.create(profile=self.userProfile)
        self.skill.save()
        self.skill = Skill.objects.create(profile=self.userProfile)
        self.skill.save()

        # Can get experience from section
        self.assertEqual(Skill.objects.filter(pk=1).get(pk=1).profile.user.username,
                         self.userProfile.user.username)
        self.assertEqual(Skill.objects.filter(pk=2).get(pk=2).profile.user.username,
                         self.userProfile.user.username)

class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='email@email.com',
                                        password='password1234')
        self.user.save()
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.userProfile.save()

    def test_project_links_to_profile(self):
        self.progress = Project.objects.create(profile=self.userProfile)
        self.progress.save()

        # Can get experience from section
        self.assertEqual(Project.objects.filter(pk=1).get(pk=1).profile, self.userProfile)

    def test_multiple_skill_to_one_profile(self):
        self.progress = Project.objects.create(profile=self.userProfile)
        self.progress.save()
        self.progress = Project.objects.create(profile=self.userProfile)
        self.progress.save()

        # Can get experience from section
        self.assertEqual(Project.objects.filter(pk=1).get(pk=1).profile.user.username,
                         self.userProfile.user.username)
        self.assertEqual(Project.objects.filter(pk=2).get(pk=2).profile.user.username,
                         self.userProfile.user.username)