
'''
This is a test module, which can flatter a list, up to 3 levels
'''

def print_lol(list_x):
  '''
  test con
  '''
  for i in list_x:
      if isinstance(i,list):
          for j in i:
              if isinstance(j,list):
                  for k in j:
                      print (k)
              else:
                  print(j)
      else:
          print(i)