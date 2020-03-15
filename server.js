var Twit = require('twit')

var fs = require('fs'),
	path = require('path'),
	Twit = require('twit'),
	config = require(path.join(__dirname, 'config.js'));

var T = new Twit(config);


function random_from_array(images){
	return images[Math.floor(Math.random() * images.length)];
}

function upload_random_image(images){
	console.log('Opening an image...');
	var image_path = path.join(__dirname, '/images/Perfume Pics/bot-pics/' + random_from_array(images)),
		b64content = fs.readFileSync(image_path, { encoding: 'base64' });
	console.log('Uploading an image...');
	T.post('media/upload', { media_data: b64content }, function (err, data, response) {
		if (err){
			console.log('ERROR:');
			console.log(err);
		}
		else{
			console.log('Image uploaded!');
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
	if (err){
		console.log(err);
	}
	else{
		var images = [];
		 files.forEach(function(f) {
			images.push(f);
		});
		setInterval(function(){
			 upload_random_image(images);
//		}, 10000); //10 secs
//		}, 300000); //5 mins
		}, 1200000); //20 mins
	 }
});
