!(function (l) {
	"use strict";
	l(document).on("click", "#sidebarToggle", function (e) {
		e.preventDefault(),
			l("body").toggleClass("sidebar-toggled"),
			l(".sidebar").toggleClass("toggled");
	}),
		l("body.fixed-nav .sidebar").on(
			"mousewheel DOMMouseScroll wheel",
			function (e) {
				let l;
				768 < $window.width() &&
					((l = (l = e.originalEvent).wheelDelta || -l.detail),
					(this.scrollTop += 30 * (l < 0 ? 1 : -1)),
					e.preventDefault());
			}
		);
})(jQuery);

const API_URL = "https://cinemeta-catalogs.strem.io/top/catalog/movie/top.json";
const IMG_PATH = "https://image.tmdb.org/t/p/w220_and_h330_face";
const SEARCH_API =
	"https://api.apipop.net/list?sort=seeds&short=1&cb=&quality=720p,1080p,3d&page=1&ver=100.0.0.0.&os=windows&app_id=T4P_ONL&keywords=";

const main = document.getElementById("porco");
const form = document.getElementById("form");
const search = document.getElementById("search");

// Get initial movies
getMovies(API_URL);

async function getMovies(url) {
	const res = await fetch(url);
	const data = await res.json();

	showMovies(data.metas);
}

function showMovies(movies) {
	main.innerHTML = "";

	movies.forEach((movie) => {
		const { name, poster, imdbRating, runtime, year, genre, imdb_id } = movie;

		const movieEl = document.createElement("div");
		movieEl.classList.add("col-xl-2");
		movieEl.classList.add("col-sm-6");
		movieEl.classList.add("mb-2");
		movieEl.innerHTML = `
                        <div class="video-card">
                           <div class="video-card-image">
                              <a class="play-icon" href="https://www.imdb.com/title/${imdb_id}/" target="_blank"><i class="fas fa-play-circle"></i></a>
                              <a href="#"><img class="img-fluid" src="${poster}" alt="${name}"></a>
                              <span class="movierating movierating-${getClassByRate(
																															imdbRating
																														)}">${imdbRating}</span>
                           </div>
                           <div class="video-card-body">
                              <div class="video-title">
                                 <a href="https://www.imdb.com/title/${imdb_id}/" target="_blank">${name}</a>
                              </div>
                              <div class="video-view">
                                 ${
																																		genre[0]
																																	}<span style="float:right;">${year}</span> 
                              </div>
                           </div>
                        </div>
        `;
		main.appendChild(movieEl);
	});
}

function getClassByRate(vote) {
	if (vote >= 8) {
		return "green";
	} else if (vote >= 5) {
		return "yellow";
	} else {
		return "red";
	}
}

form.addEventListener("submit", (e) => {
	e.preventDefault();

	const searchTerm = search.value;

	if (searchTerm && searchTerm !== "") {
		getMovies(SEARCH_API + searchTerm);

		search.value = "";
	} else {
		window.location.reload();
	}
});