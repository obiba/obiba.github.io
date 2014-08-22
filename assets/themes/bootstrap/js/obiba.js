(function ($) {
  'use strict';

  $.popImageModal = function (imageUrl) {
    $('#image-modal-container').modal({
      backdrop: true,
      keyboard: true
    });

    $('#image-modal-container #image-modal')
    .css({
      'width': function () {
        return ($(document).width() * .6) + 'px';
      }
    });

    $('#modal-image-holder').attr('src', imageUrl);
  }

}(jQuery));



