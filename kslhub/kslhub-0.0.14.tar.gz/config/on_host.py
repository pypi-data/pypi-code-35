c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'
c.Spawner.http_timeout = 120
#------------------------------------------------------------------------------
# ProfilesSpawner configuration
#------------------------------------------------------------------------------
# List of profiles to offer for selection. Signature is:
#   List(Tuple( Unicode, Unicode, Type(Spawner), Dict ))
# corresponding to profile display name, unique key, Spawner class,
# dictionary of spawner config options.
# 
# The first three values will be exposed in the input_template as {display},
# {key}, and {type}
#
c.ProfilesSpawner.profiles = [
       ( "Host process", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip':'0.0.0.0'} ),
 ]

 
