from django.db import models
import os
from uuid import uuid4

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


class Player(models.Model):
    name = models.CharField(max_length=20, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Participation(models.Model):
    game = models.ForeignKey("Game", related_name="participations", null=False)
    player = models.ForeignKey("Player", related_name="participations", null=True, blank=True)
    character = models.ForeignKey("Character", related_name="participation", null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.game) + ": " + str(self.player) + " " + str(self.character)

class Character(models.Model):
    name = models.CharField(max_length=20, blank=False)
    template = models.ForeignKey("Template", related_name="characters", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Value(models.Model):
    character = models.ForeignKey("Character", related_name="values", null=False)
    field = models.ForeignKey("Field", related_name="values", null=False)
    value = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.character) + ": "

class Game(models.Model):
    name = models.CharField(max_length=50, blank=False)
    universe = models.ForeignKey("Universe", related_name="games", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Note(models.Model):
    name = models.CharField(max_length=50, blank=False)
    text = models.TextField(blank=True)
    game = models.ForeignKey("Game", related_name="notes", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Universe(models.Model):
    name = models.CharField(max_length=20, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to=path_and_rename("media/templates/"), null=False)
    universe = models.ForeignKey("Universe", related_name="template", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.universe) + " - " + str(self.name)

class Field(models.Model):
    name = models.CharField(max_length=40, blank=False)
    position_x = models.IntegerField(null=False, default=0)
    position_y = models.IntegerField(null=False, default=0)
    scale_x = models.IntegerField(null=False, default=0)
    scale_y = models.IntegerField(null=False, default=0)
    template = models.ForeignKey("Template", related_name="fields", null=False)

    def __str__(self):
        return self.name

class Map(models.Model):
    name = models.CharField(max_length=20, blank=False)
    active = models.BooleanField()
    game = models.ForeignKey("Game", related_name="maps", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Layer(models.Model):
    name = models.CharField(max_length=20, blank=False)
    layer_height = models.IntegerField(null=False)
    map = models.ForeignKey("Map", related_name="layers", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Entity(models.Model):
    class Meta:
        verbose_name_plural = "Entities"
    position_x = models.IntegerField(null=False, default=0)
    position_y = models.IntegerField(null=False, default=0)
    scale_x = models.IntegerField(null=False, default=0)
    scale_y = models.IntegerField(null=False, default=0)
    layer = models.ForeignKey("Layer", related_name="entities", null=False)
    sprite = models.ForeignKey("Sprite", related_name="entities", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sprite)

class Sprite(models.Model):
    name = models.CharField(max_length=20, blank=False)
    image = models.ImageField(upload_to="media/sprites/", null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

