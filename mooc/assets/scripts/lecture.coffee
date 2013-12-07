$ ->
    $(".lecture-btns").click ->
        _name = $(this).attr("id").replace("btn", "lecture")
        $(".lecture-bar").addClass("lecture-hidden")
        $("#" + _name).removeClass("lecture-hidden")
        $(".lecture-btns").removeClass("current")
        $(this).addClass("current")
        return ;

    window.check_answer = (lecture_id, quiz_id, answer_id, answer) ->
        $.ajax {
                url: '/lecture/' + lecture_id + '/check',
                dataType: 'json',
                data: {'quiz_id': quiz_id, 'answer_id': answer_id},
                type: 'POST',
                success: (res) ->
                    if (res.success)
                        $("#quiz-title-" + quiz_id).children('span').html '回答正确！（' + answer + '）' 
                        setTimeout ->
                                $("#quiz-option-" + quiz_id).slideUp()
                                return ;
                            , 1000
                    else
                        $("#quiz-title-" + quiz_id).children('span').html '回答错误，请重新回答'
                    return ;
            }
        return ;
    return ;