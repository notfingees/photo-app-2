const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};
/*
const profile2Html = profile => {
    return `
    <img src="${profile.image_url}" alt="profile pic for ${ profile.username}"
    class="profilephoto" />
    <p>${profile.first_name} ${profile.last_name}</p>
    `;
};
*/

function getProfileHTML(profile){
    return `
    <img src="${profile.image_url}" alt="profile pic for ${ profile.username}"
    class="profilephoto" style="border-radius:50%;width:6vw;height:6vw;"/>
    <p style="display:inline-block;">${profile.first_name} ${profile.last_name}</p>
    `;
}




const displayProfile = () => {
    console.log("in displayProfile");
    fetch('/api/profile')
        .then(response => response.json())
        .then(profiles => {
            const html = getProfileHTML(profiles)//profiles.map(profile2Html);
            document.querySelector('.profile').innerHTML = html;
        })
};


const suggestion2HTML = suggestion => {
    return `
    <div id="suggestion">
    <img src="${suggestion.thumb_url}" class="suggested_pfp"/>
    <div id="suggestion_name_div">
    <p id="suggestion_name">${suggestion.username}</p>
    <p id="suggestio_for_youn">suggested for you</p>
    </div>'
    <button onclick="followUser(${suggestion.id})" id="follow" aria-checked="false" aria-label="Following">follow</button>
</div>
    `;

    /* 
        how to get following / unfollowing 
    */
};

const displaySuggested = () => {

    fetch('/api/suggestions')
        .then(response => response.json())
        .then(suggestions => {
            const html = suggestions.map(suggestion2HTML).join('\n') //profiles.map(profile2Html);
            document.querySelector('.recommendations').innerHTML = html;
        })
};




const postModal2HTML = post => {

    var postModalHTML =  `
    <div style="display:flex; position:relative;">
    <div>
    <img style="width: 30vw; height: auto;" src="${post.image_url}"/>
    </div>
    <div style="overflow: scroll; display: inline-block; overflow: scroll;">
    `
    for (let i = 0; i < post.comments.length; i++) {
        postModalHTML += `<span><b>${post.comments[i].user.username} </b>${post.comments[i].text}</span><br>`
      }

    postModalHTML += `
        </div>
        </div>
    `;

    return postModalHTML
};



const post2HTML = post => {
    var postHTML =  `
    <div id="card">
    <div id="card_top">
        <p id="card_top_username">gibsonjack</p>
        <i class="fas fa-ellipsis-h"></i>
    
    </div>
    <img src="${post.image_url}" class="card_photo"/>
    
    <div id="card_icons">`
        
    if (post.current_user_like_id){
        postHTML += `<i aria-checked="true" aria-label="Liked" class="fas fa-heart" style="color:red;" onclick="unlikePost(${post.id}, ${post.current_user_like_id})"></i>`
    }
    else{
        postHTML += `<i aria-checked="false" aria-label="Liked" onclick="likePost(${post.id})" class="far fa-heart"></i>`
    }
    postHTML +=
      `  <i class="far fa-comment"></i><i class="far fa-paper-plane"></i>`
    
    if (post.current_user_bookmark_id){
       postHTML += ` <i aria-checked="true" aria-label="Bookmarked" id="save" class="far fa-bookmark" onclick="unbookmarkPost(${post.id}, ${post.current_user_bookmark_id})"></i>`
    }
    else{
        postHTML += ` <i aria-checked="false" aria-label="Bookmarked" id="save" class="fas fa-bookmark" onclick="bookmarkPost(${post.id})"></i>`
    }
    
   postHTML +=` </div>
    
    <p><b>${post.likes.length} likes</b></p>
    
    <p id="caption"><span id="caption_username"><b>${post.user.username}</b></span>${post.caption}</span></p>
    `
    if (post.comments.length == 0){
        // do nothing
    }
    else if (post.comments.length > 1){
        postHTML += ` <p id="comment"><span id="comment_username"><b>${post.comments[0].user.username}</b></span> ${post.comments[0].text}</p>`
        postHTML += `<button onclick="showModal(${post.id}, ${this.id})">View all ${post.comments.length} comments</button>`
    }
    else{
        postHTML += ` <p id="comment"><span id="comment_username"><b>${post.comments[0].user.username}</b></span> ${post.comments[0].text}</p>`
    }

    postHTML += `
    <div id="comments_section"></div>
    <i class="far fa-smile"></i>
    <form>
    <input id="comment_input" type="text">
    <input type="submit" value="Post" onclick="comment(${post.id})">
</div>
    `;

    return postHTML
};

