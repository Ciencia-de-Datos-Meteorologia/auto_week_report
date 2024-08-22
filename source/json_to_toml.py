import json
import toml

with open('client_secret.json') as text:
    a = json.load(text)
    a = {'client_secret': a}
    print(a)
    tml = toml.dumps(a)
    print('\nToml:\n', tml)
    with open('client_secret.toml', 'x') as toml_file:
        toml_file.writelines(tml)
