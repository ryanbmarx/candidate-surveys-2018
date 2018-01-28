const inView = require('in-view');
import 'awesomplete';
import clickTrack from "./click-track.js";

// Let's set our offset to 33% into the viewport. 
inView.offset(window.innerWidth / 3);

window.addEventListener('DOMContentLoaded', function(e){
	// These waypoints power the navbar buttons
	inView('.category')
	    .on('enter', el => {
	        let raceID =  el.getAttribute('id');
	        document.querySelector('.nav-button--active').classList.remove('nav-button--active');
	        document.querySelector(`.nav-button[href="#${raceID}"]`).classList.add('nav-button--active');
	    });

    // ----------------------------
    // AUTOCOMPLETE ---------------
    // ----------------------------

	const 	form = document.querySelector('#candidate-lookup'),
			searchBar = form.querySelector('input'),
			submitButton = form.querySelector('button');

	// This is the autocomplete tool. It needs the `list` attribute
	// to be filled with autocomplete options. We'll do that with a 
	// window variable templated with Jinja on the index page.
	
	const auto = new Awesomplete(searchBar, {
		minChars: 2,
		maxItems: 20,
		autoFirst: true,
		list: window.candidates,
		replace: function(text){
			// This puts the readable name into the search bar
			// this means the awesomplete object. 
			this.input.value = text.label;
		}
	});

	window.addEventListener('awesomplete-selectcomplete', function(e) {
		// When the user makes an autocompleted selection, take the "value"
		// and go to that candidate page
		window.location = `${window.ROOT_URL}/candidates/${e.text.value}.html`;

		// Trigger an omniture link track
		clickTrack('Elex 2018 - surveys - candidate search');
	})
});

