from django.contrib.auth.models import AbstractUser  
from django.db import models  
from django.utils import timezone

class User(AbstractUser):  

    EDUCATION_CHOICE = [        
        ("SSC", "Secondary School Certificate"),
        ("HSC", "Higher Secondary Certificate"),
        ("AD", "Associate Degree"),
        ("BACHELOR", "Bachelor’s Degree (BA, BSc, BBA, BE, B.Tech, etc.)"),
        ("MASTER", "Master’s Degree (MA, MSc, MBA, M.Tech, etc.)"),
        ("PHD", "Doctorate (PhD, EdD, DSc, etc.)"),
        ("POSTDOC", "Postdoctoral Research (Postdoc)"),
        ("DIPLOMA", "Diploma (Dip.)"),
        ("CERT", "Certificate Program (Cert.)"),
        ("VT", "Vocational Training (VT)"),
        ("NFE", "No Formal Education")
    ]

    education = models.CharField(max_length=50, choices=EDUCATION_CHOICE)
    subjects_of_interest = models.ManyToManyField('Subject', blank=False)
    bio = models.TextField(max_length=140, blank=True)
    researcher = models.BooleanField(default=False) # if this user has at-least one PR merged and the doc was published
    profile_picture = models.ImageField(upload_to = "profile_images", default="prfile_images/placeholder.jpeg")
    reputation = models.IntegerField(default=0) # total upvotes this user has 

class PublisherRoom(models.Model) :

    """reputations/upvotes"""
    up_votes = models.IntegerField()
    down_votes = models.IntegerField()
    members = models.ManyToManyField('User', related_name = 'publisher_rooms')
    moderators = models.ManyToManyField('User', related_name = 'moderated_rooms')
    subject_tags = models.ManyToManyField('Subject', related_name = 'subject_tag')
    room_ = models.CharField(max_length=255)
    specific_for_document = models.BooleanField(default=False)
    document = models.ForeignKey('Document' ,blank=True, null= True, on_delete= models.CASCADE) # only if the Room is specific to a document
    documents = models.ManyToManyField('Document', blank= True, null = True, related_name= 'publisher_room_articles')


class Subject(models.Model):
    # subject tage for the classrooms
    SUBJECT_CHOICES = [
    # Core Sciences
    ('MAT', 'Mathematics'), ('PHY', 'Physics'), ('CHE', 'Chemistry'), ('BIO', 'Biology'), ('ASTRO', 'Astronomy'),
    ('GEOL', 'Geology'), ('METEO', 'Meteorology'), ('OCEAN', 'Oceanography'), ('ECO', 'Ecology'), ('GEN', 'Genetics'),
    ('NEURO', 'Neuroscience'), ('BTEK', 'Biotechnology'), ('PHARM', 'Pharmacology'), ('IMMU', 'Immunology'), ('PATH', 'Pathology'),
    
    # Technology & Engineering
    ('CS', 'Computer Science'), ('DS', 'Data Science'), ('AI', 'Artificial Intelligence'), ('ML', 'Machine Learning'), ('ROB', 'Robotics'),
    ('CYB', 'Cybersecurity'), ('NANO', 'Nanotechnology'), ('QE', 'Quantum Engineering'), ('CE', 'Civil Engineering'), 
    ('ME', 'Mechanical Engineering'), ('EE', 'Electrical Engineering'), ('AERO', 'Aerospace Engineering'), 
    ('CHEM', 'Chemical Engineering'), ('BME', 'Biomedical Engineering'), ('ENE', 'Energy Engineering'),
    
    # Social Sciences
    ('PSY', 'Psychology'), ('SOC', 'Sociology'), ('ANTH', 'Anthropology'), ('POL', 'Political Science'), ('ECO', 'Economics'),
    ('LING', 'Linguistics'), ('GEOG', 'Geography'), ('IR', 'International Relations'), ('CRIM', 'Criminology'), ('URB', 'Urban Planning'),
    ('SW', 'Social Work'), ('DEV', 'Development Studies'), ('GEND', 'Gender Studies'), ('DIS', 'Disability Studies'),
    ('CLIM', 'Climate Science'),
    
    # Humanities
    ('HIS', 'History'), ('PHIL', 'Philosophy'), ('LIT', 'Literature'), ('LANG', 'Modern Languages'), ('CLAS', 'Classical Studies'),
    ('REL', 'Religious Studies'), ('MYTH', 'Mythology'), ('ART', 'Art History'), ('MUS', 'Musicology'), ('ARCH', 'Archaeology'),
    ('CUL', 'Cultural Studies'), ('ETH', 'Ethics'), ('THEO', 'Theology'), ('COMPL', 'Comparative Literature'), 
    ('DH', 'Digital Humanities'),
    
    # Professional Fields
    ('MED', 'Medicine'), ('LAW', 'Law'), ('BUS', 'Business Administration'), ('ACC', 'Accounting'), ('FIN', 'Finance'),
    ('MKT', 'Marketing'), ('HR', 'Human Resources'), ('ENT', 'Entrepreneurship'), ('PA', 'Public Administration'), ('EDU', 'Education'),
    ('JOUR', 'Journalism'), ('COM', 'Communication'), ('ARCHI', 'Architecture'), ('DES', 'Design'), ('NURS', 'Nursing'),
    ('PHARM', 'Pharmacy'), ('VET', 'Veterinary Science'), ('FOREN', 'Forensic Science'), ('ACCT', 'Actuarial Science'), 
    ('SPORT', 'Sports Science'),
    
    # Interdisciplinary & Emerging Fields
    ('COG', 'Cognitive Science'), ('ENV', 'Environmental Science'), ('SUST', 'Sustainability Studies'), ('BIOINF', 'Bioinformatics'), 
    ('GAME', 'Game Design'), ('VR', 'Virtual Reality'), ('BLOCK', 'Blockchain'), ('ETHIC', 'Digital Ethics'), ('ASTROB', 'Astrobiology'),
    ('EPI', 'Epidemiology'), ('MATHB', 'Mathematical Biology'), ('MARB', 'Marine Biology'), ('PALEO', 'Paleontology'), 
    ('AERO', 'Aeronautics'), ('MIL', 'Military Science'),
    
    # Arts & Creative
    ('FINE', 'Fine Arts'), ('THEA', 'Theater Arts'), ('FILM', 'Film Studies'), ('DAN', 'Dance'), ('CW', 'Creative Writing'),
    ('GD', 'Graphic Design'), ('FD', 'Fashion Design'), ('ID', 'Industrial Design'), ('NUTR', 'Nutrition'), ('PEACE', 'Peace Studies')
    ]
    name = models.CharField(max_length=6, choices= SUBJECT_CHOICES)
    pass

class RoomMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="room_messages")
    message_mentioned = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    room = models.ForeignKey(PublisherRoom, on_delete= models.CASCADE, related_name= "messages")


    def get_date(self):
        return self.timestamp.date()

    def get_time(self):
        return self.timestamp.strftime("%H:%M")

class PersonalMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_messages")
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="recieved_messages")
    message_mentioned = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    def get_date(self):
        return self.timestamp.date()

    def get_time(self):
        return self.timestamp.strftime("%H:%M")

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_documents")
    guardians = models.ManyToManyField(User, related_name="guarded_documents", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title