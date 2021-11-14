thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

lista = {key for key in thisdict.items()}
print(lista)

iter_count = -1
for i in lista:
  iter_count += 1
  if iter_count == 2:
    print(i)
