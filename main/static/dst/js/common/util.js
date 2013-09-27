// Generated by CoffeeScript 1.6.3
(function() {
  window.LOG = function() {
    return typeof console !== "undefined" && console !== null ? typeof console.log === "function" ? console.log.apply(console, arguments) : void 0 : void 0;
  };

  window.init_loading_button = function() {
    return $('body').on('click', '.btn-loading', function() {
      return $(this).button('loading');
    });
  };

  window.init_time = function() {
    var recalculate;
    if (($('time')).length > 0) {
      recalculate = function() {
        return ($('time[datetime]')).each(function() {
          var date, diff;
          date = moment.utc(($(this)).attr('datetime'));
          diff = moment().diff(date, 'days');
          if (diff > 25) {
            ($(this)).text(date.local().format('YYYY-DD-MM'));
          } else {
            ($(this)).text(date.fromNow());
          }
          return ($(this)).attr('title', date.local().format('dddd, MMMM Do YYYY, HH:mm:ss Z'));
        });
      };
      recalculate();
      return setInterval(function() {
        return recalculate();
      }, 1000 * 60);
    }
  };

}).call(this);
