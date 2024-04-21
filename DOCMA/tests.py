from django.test import TestCase

# Create your tests here.

import os


parent_dir = os.path.dirname(os.getcwd())
os.chdir(parent_dir)


new_doc_path = "assets/Documents/kis"






if not os.path.exists(new_doc_path):os.mkdir(new_doc_path)





