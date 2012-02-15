from django.utils import unittest
from django.contrib.auth.models import User
from confucius.models import Profile, Language, EmailAddress, PostalAddress

class ProfileTestCase(unittest.TestCase):
    def test_profile_creation(self):
        p = Profile.objects.create(last_name="b")
        e = EmailAddress.objects.create(name="blu",
                value="asasaasaasaeza@e.fr", profile=p)
        p.first_name ="lol"
        p.save()
        print Profile.objects.get(last_name="b").first_name

        for e in p.email_addresses.all():
            print e

"""
class UserTestCase(unittest.TestCase):

    def setUp(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Language.objects.all().delete()
        self.user = User.objects.create(last_name="DURAND", first_name="Jean-Pierre", email="durand.jeanpierre@gmail.com",  username="jpduran", password="kikou")
        lang = Language.objects.create(code="FR", name="French")
        profile = Profile.objects.create(secondary_email="tareus@gmail.com", primary_postal_address="12 rue de mon coeur 92220 ANTONY", secondary_postal_address="34 avenue de paris PARIS", user=self.user)
        profile.languages.add(lang)
        self.user.save()


    def test_missing_arguments(self):
        self.assertRaises(ValidationError, lambda: User.objects.create())
        self.assertRaises(ValidationError,
                lambda: User.objects.create(username="test"))
        self.assertRaises(ValidationError,
                lambda: User.objects.create(username="foo", password="bar"))
        self.assertRaises(ValidationError,
                lambda: User.objects.create(
                    username="ni", password="rah", last_name="mit"))
        self.assertRaises(ValidationError,
                lambda: User.objects.create(
                    username="blu", password="red", last_name="sky"))

    def test_unicity(self):
        u = User.objects.create(
                username="user1", password="doesntmatter", last_name="user1",
                email="user1@user1.com")
        u.pk = None
        self.assertRaises(ValidationError,
                lambda: u.save())
        u.pk = None
        u.username = "user2"
        self.assertRaises(ValidationError,
                lambda: u.save())
        u.pk = None
        u.username = "user1"
        u.email = "user2@user2.com"
        self.assertRaises(ValidationError,
                lambda: u.save())

    def test_user_creation(self):
        myuser = User.objects.get(username="jpduran")
        self.assertEqual(myuser, self.user)
        

    def test_multiple_languages(self):
        lang1 = Language.objects.create(code="DE", name="German")
        lang2 = Language.objects.create(code="ES", name="Spanish")
        lang3 = Language.objects.create(code="CI", name="Chinese")
        blu = [lang1, lang2, lang3]
        for lang in blu:        
            self.user.get_profile().languages.add(lang)
    

    def test_identical_email(self):
        with self.assertRaises(ValidationError):
            myuser = User.objects.create(last_name="traitor", first_name="fake", email="durand.jeanpierre@gmail.com", username="fake", password="fake") 

    def test_identical_username(self):
        with self.assertRaises(ValidationError):
            myuser = User.objects.create(last_name="traitor", first_name="fake", email="fake@gmail.com", username="jpduran", password="fake") 
            
    def test_username_null(self):
        with self.assertRaises(ValidationError):
            myuser = User.objects.create(last_name="traitor", first_name="fake", email="fake@gmail.com", password="fake")
            myprofile = Profile.objects.create(secondary_email="fake@gmail.com", secondary_postal_address="fake", user=myuser)


    def test_user_change_field(self):
        u = User.objects.get(username="jpduran")
        self.user.last_name="Fernandes"
        self.user.first_name="Lucas"
        self.user.email="lucskywalkerzero@gmail.com"
        self.user.username="lferna05"
        self.user.password="lucas"
        self.user.save()
        self.assertNotEquals(self.user.last_name, u.last_name)
        self.assertNotEquals(self.user.first_name, u.first_name)
        self.assertNotEquals(self.user.email, u.email)
        self.assertNotEquals(self.user.username, u.username)
        self.assertNotEquals(self.user.password, u.password)
        
    def test_profile_change_field(self):
        u = User.objects.get(username="jpduran").get_profile()
        self.user.get_profile().secondary_email="lucskywalkerzero@gmail.com"
        self.user.get_profile().primary_postal_address="10 rue dans tes fesses du NEUF DEUX"
        self.user.get_profile().secondary_postal_address="Ou pas"
        self.user.get_profile().languages.clear()
        self.user.get_profile().languages.add(Language.objects.create(code="DE", name="German"))
        self.user.get_profile().save()
        self.assertNotEquals(self.user.get_profile().secondary_email, u.secondary_email)
        self.assertNotEquals(self.user.get_profile().primary_postal_address, u.primary_postal_address)
        self.assertNotEquals(self.user.get_profile().secondary_postal_address, u.secondary_postal_address)
        self.assertNotEquals(self.user.get_profile().languages, u.languages)

    
"""
