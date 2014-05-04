from subprocess import call
import os

for root, dirs, files in os.walk('../src'):
	for file in files:
		if not file.endswith('py'):
			continue

		path = os.path.join(root, file)
		print path

		script = open(path).read()
		open(path, 'w').write(script.replace('\t', '    '))
