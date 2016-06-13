import sys

def main():
	sys.stdout.write('This program adds numbers.\n')
	sum = 0
	for arg in sys.argv:
		try:
			sum = sum + float(arg)
		except:
			continue
	sys.stdout.write(str(sum))
	sys.stdout.write("Calculation finished.")
	

main()