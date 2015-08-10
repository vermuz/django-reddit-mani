from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blat(models.Model):
	text = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	via = models.URLField(blank=True) # URL Field - optional field hence blank = True
	# who created what - Foreign Key Reference
	created_by = models.ForeignKey(User)
    
    # How many people liked our blate
	def total_likes(self):
		return self.like_set.count()

	def __unicode__(self):
		return self.text[:50]

class Like(models.Model):
	blat = models.ForeignKey(Blat)

# General way of creating a User profile
# Extra JOIN is done for extracting User info
class Profile(models.Model):
	user = models.OneToOneField(User)
	bio  = models.TextField(blank=True) #Optional
	blog = models.URLField(blank=True)
