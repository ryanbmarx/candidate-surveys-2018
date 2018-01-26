const inView = require('in-view');


// Let's set our offset to 33% into the viewport. 
inView.offset(window.innerWidth / 3);

window.addEventListener('DOMContentLoaded', function(e){

	inView('.category')
	    .on('enter', el => {

	        let raceID =  el.getAttribute('id');
			
	        document.querySelector('.nav-button--active').classList.remove('nav-button--active');
	        document.querySelector(`.nav-button[href="#${raceID}"]`).classList.add('nav-button--active');
	    });

});