function likePost(postID){
    console.log("in likePost with " + postID);
        const postData = {};

fetch("http://127.0.0.1:5000/api/posts/" + String(postID) + "/likes/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(function(response){
        if (response.status == 201){
            displayPosts();
        }
    })
}


function unlikePost(postID, otherID){
        const postData = {};

fetch("http://127.0.0.1:5000/api/posts/" + String(postID) + "/likes/" + String(otherID), {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(function(response){
        if (response.status == 201){
            displayPosts();
        }
    })
}

function bookmarkPost(postID){
        const postData = {
            "post_id": postID
        };

fetch("http://127.0.0.1:5000/api/bookmarks/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(function(response){
        if (response.status == 201){
            displayPosts();
        }
    })
}

function unbookmarkPost(postID, otherID){
        const postData = {
        };

fetch("http://127.0.0.1:5000/api/bookmarks/" + String(otherID), {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(function(response){
        if (response.status == 200){
            displayPosts();
        }
    })
}

function followUser(userID){

    var el = window.event.target;
    console.log(el)

console.log("in followUser userID is " +userID)
const postData = {
    "user_id": userID
};

fetch("http://127.0.0.1:5000/api/following/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(function(response){
        if (response.status == 201){
            console.log("success")
            document.getElementById(el.id).innerText = "Unfollow"
    
        }
        else{

        }
    });

//console.log("in followuser");
}

function unfollowUser(userID){

    var el = window.event.target;
    console.log(el)

const postData = {
};

fetch("http://127.0.0.1:5000/api/following/" + String(userID), {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
    .then(function(response){
        if (response.status == 200){
            console.log("success")
            document.getElementById(el.id).innerText = "Follow"
    
        }
        else{

        }
    });

//console.log("in followuser");
}

function comment(postID){
    const text = document.getElementById('comment_input').value;

    const postData = {
        "post_id": postID,
        "text": text
    };
    
    fetch("http://127.0.0.1:5000/api/comments", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        })
        .then(function(response){
            if (response.status == 201){
                console.log("success")
                displayPosts();
        
            }
            else{
    
            }
        });

}

var currentlyOpenButtonId = 0

function showModal(postID, buttonID){
    document.getElementsByClassName("modal")[0].style.display = "block";
    document.getElementsByClassName("modalBackground")[0].style.display = "block";

    console.log("buttonID is", buttonID)
    currentlyOpenButtonId = buttonID

    fetch('/api/posts/' + String(postID))
        .then(response => response.json())
        .then(post => {
            const html = postModal2HTML(post)//profiles.map(profile2Html);
            document.querySelector('.modal').innerHTML += html;
        })

    

}

function closeModal(){
    document.getElementsByClassName("modal")[0].style.display = "none";
    document.getElementsByClassName("modalBackground")[0].style.display = "none";
    console.log("BUTTON ID IS ", currentlyOpenButtonId)
    document.getElementById(currentlyOpenButtonId).focus()
}




const displayPosts = () => {

    fetch('/api/posts/?limit=10')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2HTML).join('\n') //profiles.map(profile2Html);
            document.querySelector('#posts').innerHTML = html;
        })
};


const initPage = () => {
    displayStories();
    displayProfile();
    displaySuggested();
    displayPosts();
};

// invoke init page to display stories:
initPage();