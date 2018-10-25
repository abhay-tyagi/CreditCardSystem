from sys import argv
import zbar

def funct():
	proc = zbar.Processor()
	proc.parse_config('enable')

	device = '/dev/video0'
	
	proc.init(device)
	proc.visible = True
	proc.process_one()
	proc.visible = False

	for symbol in proc.results:
		return symbol.data


if __name__ == '__main__':
	funct()