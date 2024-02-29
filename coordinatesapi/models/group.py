from django.db import models

class Group(models.Model):
    uuid = models. UUIDField()
    name = models.CharField(max_length=50)

    def guests(self):
        return [guest_group.guest for guest_group in self.guest_groups.all()]
