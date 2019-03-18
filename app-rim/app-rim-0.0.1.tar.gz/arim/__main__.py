import arim.layout,sys

if len(sys.argv) == 2:
  arim.layout.tarApp(sys.argv[1])
else:
  print("arim <app_name>\n\tapp_name - the name of application to backup")
