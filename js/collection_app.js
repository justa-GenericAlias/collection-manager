const defaultMovies = Array.from({ length: 30 }, (_, i) => ({
  id: i + 1,
  title: `Movie ${i + 1}`,
  genre: "N/A",
  year: 2000 + i,
  rating: (i % 10) + 1
}));

function loadMovies() {
  const saved = localStorage.getItem("movies");
  if (saved) {
    return JSON.parse(saved);
  } else {
    localStorage.setItem("movies", JSON.stringify(defaultMovies));
    return defaultMovies;
  }
}

function saveMovies() {
  localStorage.setItem("movies", JSON.stringify(movies));
}

let movies = loadMovies();
let editingId = null;

const listEl = document.getElementById("movie-list");
const form = document.getElementById("movie-form");
const formTitle = document.getElementById("form-title");
const cancelEditBtn = document.getElementById("cancel-edit");

const totalCountEl = document.getElementById("total-count");
const avgRatingEl = document.getElementById("average-rating");

function renderList() {
  listEl.innerHTML = "";

  movies.forEach(movie => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${movie.title}</td>
      <td>${movie.genre}</td>
      <td>${movie.year}</td>
      <td>${movie.rating}</td>
      <td>
        <button onclick="editMovie(${movie.id})">Edit</button>
        <button onclick="deleteMovie(${movie.id})">Delete</button>
      </td>
    `;

    listEl.appendChild(row);
  });
}

function renderStats() {
  totalCountEl.textContent = movies.length;

  const avg =
    movies.reduce((sum, m) => sum + m.rating, 0) / movies.length || 0;

  avgRatingEl.textContent = avg.toFixed(1);
}

function render() {
  renderList();
  renderStats();
}

form.addEventListener("submit", e => {
  e.preventDefault();

  const title = document.getElementById("title").value.trim();
  const genre = document.getElementById("genre").value.trim();
  const year = Number(document.getElementById("year").value);
  const rating = Number(document.getElementById("rating").value);

  if (!title || !genre || year < 1900 || rating < 1 || rating > 10) {
    alert("Please enter valid data.");
    return;
  }

  if (editingId === null) {
    const newMovie = {
      id: Date.now(),
      title,
      genre,
      year,
      rating
    };

    movies.push(newMovie);
  } 
  else {
    const movie = movies.find(m => m.id === editingId);
    movie.title = title;
    movie.genre = genre;
    movie.year = year;
    movie.rating = rating;
    editingId = null;
    cancelEditBtn.hidden = true;
    formTitle.textContent = "Add Movie";
  }

  form.reset();
  saveMovies();
  render();
});

function editMovie(id) {
  const movie = movies.find(m => m.id === id);

  document.getElementById("title").value = movie.title;
  document.getElementById("genre").value = movie.genre;
  document.getElementById("year").value = movie.year;
  document.getElementById("rating").value = movie.rating;

  editingId = id;
  formTitle.textContent = "Edit Movie";
  cancelEditBtn.hidden = false;
}

function deleteMovie(id) {
  if (!confirm("Are you sure you want to delete this movie?")) return;

  movies = movies.filter(m => m.id !== id);
  saveMovies();
  render();
}

cancelEditBtn.addEventListener("click", () => {
  editingId = null;
  form.reset();
  formTitle.textContent = "Add Movie";
  cancelEditBtn.hidden = true;
});

render();