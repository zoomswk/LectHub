var vtt,
parser,
cues = [],
regions = [];
var editing = 0;
var cur;

function update_subtitle(s, render) {
    var element_list = s.trim().split(' ');
    $('#subtitle').empty();
    for (var [i, v] of element_list.entries()) {
        var tag = `<div contenteditable id="tag-${i}" class="subtitle-element flex">${v}</div>`;
        $('#subtitle').append(tag);

        $(`#subtitle > #tag-${i}`).bind("blur", (function() {
          const cur_i = i;
          return function() {
            const new_text = $(this).html();

            if (new_text !== v){
              // edit locally
              element_list[cur_i] = new_text;
              s = element_list.join(" ");
              // HEREEEE
              console.log("s = " + s);

              // send a new request

              display(1, true);

            }
          }
        })()).click(() => { edit(i) });
    }
    if (render)
        MathJax.typeset()
}

function edit(index) {
    $('#vid')[0].pause();
    if (editing == 0) {
        //update_subtitle(cues[cur].text, 0);
    }
    //add a submit changes! button here
}

function binSearch(curtime) {
    var min = 0, mid, max = cues.length - 1;
    while (max != min) {
        if (max - min == 1) {
            if (curtime >= cues[max].startTime)
                return max;
            else
                return min;
        }
        mid = Math.round((min + max)/2);
        if (curtime >= cues[mid].startTime)
            min = mid;
        else
            max = mid;
    }
}

function display(render, force = false){
    var curtime = $('#vid')[0].currentTime;
    var cnt = binSearch(curtime);
    if (cnt < cues.length) {
        if (curtime >= cues[cnt].startTime)
            if (cur != cnt || force) {
                update_subtitle(cues[cnt].text, render);
                cur = cnt;
            }
        if (curtime >= cues[cnt].endTime)
            $('#subtitle').empty();
    }
}

$(function() {
    $('#vid').on('timeupdate', function() {display(1)});

    const url = $('#subtitle_url').html();

    $.get( url, function( data ) {
      vtt = data;
      parser = new WebVTT.Parser(window, WebVTT.StringDecoder());
      parser.oncue = function(cue) {
          cues.push(cue);
      };
      parser.onregion = function(region) {
          regions.push(region);
      }
      parser.parse(vtt);
      parser.flush();
    });
});
