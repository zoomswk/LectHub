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
        var tag = `<div contenteditable id="tag-${i}" class="subtitle-element d-inline-flex">${v}</div>`;
        $('#subtitle').append(tag);

        $(`#subtitle > #tag-${i}`).bind("blur", (function() {
          const cur_i = i;
          return function() {
            const new_text = $(this).html();

            if (new_text !== v){
              // edit locally
              element_list[cur_i] = new_text;
              s = element_list.join(" ");
              cues[cur].text = s;
              console.log("s = " + s);

              // send a new request
              $.post("update/", {block_id: cur_id, new_dialog: s});

              display(1, true);

            }
          }
        })()).click( (function() {
          is_latex = /^.*\$.*\$.*$/.test(v);
          return function () {
            edit(i, is_latex);
          }
        })());
    }
    if (render)
        MathJax.typeset()
}

function edit(index, is_latex) {
    $('#vid')[0].pause();
    if (is_latex) {
        display(false, true);
    }
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
                cur_id = cues[cnt].id;
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
