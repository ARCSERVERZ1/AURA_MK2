from django.test import TestCase

# Create your tests here.

str = "xyz.csv"
if str.endswith(".pdf"):
    print("The string ends with '.pdf'")
else:
    print("The string does not end with '.pdf'")
