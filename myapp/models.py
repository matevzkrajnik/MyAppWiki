from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class UporabnikProfil(models.Model):
    uporabnik = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil', null=True, unique=True)
    slika_profila = models.ImageField(blank=True, default='profili/user-default.png', upload_to='profili')

    def __str__(self):
        return self.uporabnik.first_name + " " + self.uporabnik.last_name
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    '''

class Stran(models.Model):
    datum_nastanka = models.DateTimeField('datum nastanka', null='True')
    naslov = models.CharField(max_length=200)
    vsebina = models.TextField()
    sporocilo = models.TextField()
    avtor = models.ForeignKey(UporabnikProfil, null='True')

    def __str__(self):
        return self.naslov
    '''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    '''


