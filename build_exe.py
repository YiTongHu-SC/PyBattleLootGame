import yaml
import subprocess

with open('config/build.yaml', 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

cmd = [
    'pipenv', 'run', 'pyinstaller',
    '--onefile',
    '--name', cfg['name'],
    '--icon', cfg['icon'],
    cfg['entry']
]
subprocess.run(cmd)