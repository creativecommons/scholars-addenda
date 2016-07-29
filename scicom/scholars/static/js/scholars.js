YAHOO.namespace("scholars");

// validate the form prior to submission
function validate() {

  // clear all previous errors
  $("input").removeClass("error");
  var errors = false;

  // check all except author, which is special cased
  $("input[@name!='author']").each(function(){

     if(! $(this).val()) {

        errors = true;
        $(this).addClass("error");

     } 
  });

  // check author
  var seen_author = false;
  $("input[@name='author']").each(function(){
     if ($(this).val()) seen_author = true;
  });

  if (!seen_author) {
     $("//input[@name='author']:first").addClass("error");
     errors = true;
  }

  // submit if no errors
  return !(errors);

} // validate

// initialization for the client-side app
YAHOO.scholars.init = function() {

   // HTML snippet for new author input boxes
   var AUTHOR_INPUT = '<label>&nbsp;</label><input class="additional" name="author" /><br/>';


   // add author input box functionality
   $("#addAuthor").click( function() {
       $(AUTHOR_INPUT).hide().appendTo("#author_container").slideDown();

       return false;
       } );

   // connect the validation handler to the button
   $("#generate").click(validate);

} // init

YAHOO.util.Event.onDOMReady(YAHOO.scholars.init); 