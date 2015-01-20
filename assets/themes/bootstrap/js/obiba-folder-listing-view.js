/**
 * Simple JS used to set bootstrap style on folder table views used in external obiba sites
 */
$(document).ready(function () {
  $("table").addClass("table");
  $("td").removeAttr("align");
  $("tr:eq(1)").remove();
});
