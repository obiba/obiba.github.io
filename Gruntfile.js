'use strict';

module.exports = function (grunt) {

  grunt.initConfig({
    less: {
      development: {
        options: {
          compress: true,
          yuicompress: true,
          optimization: 2
        },
        files: {
          // target.css file: source.less file
          "assets/themes/bootstrap/css/bootstrap-col-height.css": "assets/themes/bootstrap/css/bootstrap-col-height.less",
          "assets/themes/bootstrap/css/obiba.css": "assets/themes/bootstrap/less/obiba.less"
        }
      }
    },
    uglify: {
      options: {
        // Preserve banner
        preserveComments: "some"
      },
      dist: {
        files: {
          "assets/themes/bootstrap/js/obiba.min.js": "assets/themes/bootstrap/js/obiba.js"
        }
      }
    },
    watch: {
      styles: {
        // Which files to watch (all .less files recursively in the less directory)
        files: ['assets/themes/bootstrap/less/**/*.less', 'assets/themes/bootstrap/js/obiba.js'],
        tasks: ['less', 'uglify'],
        options: {
          nospawn: true
        }
      }
    }

  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks("grunt-contrib-uglify");

  grunt.registerTask('default', ['watch']);
};