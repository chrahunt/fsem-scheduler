// Connect "Browse" buttons and the actual file input elements.
$('#student-data-button').click(function(e) {
  $('#student-data').click();
  e.preventDefault();
});

$('#course-data-button').click(function(e) {
  $('#course-data').click();
  e.preventDefault();
});

// Update span when files selected.
$('#student-data').change(function() {
  // Get the file name alone, not the entire path.
  var fileName = $(this).val().replace(/.*(\/|\\)/, '');
  $('#student-data-filename').text(fileName);
});

$('#course-data').change(function() {
  var fileName = $(this).val().replace(/.*(\/|\\)/, '');
  $('#course-data-filename').text(fileName);
});

// Makes the element identified by targetElt able to handle files dragged
// and dropped onto it, setting them as the value of the file selected by
// fileElt.
function fileDragAndDrop(targetElt, fileElt) {
  target = $(targetElt);
  target.on('dragenter', function(e) {
    e.stopPropagation();
    e.preventDefault();
  });

  target.on('dragover', function(e) {
    e.stopPropagation();
    e.preventDefault();
  });

  target.on('drop', function(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer = e.originalEvent.dataTransfer;

    var dt = e.dataTransfer;
    var files = dt.files;
    $(fileElt).get(0).files = files;
  });
}

// Make the boxes around the file inputs respond to files dragged and
// dropped into them.
fileDragAndDrop('#sd-file-handler-box', '#student-data');
fileDragAndDrop('#cd-file-handler-box', '#class-data');
