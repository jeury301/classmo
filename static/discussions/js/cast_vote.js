function cast_vote(id, val, type) {
    var scoreSpanId = type + "-score-" + id;
    var oldScore = document.getElementById(scoreSpanId).innerHTML

    $.ajax({
        url: "/discussions/votes/cast_vote/",
        type: "POST",
        data: {
            'id': id,
            'type': type,
            'val': val
        },
        dataType: 'json',
        success: function (data) {
            var upvoteIconId = type + "-upvote-" + id
            var novoteIconId = type + "-novote-" + id
            var downvoteIconId = type + "-downvote-" + id

            /* Highlight the upvote/downvote/no-vote icon as appropriate */
            if (val == 1) {
                document.getElementById(upvoteIconId).classList.add('highlighted');
            } else {
                document.getElementById(upvoteIconId).classList.remove('highlighted');
            }

            if (val == 0) {
                document.getElementById(novoteIconId).classList.add('highlighted');
            } else {
                document.getElementById(novoteIconId).classList.remove('highlighted');
            }

            if (val == -1) {
                document.getElementById(downvoteIconId).classList.add('highlighted');
            } else {
                document.getElementById(downvoteIconId).classList.remove('highlighted');
            }

            /* Update the score */
            document.getElementById(scoreSpanId).classList.add('highlighted');
            document.getElementById(scoreSpanId).innerHTML = data.new_score;

        },
        error: function(data) {
            console.log("Ajax failed");
            console.log(data);
        }
    });
}