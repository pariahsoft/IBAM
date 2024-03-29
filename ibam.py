############################
## Itsy Bitsy Album Maker  #
## By Michael D. Reiley    #
## Copyright 2011 OmegaSDG #
############################

# This script is to be embedded in an iframe.

import os, locale

## Config ##

bgcolor = "#ffffff" # Background color of page.
album = "images/" # Directory containing album images. (Needs trailing slash.)
count = 5 # Number of images to show at once. Must be odd.
thumbsize = [100, 100] # Width and height for thumbnails.
midsize = [200, 200] # Width and height for center image.
larrow = "left.png" # Left arrow image.
rarrow = "right.png" # Right arrow image.
loc = "en_US.UTF-8" # Your locale string for filename sorting. Leave alone if unsure.

## Setup and Functions ##

images = os.listdir(album) # Fill images array with alphabetized image paths.
locale.setlocale(locale.LC_ALL, loc)
images = sorted(images, cmp=locale.strcoll)
i = 0
while i < len(images):
	images[i] = album+images[i]
	i += 1

first = -(count/2) # First image position.

def get(index): # Helper function to cycle the image list.
	return images[index % len(images)]

## Generate Album ##

if "REQUEST_METHOD" in os.environ: # Are we on a webserver?
		print "Content-type: text/html\n"

print '''<!doctype html>

<html>
<head>
	<title>This should be embedded.</title>
	<style type="text/css">
		body {
			background-color: '''+bgcolor+''';
			padding: 0;
			margin: 0;
		}
		a {
			padding-left: 5px;
			padding-right: 5px;
		}
		a img {
			border: 0;
		}
		a:link, a:visited, a:active, a:hover {
			text-decoration: none;
		}
		a:active
		{
			outline: none;
		}
		a:focus
		{
			-moz-outline-style: none;
		}
		.thumb {
			width: '''+str(thumbsize[0])+'''px;
			height: '''+str(thumbsize[1])+'''px;
		}
		.full {
			width: '''+str(midsize[0])+'''px;
			height: '''+str(midsize[1])+'''px;
		}
	</style>
	<script type="text/javascript">
		var pos = '''+str(first)+''';
		var images = new Array();'''

i = 0 # Pass the list of images to a javascript array.
while i < len(images):
	print "\t\timages["+str(i)+"] = \""+images[i]+"\";"
	i+= 1

print '''
		// Preload images.
		function preloader() {
			var tmp = new Image();
			tmp.src = "'''+larrow+'''";
			tmp.src = "'''+rarrow+'''";
			var i = 0;
			while (i < images.length) {
				var img = new Image();
				img.src = images[i];
				images[i] = img.src;
				i += 1;
			}
		}
		
		// Make sure page is loaded before loading images.
		// Courtesy of http://perishablepress.com/
		function onLoad(func) {
			var oldonload = window.onload;
			if (typeof window.onload != 'function') {
				window.onload = func;
			} else {
				window.onload = function() {
					if (oldonload) {
						oldonload();
					}
					func();
				}
			}
		}
		
		// Get an image from the list, work around negative modulus bug.
		function get(index)
		{
			return images[(((index % images.length) + images.length) % images.length)];
		}
		
		// Cycle the images.
		function move()
		{
			var i = 0;
			while (i < '''+str(count)+''')
			{
				document.getElementById("img"+i).src = get(pos+i);
				document.getElementById("a"+i).href = get(pos+i);
				i += 1;
			}
		}
		
		function prev()
		{
			pos -= 1;
			move();
		}
		
		function next()
		{
			pos += 1;
			move();
		}
		
		onLoad(preloader());
	</script>
</head>
<body>
	<a href="javascript:prev()">
		<img src="'''+larrow+'''" />
	</a>'''
i = 0
while i < count: # Insert initial album images.
	if i == (count / 2):
		print "\t<a id=\"a"+str(i)+"\" href=\""+get(i+first)+"\" target=\"_blank\">"
		print "\t\t<img class=\"full\" id=\"img"+str(i)+"\" src=\""+get(i+first)+"\" />"
		print "\t</a>"
		i += 1
	print "\t<a id=\"a"+str(i)+"\" href=\""+get(i+first)+"\" target=\"_blank\">"
	print "\t\t<img class=\"thumb\" id=\"img"+str(i)+"\" src=\""+get(i+first)+"\" />"
	print "\t</a>"
	i += 1
print '''	<a href="javascript:next()">
		<img src="'''+rarrow+'''" />
	</a>
</body>
</html>
'''

