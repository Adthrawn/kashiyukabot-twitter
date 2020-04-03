var Twit = require('twit')

var fs = require('fs'),
	path = require('path'),
	Twit = require('twit'),
	config = require(path.join(__dirname, 'config.js'));

var T = new Twit(config);

//get all the images at load
//var images = [];
//files.forEach(function(f) {
//	images.push(f);
//});
var image_count = 0;

function random_from_array(images){
	return images[Math.floor(Math.random() * images.length)];
}

//go to the next file in the array
function next_file(images){
	console.log(image_count);
	return images[image_count];
}

function upload_random_image(images){
	console.log('Opening an image...');
	//if the counter reaches the end of the array, start over
	//also get a new file list
	if (image_count > images.length)
	{
		files.forEach(function(f) {
			images.push(f);
		});
		image_count=0;
	}
	
	//get the next file
	var image_path = path.join(__dirname, '/images/Perfume Pics/bot-pics/' + next_file(images)),
		b64content = fs.readFileSync(image_path, { encoding: 'base64' });
	
	//iterate the counter
	image_count++;
	console.log('Uploading an image...');
	
	//upload the image
	T.post('media/upload', { media_data: b64content }, function (err, data, response) {
		if (err){
			console.log('ERROR:');
			console.log(image_path);
			console.log(err);
		}
		else{
			console.log('Image uploaded!');
			console.log(image_path);
			console.log('Now tweeting it...');
			T.post('statuses/update', {
				status: '#prfm #perfume_um #kashiyuka #ksyk #かしゆか',
				media_ids: new Array(data.media_id_string)
			},
			function(err, data, response) {
				if (err){
					console.log('ERROR:');
					console.log(err);
				}
				else{
					console.log('Posted an image!');
				}
			}
			);
		}
	});
}

fs.readdir(__dirname + '/images/Perfume Pics/bot-pics', function(err, files) {
	var images = [];
	files.forEach(function(f) {
		images.push(f);
	});
	if (err){
		console.log(err);
	}
	//every 20 mins, the below script will fire
	else{
		setInterval(function()
		{
			 upload_random_image(images);
		}, 
		//60000); //1min
		//300000); //5 mins
		600000); //10 mins
		//1200000); //20 mins
	 }
});
