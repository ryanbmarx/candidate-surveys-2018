const inView = require('in-view');


// Let's set our lazyload offset to 500px into the viewport. 
// inView.offset(500);

window.addEventListener('DOMContentLoaded', function(e){

	inView('.category')
	    .on('enter', el => {

	        let raceID =  el.getAttribute('id');
			
	        document.querySelector('.nav-button--active').classList.remove('nav-button--active');
	        document.querySelector(`.nav-button[href="#${raceID}"]`).classList.add('nav-button--active');
	    });

});