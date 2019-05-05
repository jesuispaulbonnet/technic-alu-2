// Include gulp
var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var minify = require('gulp-minify');


// Compile Sass
gulp.task('sass', function() {
    return gulp.src('technic_alu_2/static/sass/technic_alu_2.scss')
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(rename('technic_alu_2.min.css'))
        .pipe(gulp.dest('technic_alu_2/static/css'));
});
// Minify javascript
gulp.task('scripts', function() {
  gulp.src('technic_alu_2/static/js/*')
    .pipe(minify({
      ext: {
          min:'.min.js'
      },
    }))
    .pipe(gulp.dest('technic_alu_2/static/dist/'));
});

//Watch task
gulp.task('watch', ['sass', 'scripts'], function() {
    gulp.watch('technic_alu_2/static/sass/**/*.scss', ['sass']);
    gulp.watch('technic_alu_2/static/js/**/*.js', ['scripts']);
});
