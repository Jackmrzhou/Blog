function jump_to_edit(id){
    window.location.href = "/edit/"+id;
}

function render_post(post){
    $(document).ready(function(){
        if (post.status){
            var f = document.createDocumentFragment();
            var c = document.createElement("center");
            var title = document.createElement("h2");
            title.innerText = post.title;
            var date = document.createElement("div");
            date.className = "post-meta";
            date.innerText = post.date.split(" ").splice(0,4).join(" ");
            var con = document.createElement("div");
            con.className = "post-body";
            if (post.content_type == "PlainText"){
                con.innerText = post.content;
            }
            else{
                var converter = new showdown.Converter({tables: true, 
                                                        strikethrough: true,
                                                        literalMidWordUnderscores : true});
                con.innerHTML = converter.makeHtml(post.content.replace(/\\/g, "\\\\"));
            }
            c.appendChild(title);
            c.appendChild(date);
            f.appendChild(c);
            f.appendChild(con);
            $("#Main").append(f);
            $("#Main").append(render_comment(post.id, converter));
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        }
    })
}

function Get_Post(){
    var p = window.location.pathname;
    $.get("/api" + p, render_post)
}

function render_feed(feed){
    $(document).ready(function(){
        if (feed.status){
            var converter = new showdown.Converter({tables: true, 
                                                    strikethrough: true,
                                                    literalMidWordUnderscores : true});
            for(let p of feed.posts){
                f = create_feed(p, converter);
                $("#Main").append(f);
            }
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        }
        render_attr.continue_get = feed.status && feed.next;
        render_attr.on_render = false;
    })
}

function Get_Feed(){
    var count = 1;
    function Get(){
        $.get("/api/batch", {"o":count}, render_feed);
        count++;
    }
    return Get;
}

var render = null;
var render_attr ={
    continue_get : true,
    first_reach_bottom : false,
    on_render : true,
};

function Main(){
    this.render_attr.continue_get = true;
    this.render_attr.first_reach_bottom = false;
    this.render_attr.on_render = true;
    this.render = Get_Feed();
    this.render();

    $(window).scroll(function(){
        if ($(document).height() - $(window).scrollTop() - $(window).height() < 260){
            if (render_attr.continue_get && !render_attr.on_render){
                render_attr.on_render = true;
                render();
            }
            else if (!render_attr.continue_get && !render_attr.first_reach_bottom){
                render_attr.first_reach_bottom = true;
                var end = document.createElement("center");
                end.innerText = "到底啦！";
                $("#Main").append(end);
            }
        }
    })
}

function render_form(){
    var p = window.location.pathname.split("/").splice(2,1).join();
    $.get("/api/p/" + p, function(post){
        $(document).ready(function(){
            $("#title").val(post.title);
            $("#category").val(post.category);
            $("#is_md").attr("checked", post.content_type === "Markdown");
            $("#content").val(post.content);
        })
    });
}

function create_feed(p, converter){
    var f = document.createElement("div");
    var content = document.createElement("div");
    var c = document.createElement("center");
    var t = document.createElement("h2");
    var title = document.createElement("a");
    t.appendChild(title);
    var date = document.createElement("div");
    date.className = "post-meta";
    date.innerText = p.date.split(" ").splice(0,4).join(" ");
    title.innerText = p.title;
    title.href = "/p/" + p.id;
    f.className = "post-feed";
    f.id = "feed-" + String(p.id);
    content.className = "post-content";
    content.id = "content-" + String(p.id);
    if (p.content_type == "PlainText"){
        content.innerText = p.content;
    }
    else{
        content.innerHTML = converter.makeHtml(p.content.replace(/\\/g, "\\\\"));
    }
    c.appendChild(t);
    c.appendChild(date);
    f.appendChild(c);
    f.appendChild(content);
    f.appendChild(create_mask(p.id));
    f.appendChild(create_btn(p.id));
    return f;
}

function create_mask(id){
    var mask = document.createElement("div");
    mask.className = "feed-mask";
    mask.id = "mask-"+String(id);
    return mask;
}

function create_btn(id){
    var btn = document.createElement("button");
    var cc = document.createElement("center");
    btn.type = "button";
    btn.className = "btn btn-info read-more-pos";
    btn.innerText = "Read More";
    btn.id = "btn-" + String(id);
    cc.id = "btn-center-" + String(id);
    btn.onclick = function(){
        read_more(id);
    }
    cc.appendChild(btn);
    return cc;
}

function read_more(id){
    $("#mask-"+ String(id)).remove();
    $("#content-"+String(id)).css("max-height", "100%");
    var btn = $("#btn-" + String(id));
    btn.text("Fold");
    var btnn = document.getElementById("btn-" + String(id));
    btnn.onclick= function(){
        var content = $("#content-" + String(id));
        content.css("max-height", "300px");
        content.after(create_mask(id));
        $("#btn-center-" + String(id)).remove();
        $("#feed-" + String(id)).append(create_btn(id));
        $('html, body').animate({  
            scrollTop: $("#feed-" + String(id)).offset().top
        });
    };
}

function render_comment(id, converter) {
    $.get("/api/c/" + String(id), function (comments) {
        if (comments.status) {
            var a = document.createElement("div");
            a.className = "comments";
            var info = document.createElement("div");
            info.className = "comment-info";
            var sp = document.createElement("span");
            sp.className = "label label-info comment-info";
            sp.innerText = "All " + comments.comments.length + " Comments:";
            info.appendChild(sp);
            a.appendChild(info);
            for (let c of comments.comments) {
                var f = document.createElement("div");
                f.className = "panel panel-info";
                var name = document.createElement("div");
                name.className = "panel-heading";
                name.innerText = c.name;
                var content = document.createElement("div");
                content.className = "panel-body";
                if (c.content_type == "PlainText") {
                    content.innerText = c.content;
                }
                else {
                    content.innerHTML = converter.makeHtml(c.content.replace(/\\/g, "\\\\"));
                }
                f.appendChild(name);
                f.appendChild(content);
                a.appendChild(f);
            }
            $("#Main").append(a);
        }
        $("#post-comment").css("display", "block");
    })
}