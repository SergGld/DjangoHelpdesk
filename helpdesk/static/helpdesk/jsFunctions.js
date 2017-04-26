/**
 * Created by Серж on 25.04.2017.
 */
   function MyFunction(category) {
    $("#carousel-example-generic").carousel("next");
    $('.cat').html(category)
    $("#id_category").val(category);
}
