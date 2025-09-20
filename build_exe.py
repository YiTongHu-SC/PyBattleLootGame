import yaml
import subprocess

with open('config/build.yaml', 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

cmd = [
    'pipenv', 'run', 'pyinstaller',
    '--onefile',
    '--name', cfg['name'],
    '--icon', cfg['icon'],
    # 添加数据文件到打包中
    '--add-data', 'data;data',
    '--add-data', 'config;config',
    cfg['entry']
]
subprocess.run(cmd)