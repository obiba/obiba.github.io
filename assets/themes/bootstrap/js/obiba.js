(function ($) {
  'use strict';

  $.popImageModal = function (imageUrl, imageHeader, imageCaption) {
    $('#image-modal-container').modal({
      backdrop: true,
      keyboard: true
    });

    $('#image-modal-container #image-modal')
    .css({
      'width': function () {
        return ($(document).width() * .5) + 'px';
      }
    });

    $('#modal-image-holder').attr('src', imageUrl);
    $('#modal-image-header').text(imageHeader);
    $('#modal-image-caption').text(imageCaption);
  }

}(jQuery));



