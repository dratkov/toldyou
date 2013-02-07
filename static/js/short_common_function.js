/**
 * Created with PyCharm.
 * User: dim
 * Date: 02.02.13
 * Time: 0:20
 * To change this template use File | Settings | File Templates.
 */
function set_fulfilled(obj){
    var form = $("#form_edit_post");
    if(form.get(0).fulfilled.value == "False"){
        $(obj).children().removeClass('hide');
        form.get(0).fulfilled.value = "True";
        if(form.get(0).not_fulfilled.value == "True"){
            form.get(0).not_fulfilled.value = "False";
            $(form.get(0).not_fulfilled).next().children().addClass('hide');
        }
    } else {
        $(obj).children().addClass('hide');
        form.get(0).fulfilled.value = "False"
    }
}

function set_not_fulfilled(obj){
    var form = $("#form_edit_post");
    if(form.get(0).not_fulfilled.value == "False"){
        $(obj).children().removeClass('hide');
        form.get(0).not_fulfilled.value = "True";
        if(form.get(0).fulfilled.value == "True"){
            form.get(0).fulfilled.value = "False";
            $(form.get(0).fulfilled).next().children().addClass('hide');
        }
    } else {
        $(obj).children().addClass('hide');
        form.get(0).not_fulfilled.value = "False"
    }
}

function addShortPostComment(obj, post_id, url){
    var prev = $(obj).prev();
    if(prev.css('display') == 'none'){
        prev.show();
        $(obj).html('сохранить')
    } else {
        prev.next().html('сохранение...');
        $.post(url, {post_id: post_id, user_post_short_comment: prev.val()},
            function(data) {
                if(data.success) {
                    prev.hide();
                    prev.next().html('написать свой <i class=\'icon-comment icon-white\'></i>');
                    $($(obj).parent().children().get(0)).append(' ').append($('<span>').css('display', 'inline-block').addClass('label label-user-short-comment').html(data.text))
                    obj.value = ''
                } else {
                    prev.next().html('сохранить')
                }
            });
    }
}

function postMore(obj){
    if($(obj).parent().next().hasClass('hide')){
        $(obj).html('<abbr>скрыть</abbr> <i class=\'icon-chevron-up\'></i>')
        $.each($(".post-more-info"),
            function(index, value){
                if(!$(value).parent().next().hasClass('hide')){
                    postMore(value)
                }
            }
        )
    } else {
        $(obj).html('<abbr>подробнее</abbr> <i class=\'icon-chevron-down\'></i>')
    }
    $(obj).parent().next().toggleClass('hide');
    return false
}

function postAgree(obj, post_id, url, agree){
    $.post(url,
        {agree: agree, post_id: post_id},
            function(data){
                if (data.success) {
                    $($(obj).children().get(1)).html( agree ? data.agree_count : data.disagree_count);
                    $(obj).attr('onclick', '').css('cursor', 'default')
                }
            }
    )
}

function postCharsetCount(){
    var form = $("#form-post-id");
    if(!form.get(0))
        return;
    var max_length = 280;
    var danger_length = 280 - 20;
    var warning_length = 280 - 40;
    var len = form.get(0).text.value.length;
    var class_name = '';
    if(len > warning_length){
        if (len < danger_length){
            class_name = 'text-warning'
        } else {
            class_name = 'text-error'
        }
    }
    $("#charset-count").html(max_length - len).removeAttr('class').addClass(class_name);

}
setInterval(function(){ postCharsetCount() }, 300);

function shortCommentsVote(obj, url, post_id, comment_id){
    $.post(url, { short_comment_id: comment_id, post_id: post_id },
        function(data){
            if(data.success)
                $(obj).attr('onclick', '').css('cursor', 'default').children().html(data.short_comment_count);
            var count_arr = [];
            $.each($(obj).parent().children(),
                function(index, value){
                    var count = parseInt($(value).children().html());
                    count_arr.push(count ? count : 0)
                }
            );
            var max_count = 0;
            for(var i = 0; i < count_arr.length; i++){
                if(count_arr[i] > max_count){
                    max_count = count_arr[i]
                }
            }
            $.each($(obj).parent().children(),
                function(index, value){
                    $(value).css('opacity', Number((count_arr[index] * 80 / max_count + 20) / 100).toFixed(2))
                }
             )

        })
}
