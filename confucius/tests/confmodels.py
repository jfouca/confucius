from django.utils import unittest
from confucius.models import Conference, Alert, Role, ConferenceAccountRole, MessageTemplate, Account
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class ConfTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    def setUp(self):
        Conference.objects.all().delete()
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)
        self.account.save()
        
    def test_succesfful_create_conference(self):
        self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
        self.conference.save()
        reqconference = Conference.objects.get(title="UneConference")
        self.assertEquals(self.conference,reqconference)
        
        
    def test_duplicate_conference_name(self):
        self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
        self.conference.save()
        newconference = Conference.objects.get(title="UneConference")
        newconference.pk = None
        with self.assertRaises(IntegrityError):
            newconference.save()
     
  
    def test_missing_conference_name(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
 
            
    def test_missing_conference_account(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(title="UneConference", startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())

 
    def test_missing_conference_startConfDate(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(title="UneConference", president=self.account, endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())


    def test_missing_conference_endConfDate(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())


    def test_missing_conference_startSubmitDate(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())


    def test_missing_conference_endSubmitDate(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())


    def test_missing_conference_startEvaluationDate(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), endEvaluationDate=datetime.now())


    def test_missing_conference_endEvaluationDate(self):
        with self.assertRaises(IntegrityError):
            self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now())


class AlertTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    def setUp(self):
        Alert.objects.all().delete()
        Conference.objects.all().delete()
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)
        self.account.save()
        self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
        self.conference.save()

    def test_successfull_alert_creation(self):
        myconference = Conference.objects.get(title="UneConference")
        myalert = Alert.objects.create(title="my message", date=datetime.now(), content="my message content", conference=myconference)
        myalert.save()
        self.assertEquals(Alert.objects.get(title="my message"), myalert)
   
    def test_successfull_alert_creation_with_same_title_and_different_conference(self):
        myalert = Alert.objects.create(title="my message", date=datetime.now(), content="my message content", conference=self.conference)
        myalert.save()
        myalert2 = Alert.objects.get(title="my message")
        myalert2.conference = Conference.objects.create(title="UneAutreConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
        myalert2.pk = None
        myalert2.save()
            
    def test_missing_title(self):
        with self.assertRaises(IntegrityError):
            Alert.objects.create(date=datetime.now(), content="my message content", conference=self.conference)
            
    def test_missing_date(self):
        with self.assertRaises(IntegrityError):
            Alert.objects.create(title="my message", content="my message content", conference=self.conference)

            
    def test_missing_content(self):
        with self.assertRaises(IntegrityError):
            Alert.objects.create(title="my message", date=datetime.now(), conference=self.conference)

    def test_missing_conference(self):
        with self.assertRaises(IntegrityError):
            Alert.objects.create(title="my message", date=datetime.now(), content="my message content")

    def test_duplicate_alert_creation(self):
        myalert = Alert.objects.create(title="my message", date=datetime.now(), content="my message content", conference=self.conference)
        myalert.save()
        myalert2 = Alert.objects.get(title="my message", conference=self.conference)
        myalert2.pk = None
        with self.assertRaises(IntegrityError):
            myalert2.save()
        
        

class MessageTemplateTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    def setUp(self):
        MessageTemplate.objects.all().delete()
        Conference.objects.all().delete()
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)
        self.account.save()
        self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
        self.conference.save()


    def test_successfull_message_creation(self):
        mymessage = MessageTemplate.objects.create(title="UnMessage", content="Contenu", conference=self.conference)
        mymessage.save()
        self.assertEquals(MessageTemplate.objects.get(title="UnMessage"), mymessage)

   
    def test_successfull_message_creation_with_same_title_and_different_conference(self):
        otherconference = Conference.objects.create(title="UneAutreConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
        otherconference.save()
        mymessage = MessageTemplate.objects.create(title="UnMessage", content="Contenu", conference=otherconference)
        mymessage.save()
        mymessage2 = MessageTemplate.objects.create(title="UnMessage", content="Contenu", conference=self.conference)
        mymessage2.save()
 
       
    def test_missing_title(self):
        with self.assertRaises(IntegrityError):
            mymessage = MessageTemplate.objects.create(content="Contenu", conference=self.conference)
            
    def test_missing_content(self):
        with self.assertRaises(IntegrityError):
            mymessage = MessageTemplate.objects.create(title="UnMessage", conference=self.conference)

    def test_missing_conference(self):
        with self.assertRaises(IntegrityError):
            mymessage = MessageTemplate.objects.create(title="UnMessage", content="Contenu")

    def test_duplicate_message_creation(self):
        mymessage = MessageTemplate.objects.create(title="UnMessage", content="Contenu", conference=self.conference)
        mymessage.save()
        
        mymessage2 = MessageTemplate.objects.get(title="UnMessage")
        mymessage2.pk = None
        with self.assertRaises(IntegrityError):
            mymessage2.save()   
            

class RoleTestCase(unittest.TestCase):
    def setUp(self):
        Role.objects.all().delete()

    def test_successfull_role_creation(self):
        role = Role.objects.create(code="UNRO", name="UnRole")
        role.save()
        self.assertEquals(Role.objects.get(code="UNRO"), role)
 
    def test_missing_fields(self):
        with self.assertRaises(IntegrityError):
            Role.objects.create(name="UnRole")
        with self.assertRaises(IntegrityError):
            Role.objects.create(code="UNRO")

    def test_duplicate_role_creation(self):
        role = Role.objects.create(code="UNRO", name="UnRole")
        role.save()
        
        role2 = Role.objects.get(code="UNRO")
        role2.pk = None
        with self.assertRaises(IntegrityError):
            role2.save()  
            
class ConferenceAccountRoleTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    def setUp(self):
        Role.objects.all().delete()
        Conference.objects.all().delete()
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)
        self.account.save()
        self.conference = Conference.objects.create(title="UneConference", president=self.account, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
        self.conference.save()
        self.role = Role.objects.create(code="UNRO", name="UnRole")
        self.role.save()
        
    def test_successfull_AccountRole_creation(self):
        myAccountRole = ConferenceAccountRole.objects.create(account=self.account, conference=self.conference, role=self.role)
        myAccountRole.save()
        self.assertEquals(ConferenceAccountRole.objects.get(pk=myAccountRole.pk), myAccountRole)
        
    def test_duplicate_AccountRole_creation(self):
        myAccountRole = ConferenceAccountRole.objects.create(account=self.account, conference=self.conference, role=self.role)
        myAccountRole.save()
        with self.assertRaises(IntegrityError):
            myAccountRole2 = ConferenceAccountRole.objects.create(account=self.account, conference=self.conference, role=self.role)
            
    
    def test_missing_account(self):
        with self.assertRaises(IntegrityError):
            myAccountRole = ConferenceAccountRole.objects.create(conference=self.conference, role=self.role)
            

    def test_missing_conference(self):
        with self.assertRaises(IntegrityError):
            myAccountRole = ConferenceAccountRole.objects.create(account=self.account, role=self.role)
            
            
    def test_missing_role(self):
        with self.assertRaises(IntegrityError):
            myAccountRole = ConferenceAccountRole.objects.create(account=self.account, conference=self.conference)
