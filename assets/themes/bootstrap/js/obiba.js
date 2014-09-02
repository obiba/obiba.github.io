(function ($) {
  'use strict';

  $.popImageModal = function (imageUrl, imageHeader, imageCaption, pager) {
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


    if (!pager) {
      $('#model-footer-pager').hide();
    }

    $('#modal-image-holder').attr('src', imageUrl);
    $('#modal-image-header').text(imageHeader);
    $('#modal-image-caption').text(imageCaption);
  }

}(jQuery));

var ModalImageBrowser = (function () {

  // Instance stores a reference to the Singleton
  var instance;

  function init() {

    var count = 0;
    var index = 0;
    var images = [];

    function show() {
      if (images.length > 0) {
        $.popImageModal(images[index].src, "Image " + (index + 1) + " of " + count, "", true);
        bindKeydownEvents();
      }
    }

    function updateModal() {
      $('#modal-image-holder').attr('src', images[index].src);
      $('#modal-image-header').text("Image " + (index + 1) + " of " + count);
    }

    function next() {
      index = (index + 1) % count;
      updateModal();
    }

    function prev() {
      console.log(index, (count - index - 1));
      index = ((index - 1) < 0 ? count - 1 : index - 1) % count;
      updateModal();
    }


    function unbindKeydownEvents() {
      $(document).unbind('keydown');

    }

    function bindKeydownEvents() {
      $(document).bind('keydown', function(e) {
        switch (e.which || e.keyCode) {
          case 37:
            prev();
            break;
          case 39:
            next();
            break;
        }
      })
    }

    return {

      init: function (currentImg) {
        indexInfo = new RegExp("(\\d+):(\\d+)").exec(currentImg.id);
        images = $(currentImg).parents("ul#image-gallery-container").find("img");
        if (!indexInfo || !images) console.log("Need to have an 'img' element with id in 'size:index' format.");
        count = indexInfo[1];
        index = indexInfo[2] - 1;

        $('#image-modal-container').on('hide.bs.modal', function () {
          unbindKeydownEvents();
        });

        $('#model-footer-pager #modal-pager-prev').click(prev);
        $('#model-footer-pager #modal-pager-next').click(next);
        show();
      }

    };

  };

  return {
    getInstance: function () {
      if (!instance) {
        instance = init();
      }

      return instance;
    }

  };

})();


