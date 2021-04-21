// bind some els to vars 

t = document.querySelector("#new-post-text");
btn = document.querySelector("#new-post-btn");
content_top = document.querySelector("#top");
like = document.querySelectorAll(".liked");
edit = document.querySelectorAll(".edit");
text_area = document.querySelectorAll(".textarea");

// handle error where el isnt on page
try {
    btn.addEventListener("click", () => {
        text = t.value;

        if (text.length != 0) {
            form = new FormData();
            form.append("post", text.trim());
            fetch("/newpost", {
                method: "POST",
                body: form,
            })
                .then((res) => res.json())
                .then((res) => {
                    if (res.status == 201) {
                        add_html(
                            res.post_id,
                            res.username,
                            text.trim(),
                            res.timestamp,
                            `/u/${res.username}`
                        );
                        t.value = "";
                    }
                });
        }
    });
} catch (e) {
    console.log(e)
}

// helper function to make html els
function make_div(className) {
    div = document.createElement("div");
    div.setAttribute("class", className);
    return div;
}


// loop over our els and attach events to them to enable
// likes and edits
like.forEach((element) => {
    handle_like(element);
});

edit.forEach((element) => {
    element.addEventListener("click", () => {
        handle_edit(element);
    });
});

text_area.forEach((element) => {
    element.addEventListener("keyup", (e) => {
        if (e.keyCode == 13 && e.shiftKey) return;
        if (e.keyCode === 13) handle_edit(element);
    });
});

// actually do the work of the edit
function edit_post(id, post) {
    form = new FormData();
    form.append("id", id);
    form.append("post", post.trim());

    fetch("/edit_post/", {
        method: "POST",
        body: form,
    }).then((res) => {
        document.querySelector(`#post-content-${id}`).textContent = post;
        document.querySelector(`#post-content-${id}`).style.display = "block";
        document.querySelector(`#post-edit-${id}`).style.display = "none";
        document.querySelector(`#post-edit-${id}`).value = post.trim();
    });
}

// handle Edit state when a user edits a post we make that change
function handle_edit(element) {
    id = element.getAttribute("data-id");
    edit_btn = document.querySelector(`#edit-btn-${id}`);
    if (edit_btn.textContent == "Edit") {
        document.querySelector(`#post-content-${id}`).style.display = "none";
        document.querySelector(`#post-edit-${id}`).style.display = "block";
        edit_btn.textContent = "Save";
        edit_btn.setAttribute("class", "text-success edit");
    } else if (edit_btn.textContent == "Save") {
        edit_post(id, document.querySelector(`#post-edit-${id}`).value);

        edit_btn.textContent = "Edit";
        edit_btn.setAttribute("class", "text-primary edit");
    }
}

// when user likes or dislikes a post make that change
function handle_like(element) {
    element.addEventListener("click", () => {
        id = element.getAttribute("data-id");
        is_liked = element.getAttribute("data-is_liked");
        icon = document.querySelector(`#post-like-${id}`);
        count = document.querySelector(`#post-count-${id}`);

        form = new FormData();
        form.append("id", id);
        form.append("is_liked", is_liked);
        fetch("/like/", {
            method: "POST",
            body: form,
        })
            .then((res) => res.json())
            .then((res) => {
                if (res.status == 201) {
                    if (res.is_liked === "yes") {
                        icon.src = "/static/network/heart.png";
                        element.setAttribute("data-is_liked", "yes");
                    } else {
                        icon.src =
                            "/static/network/notliked.png";
                        element.setAttribute("data-is_liked", "no");
                    }
                    count.textContent = res.like_count + " likes!";
                }
            })
            .catch(function (res) {
                // not the best way to handle this but it works
                alert("You must Register or Login to do that!");
            });
    });
}

// add the post to the page
// this can be refactored at some point
function add_html(id, username, post, time, link) {
    card_div = make_div("card my-2");
    card_body = make_div("card-body my-card");
    username_timestamp = make_div("d-flex mb-2");
    spacer = make_div("d-flex justify-content-start");
    profile_link = document.createElement("a");
    profile_link.setAttribute("href", link);
    username_text = document.createElement("span");
    username_text.setAttribute("class", "text-secondary");
    username_text.textContent = username;
    timestamp = make_div("w-100 d-flex justify-content-end");
    timestamp_content = document.createElement("span");
    timestamp_content.setAttribute("class", "mx-2 text-secondary");
    timestamp_content.textContent = time;
    edit_content = document.createElement("span");
    edit_content.setAttribute("class", "text-primary edit");
    edit_content.textContent = "Edit";
    edit_content.setAttribute("data-id", id);
    edit_content.setAttribute("id", `edit-btn-${id}`);
    edit_content.addEventListener("click", () => {
        handle_edit(edit_content);
    });

    post_content = document.createElement("span");
    post_content.setAttribute("class", "post");
    post_content.setAttribute("id", `post-content-${id}`);
    post_content.textContent = post;

    textarea = document.createElement("textarea");
    textarea.setAttribute("class", "form-control textarea");
    textarea.setAttribute("id", `post-edit-${id}`);
    textarea.setAttribute("data-id", id);
    textarea.setAttribute("style", "display:none;");
    textarea.textContent = post;
    textarea.addEventListener("keyup", (e) => {
        if (e.keyCode == 13 && e.shiftKey) return;
        if (e.keyCode === 13) handle_edit(textarea);
    });

    like_content = make_div("like mt-3");
    img = document.createElement("img");
    img.setAttribute("class", "liked");
    img.setAttribute("data-id", id);
    img.setAttribute("id", `post-like-${id}`);
    img.setAttribute("data-is_liked", "no");
    img.setAttribute(
        "src",
        "/static/network/notliked.png"
    );
    handle_like(img);
    like_number = document.createElement("span");
    like_number.setAttribute("id", `post-count-${id}`);
    like_number.textContent = "0 likes!";

    like_content.appendChild(img);
    like_content.appendChild(like_number);

    timestamp.appendChild(timestamp_content);
    timestamp.appendChild(edit_content);
    profile_link.appendChild(username_text);
    spacer.appendChild(profile_link);
    username_timestamp.appendChild(spacer);
    username_timestamp.appendChild(timestamp);
    card_body.appendChild(username_timestamp);
    card_body.appendChild(post_content);
    card_body.appendChild(textarea);
    card_body.appendChild(like_content);
    card_div.appendChild(card_body);
    content_top.appendChild(card_div);
}

// follow a user
follow_btn = document.querySelector("#follow-btn");
try {
    follow_btn.addEventListener("click", (e) => {
        user = follow_btn.getAttribute("data-user");
        action = follow_btn.textContent.trim();
        form = new FormData();
        form.append("user", user);
        form.append("action", action);
        fetch("/follow/", {
            method: "POST",
            body: form,
        })
            .then((res) => res.json())
            .then((res) => {
                if (res.status == 201) {
                    follow_btn.textContent = res.action;
                    document.querySelector(
                        "#follower"
                    ).textContent = `Followers ${res.follower_count}`;
                }
            });
    });
} catch (e) {
    console.log(e)
}