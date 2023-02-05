from get_ip import get_ip
from pathlib import Path
import sys

localIP = get_ip()

f = open(Path(__file__).parent / '../mball/IP_host.txt', 'w')
f.write('%s\n' % localIP)
f.close()

f = open(Path(__file__).parent / '../mball/IP_client.txt', 'w')
f.write('%s\n' % sys.argv[1])
f.close()
