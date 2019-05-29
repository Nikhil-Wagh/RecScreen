from mss import mss
from datetime import datetime
from threading import Thread
from os import path, makedirs
import errno
import subprocess


def saveImages(stop):
	with mss() as sct:
		start = datetime.now()
		n = 1
		while True:
			filename = 'images/image-{:05d}.png'.format(n)
			sct.shot(output=filename)
			n += 1
			if stop():
				break
		end = datetime.now()
		print("FPS: {fps}".format(fps = round(n/(end-start).total_seconds(), 3)))


def saveMovie():
	# command = "ffmpeg -f image2 -i images/image-%05d.png -qscale 0 -y output/Movie.avi"
	failed = subprocess.call([
				'ffmpeg',
				'-f', 'image2',
				'-i', 'images/image-%05d.png',
				'-q:v', '0',
				'-y', 'output/Movie.avi'
			])
	if failed:
		print("Failed to render video")
	else:
		remOldImages()

def remOldImages():
	try:
		subprocess.call([
				'rm',
				'-r', 'images'
			])
	except Exception as e:
		print("Unable to remove images")


def createDirectories():
	try:
		makedirs('images')
		makedirs('output')
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
		

def main():
	createDirectories()
	stopSaveImages = False
	print("Type 'S' to stop")
	t_saveImages = Thread(target = saveImages, args = (lambda: stopSaveImages, ))
	t_saveImages.start()
	choice = raw_input("Whenever you're ready: ")
	if choice == "S":
		stopSaveImages = True
		t_saveImages.join()
		print("Getting your movie")
		saveMovie()

		
if __name__ == '__main__':
	main()

# ffmpeg -f image2 -i image-%05d.png -qscale 0 -y movie.avi