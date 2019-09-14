var vtt = "WEBVTT\n\n1\n00:00.000 --> 00:20.000\n[Music]\n\n1\n00:20.500 --> 00:40.000\ndu du du du DUH DUH! $O(n\\log{n})$",
    parser = new WebVTT.Parser(window, WebVTT.StringDecoder()),
    cues = [],
    regions = [];
parser.oncue = function(cue) {
    cues.push(cue);
    console.log(cue);
};
parser.onregion = function(region) {
    regions.push(region);
}
parser.parse(vtt);
parser.flush();

function update_subtitle(s) {
    var element_list = s.trim().split(' ');
    $('#subtitle').empty();
    for (var [i, v] of element_list.entries()) {
        var tag = `<span contenteditable id="tag-${i}" onclick="pause();" class="subtitle-element">${v}</span>`;
        $('#subtitle').append(tag);
        $(`#subtitle > tag-${i}`).change(() => {
          console.log("Get value " + $(this).value);
        });
    }

    MathJax.typeset()
}

function pause() {
    $('#vid')[0].pause();
    //add a submit changes! button here
}

function binSearch(cues, curtime) {
    var min = 0, mid, max = cues.length - 1;
    while (max != min) {
        if (max - min == 1) {
            if (curtime >= cues[max].startTime)
                return max;
            else
                return min;
        }
        mid = (min + max)/2;
        if (curtime >= cues[mid].startTime)
            min = mid;
        else
            max = mid;
    }
}

function what_time(){
    var curtime = $('#vid')[0].currentTime;
    var cnt = binSearch(cues, curtime);
    if (cnt < cues.length) {
        if (curtime >= cues[cnt].startTime)
            update_subtitle(cues[cnt].text);
        if (curtime >= cues[cnt].endTime)
            $('#subtitle').empty();
    }
}

$(function() {
    $('#vid').on('timeupdate', function() {what_time()});
});
