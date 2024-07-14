function submitForm() {
  var formData = $('#bookRecommendationForm').serialize();
  $.ajax({
    type: 'POST',
    url: '{% url "book_recommendation" %}',
    data: formData,
    success: function(response) {
      if (response.success) {
        displayRecommendedBooks(response.data, response.totalBooksFound);
      } else {
        displayErrorMessage(response.message);
      }
    },
    error: function(error) {
      console.log('Error:', error);
    }
  });
}

function displayRecommendedBooks(recommendedBooks, totalBooksFound) {
  var resultsContainer = $('#recommendationResults');
  resultsContainer.empty();

  if (recommendedBooks.length > 0) {
    resultsContainer.prepend('<div class="col-md-12"><p class="mb-4"><strong>Note: The summarize feature is heavily regulated, you may or may not get the correct summary, do your research.</strong></p></div>');
    resultsContainer.prepend('<div class="col-md-12"><p class="mb-4"><strong>Number of books found: ' + totalBooksFound + '</strong></p></div>');
    resultsContainer.prepend('<div class="col-md-12"><p class="mb-4"><strong>Top Ten Matching Books</strong></p></div>');

    recommendedBooks.forEach(function(book, i) {
      var card = `
        <div class="col-md-6 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">${book.title}</h5>
              <p class="card-text">Author: ${book.author}</p>
              <p class="card-text">Publish Date: ${book.publishDate}</p>
              <p class="card-text">Description: ${book.description}</p>
              <a href="${book.link}" target="_blank"><strong>View Book</strong></a>
              <button class="btn btn-secondary mt-2" onclick="summarizeBook(${i})" style="margin-left: 150px; font-weight:bold; color:black;">Summarize</button>
              <p class="card-text mt-2" id="summary-${i}"></p>
            </div>
          </div>
        </div>`;
      resultsContainer.append(card);
    });

    var scrollHeightPercentage = 0.2;
    var scrollPosition = $(document).height() * scrollHeightPercentage;
    $('html, body').animate({ scrollTop: scrollPosition }, 'slow');
  } else {
    resultsContainer.append('<div class="col-md-12"><p class="mb-4">No books found based on the given criteria.</p></div>');
  }
}


function summarizeBook(index) {
  var bookCard = $('#recommendationResults .card').eq(index);
  var bookData = {
    title: bookCard.find('.card-title').text(),
    author: bookCard.find('.card-text:contains("Author:")').text().replace('Author: ', ''),
    publishDate: bookCard.find('.card-text:contains("Publish Date:")').text().replace('Publish Date: ', ''),
    description: bookCard.find('.card-text:contains("Description:")').text().replace('Description: ', '')
  };

  $.ajax({
    type: 'POST',
    url: '{% url "summarize_book" %}',
    contentType: 'application/json',
    data: JSON.stringify(bookData),
    success: function(response) {
      if (response.success) {
        $('#summary-' + index).html('<div style="text-align: center;color:#e4ebe5;"><strong>====================================<br>Summary:</strong></div><div style="text-align: center;">' + response.summary + '</div>');
      } else {
        $('#summary-' + index).text('Failed to generate summary.');
      }
    },
    error: function(error) {
      console.log('Error:', error);
      $('#summary-' + index).text('Error while generating summary.');
    }
  });
}

function displayErrorMessage(message) {
  var resultsContainer = $('#recommendationResults');
  resultsContainer.html('<div class="col-md-12"><p class="alert alert-danger">' + message + '</p></div>');
}

const slides = document.querySelectorAll('.background-slideshow img');
let currentSlide = 0;

function showNextSlide() {
  slides[currentSlide].classList.remove('active');
  currentSlide = (currentSlide + 1) % slides.length;
  slides[currentSlide].classList.add('active');
}

setInterval(showNextSlide, 3000);


  document.getElementById('menu').addEventListener('change', function() {
      const urlMap = {
          'menu_f': '/menu_f/',
          'about': '/about_ecopboe/',
      };

      const selectedValue = this.value;
      if (urlMap[selectedValue]) {
          window.location.href = urlMap[selectedValue];
      }
  });
