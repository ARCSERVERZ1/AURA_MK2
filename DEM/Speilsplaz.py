




ab = ['b','b','a','a','a']



z = {}
for i , j in enumerate(ab):
    try:
        z[j] = z[j]+i
    except:
        z[j] = i

print(z)