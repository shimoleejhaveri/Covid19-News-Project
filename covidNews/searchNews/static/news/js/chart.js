
var endpoint = 'newsBySentiment'    //{% url "new-sentiment" %}
$.ajax({
  method:'GET',
  url:endpoint,
  success: function(data){
    console.log(data)
  },
  error:function(error_data){
    console.log(error_data)
  }
})
