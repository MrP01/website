from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site


class MeetupManager(models.Manager):
    def get_past_meetups(self):
        """
        Adds a filter for meetups that started in the past.
        """
        now = timezone.now()
        return self.get_query_set().filter(start_date__lt=now)


class SessionManager(models.Manager):
    def get_proposals(self):
        """
        Adds a filter for sessions that are not assigned to a meetup yet.
        """
        return self.get_query_set().filter(meetup__isnull=True)


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('location')
        verbose_name_plural = _('locations')


class Meetup(models.Model):
    start_date = models.DateTimeField()
    location = models.ForeignKey(Location, blank=True, null=True)
    meetupcom_id = models.CharField(blank=True, null=True, max_length=20)
    notes = models.TextField(blank=True, null=True)

    objects = MeetupManager()

    def __unicode__(self):
        return unicode(self.start_date)

    def get_absolute_url(self):
        return reverse('view-meetup', kwargs={
            'year': "{0:0>4d}".format(self.start_date.year),
            'month': "{0:0>2}".format(self.start_date.month),
            'day': "{0:0>2d}".format(self.start_date.day),
            })

    def get_permalink(self):
        return 'http://{0}{1}'.format(
            Site.objects.get_current().domain,
            reverse('meetup-permalink', kwargs={
                'pk': self.pk
            }))

    def is_in_future(self):
        now = timezone.now()
        return self.start_date > now

    class Meta(object):
        verbose_name = 'Meetup'
        verbose_name_plural = 'Meetups'
        ordering = ('-start_date',)


class Session(models.Model):
    title = models.CharField("Titel", max_length=255)
    abstract = models.TextField("Kurzbeschreibung")
    meetup = models.ForeignKey(Meetup, verbose_name="Meetup", blank=True,
        null=True, related_name='sessions')
    speaker_name = models.CharField("Vortragender", max_length=100, blank=True,
        null=True)
    speaker_email = models.EmailField("E-Mail-Adresse", blank=True, null=True)
    speaker = models.ForeignKey(auth_models.User, verbose_name="Vortragender",
        blank=True, null=True)
    slides_url = models.URLField("Folien-URL", blank=True, null=True)
    notes = models.TextField("Notizen", blank=True, null=True)

    objects = SessionManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view-session', kwargs={'pk': self.pk})

    def get_permalink(self):
        return 'http://{0}{1}'.format(
            Site.objects.get_current(),
            self.get_absolute_url())

    def get_speaker_name(self):
        if self.speaker:
            firstname = self.speaker.first_name
            lastname = self.speaker.last_name
            if firstname is not None and lastname is not None:
                return '{0} {1}'.format(firstname, lastname)
            if firstname is not None:
                return firstname
            return self.speaker.username
        return self.speaker_name

    class Meta(object):
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
