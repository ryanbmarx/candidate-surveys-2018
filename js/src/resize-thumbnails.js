'use strict'

/*

A simple node script, using Jimp, which resizes images in one dir and writes them to another dir

"resize": "node js/src/resize-photos.js 30 ./img/thubnail"

*/

const 	fs = require('fs'),
		Jimp = require('jimp'),
		path = require('path'),
		// imageDimension = parseInt(process.argv[2]),
		imageQuality = parseInt(process.argv[2]),
		imageSrc = process.argv[3];
		// imageDest = process.argv[5];


function generateImageList(files){
	/*
		This function will take an array of filenames from the contents of a dir, 
		and return a similar array of items with specific file extensions. 
	*/

	var retval = [];

	var desiredFileTypes = [
		"jpg", "jpeg", "png"
	];

	files.forEach(function(fileName, i, a){
		const 	splitFileName = fileName.split('.'),
				testMeForFileExtension = splitFileName[splitFileName.length - 1];
		if (desiredFileTypes.indexOf(testMeForFileExtension) > -1){
			retval.push(fileName);
		}
	});
	return retval;
}


const dimensions = {
	twitter:[1024,576], // height, width
	facebook:[1200,628],
	// linkedin:[552,368],
	// pinterest:[600,900],
	// googleplus:[800,320]
}

Jimp.read(`${imageSrc}`, function(err, img){	
	// loop through social networks and output
	if (err) throw err;
	Object.keys(dimensions).forEach(n => {
		// n for networks
		const	sized = img.clone(),
				targetWidth = dimensions[n][0];
		sized.resize(targetWidth, Jimp.AUTO);

		const	currentHeight = sized.bitmap.height,
				targetHeight = dimensions[n][1],
				currentWidth = sized.bitmap.width,
				cropMargin = (currentHeight - targetHeight) / 2 < 0 ? 0 : (currentHeight - targetHeight) / 2;

		sized.crop(0,cropMargin,targetWidth, targetHeight)
			.quality(imageQuality)
			.write(`./img/thumbnail-${n}.${img.getExtension()}`);		

	});
});
