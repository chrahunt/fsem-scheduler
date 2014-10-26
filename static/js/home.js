// Connect "Browse" buttons and the actual file input elements.
$('#student-data-button').click(function(e) {
  $('#student-data').click();
  e.preventDefault();
});

$('#course-data-button').click(function(e) {
  $('#course-data').click();
  e.preventDefault();
});

/*
 * This function takes an input identifier corresponding to a file
 * input and a label corresponding to the element meant to display
 * the selected file and updates the latter with the value of the
 * former, or "No file selected." if no file has been selected.
 */
function updateSelectedFilePath(input, label) {
  var path = $(input).val();
  if (path === "") {
    $(label).text("No file selected.");
  } else {
    var fileName = path.replace(/.*(\/|\\)/, '');
    $(label).text(fileName);
  }
}

// Update span when files selected. Remember these are only triggered
// when the selected file changes.
$('#student-data').change(function() {
  updateSelectedFilePath(this, '#student-data-filename');
});

$('#course-data').change(function() {
  updateSelectedFilePath(this, '#course-data-filename');
});

// Update spans initially, in case we are coming here as a result of a
// reload or back/forward browser navigation.
updateSelectedFilePath('#student-data', '#student-data-filename');
updateSelectedFilePath('#course-data', '#course-data-filename');

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
fileDragAndDrop('#cd-file-handler-box', '#course-data');
