 $(document).ready(function() {
      $('.like-button').click(function() {
        var itemType = $(this).data('item-type');  // Тип элемента: 'question' или 'answer'
        var itemId = $(this).data('item-id');  // ID вопроса или ответа
        var csrftoken = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
          type: 'POST',
          url: '/add-like/',
          data: {
            type: itemType,
            item_id: itemId,
            csrfmiddlewaretoken: csrftoken
          },
          success: function(response) {
            // Обновление интерфейса, например, изменение количества лайков
            var likesCount = parseInt($('.likes_values').text());
            $('.likes_values').text(likesCount + 1);
            $('.like-button').hide();
          },
          error: function(response) {
            // Обработка ошибок
            console.log(response.responseJSON.error);
          }
        });
      });
    });