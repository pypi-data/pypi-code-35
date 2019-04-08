from keyvaultlib.key_vault import KeyVaultOAuthClient

c = KeyVaultOAuthClient('3dd5c156-99eb-4e00-8439-56be9a17871c', '+lTF8XYILtk1DcCN7ctFUYx3lEaM4+grC2QLceF1nGo=', '72f988bf-86f1-41af-91ab-2d7cd011db47')
c.get_secret_with_key_vault_name('rainman-kb-vault', 'InterflowSubscriptionKey')

x = None