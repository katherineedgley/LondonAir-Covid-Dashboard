

// plots the figure with id
// id much match the div id above in the html
var figures = {{figuresJSON | safe}};
var ids = {{ids | safe}};
for(var i in figures) {
    Plotly.plot(ids[i],
        figures[i].data,
        figures[i].layout || {});
}

$("#NO2").click(function () {
  $("#charts").append('<div class="row d-flex"><div class="d-flex" id = "{{ids[0]}}"> </div></div>');
  alert('here')
});

// $('#dropdownMenuButton').on('click', function(){
// 	$('.charts').after('<div> hi </div>')
// 	alert($('#dropdownMenuButton').val($(this).html()));
// });


// $('#dropdownMenuButton').on('click',function() {
// 		$('.charts').after('<div class="row d-flex"><div class="d-flex" id = "{{ids[0]}}"> </div></div>');
// 		$('.charts').after('<div> hi </div>')
//         var species = $('#dropdownMenuButton').val($(this).text())
//         if (species == 'NO2') {
//         	$('.charts').after('<div class="row d-flex"><div class="d-flex" id = "{{ids[0]}}"> </div></div>');
//         }
// });
