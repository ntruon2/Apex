import {backendLookup} from '../lookup'

export function apiBlogCreate(newBlog, callback){
    backendLookup("POST", "/blogs/create/", callback, {content: newBlog})
  }

export function apiBlogAction(blogId, action, callback){
    const data = {id: blogId, action: action}
    backendLookup("POST", "/blogs/action/", callback, data)
}

export function apiBlogDetail(blogId, callback) {
    backendLookup("GET", `/blogs/${blogId}/`, callback)
}


export function apiBlogList(username, callback) {
    let endpoint =  "/blogs/"
    if (username){
        endpoint =  `/blogs/?username=${username}`
    }
    backendLookup("GET", endpoint, callback)
}
