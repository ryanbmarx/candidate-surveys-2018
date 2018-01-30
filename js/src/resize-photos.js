'use strict'

/*

A simple node script, using Jimp, which resizes images in one dir and writes them to another dir

"resize": "node js/src/resize-photos.js 1000 30 ./img/src ./img"

*/

const 	fs = require('fs'),
		Jimp = require('jimp'),
		path = require('path'),
		imageDimension = parseInt(process.argv[2]),
		imageQuality = parseInt(process.argv[3]),
		imageSrc = process.argv[4],
		imageDest = process.argv[5];


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

fs.readdir(`.${path.sep}${imageSrc}${path.sep}`, function(err, files){
	if (err) throw err;
	console.log('### PROCESSING IMAGES');
	console.log('### (THIS MIGHT TAKE A MINUTE)');

	const 	imageList = generateImageList(files),
			imageSourceBase = `${imageSrc}${path.sep}`,
			imageDestBase = `${imageDest}${path.sep}`;

	imageList.forEach(function(imageName, i, a){
		console.log(`##### ${imageName}`);
		
		Jimp.read(`${imageSrc}${path.sep}${imageName}`, function(err, img){
			
			const sized = img.clone();

			sized.resize(imageDimension, Jimp.AUTO)
				.quality(imageQuality)
				.write(`${imageDest}${path.sep}${imageName.toLowerCase()}`);
		});
		
	});
});
