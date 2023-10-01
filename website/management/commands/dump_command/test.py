from django.core.management.base import BaseCommand
#from django.contrib.staticfiles import finders
import csv
import os
import mysql.connector

class Command(BaseCommand):
    help = 'test dirs'
    
    def add_argument(self, parser):
        pass
        
    def handle(self, *args, **options):
        path = os.getcwd()
        #self.stdout.write(self.style.SUCCESS(''))
        print("YOUR PATH IS THIS: " + path)


print("your path")