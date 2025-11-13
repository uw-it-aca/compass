/*jslint browser: true */
/*global jQuery, DataTable */
var Compass = {};

Compass.AdminSupport = (function($){
  "use strict";
  function get_csrf_token() {
    var csrf = null;
    var cookie_name = 'csrftoken';
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, cookie_name.length + 1) == (cookie_name + '=')) {
          csrf = decodeURIComponent(cookie.substring(cookie_name.length + 1));
          break;
        }
      }
    }
    return csrf;
  }
  function reload_retention_import(import_id) {
    var url = '/api/internal/support/retention_admin/manage/' + import_id + '/';
    var csrf = get_csrf_token();
    var foo = 0;

    $.ajax({url: url,
      method: 'PUT',
      headers : {'X-CSRFToken': csrf}
    }).done(function (result) {
      window.location.reload();
    });
  }
  function delete_retention_import(import_id) {
    var url = '/api/internal/support/retention_admin/manage/' + import_id + '/';
    var csrf = get_csrf_token();
    $.ajax({url: url,
      method: 'DELETE',
      headers : {'X-CSRFToken': csrf}
    }).done(function (result) {
      window.location.reload();
    });
  }
  function reload_alerts(import_id) {
    var url = '/api/internal/support/retention_admin/reload_alerts/';
    var csrf = get_csrf_token();
    $.ajax({url: url,
      method: 'PUT',
      headers : {'X-CSRFToken': csrf}
    }).done(function (result) {
      window.location.reload();
    });
  }
  return {
    get_csrf_token: get_csrf_token,
    reload_retention_import: reload_retention_import,
    delete_retention_import: delete_retention_import,
    reload_alerts: reload_alerts
  };
}(jQuery));

(function ($) {
    "use strict";
    $(document).ready(function () {
        $('.reload-btn').on('click', function(){
          var import_id = $(this).val();
          Compass.AdminSupport.reload_retention_import(import_id);
        });
        $('.delete-btn').on('click', function(){
          var import_id = $(this).val();
          Compass.AdminSupport.delete_retention_import(import_id);
        });
        $('#reload_alerts_btn').on('click', function(){
          Compass.AdminSupport.reload_alerts();
        });
        $('#canvas_analytics_table').DataTable({
          autoWidth: true,
          pageLength: 10,
          searching: false,
          lengthChange: false,
          columnDefs: [
            {
              targets: '_all',
              orderable: false
            }
          ],
          order: [[0, 'desc']],
        });
    });
}(jQuery));
