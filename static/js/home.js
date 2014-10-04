// Connect "Browse" buttons and the actual file input elements.
$('#student-data-button').click(function(e) {
  $('#student-data').click();
  e.preventDefault();
});

$('#class-data-button').click(function(e) {
  $('#class-data').click();
  e.preventDefault();
});

// Update span when files selected.
$('#student-data').change(function() {
  // Get the file name alone, not the entire path.
  var fileName = $(this).val().replace(/.*(\/|\\)/, '');
  $('#student-data-filename').text(fileName);
});

$('#class-data').change(function() {
  var fileName = $(this).val().replace(/.*(\/|\\)/, '');
  $('#class-data-filename').text(fileName);
});
