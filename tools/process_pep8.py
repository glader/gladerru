from subprocess import call
import os

for root, dirs, files in os.walk('../src'):
	for file in files:
		if not file.endswith('py'):
			continue

		print os.path.join(root, file)

		call(['autopep8', '-i', os.path.join(root, file)])
